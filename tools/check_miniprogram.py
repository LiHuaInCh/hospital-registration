#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态检查：WXML 标签配对、事件处理函数、组件路径、@import 与 require 路径。"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join(ROOT, "miniprogram")

VOID = {"input", "image", "icon", "progress", "checkbox", "radio", "switch", "slider",
        "textarea", "camera", "live-player", "live-pusher", "import", "include", "wxs"}
TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w-]*)([^>]*?)(/?)>", re.S)
HANDLER_RE = re.compile(r'(?:bind|catch|capture-bind|capture-catch)[:a-zA-Z]*\s*=\s*"([^"{}]+)"')
REQUIRE_RE = re.compile(r"require\(\s*['\"]([^'\"]+)['\"]\s*\)")

problems = []


def check_wxml(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    stack = []
    for match in TAG_RE.finditer(text):
        closing, name, _attrs, self_close = match.groups()
        if name in VOID or self_close:
            continue
        if closing:
            if not stack:
                problems.append("%s: 多余的结束标签 </%s>" % (path, name))
            elif stack[-1] != name:
                problems.append("%s: 标签不匹配，期望 </%s> 实际 </%s>" % (path, stack[-1], name))
                stack.pop()
            else:
                stack.pop()
        else:
            stack.append(name)
    if stack:
        problems.append("%s: 未闭合标签 %s" % (path, ", ".join(stack)))


def check_handlers(wxml_path):
    js_path = wxml_path[:-5] + ".js"
    if not os.path.exists(js_path):
        return
    with open(wxml_path, encoding="utf-8") as f:
        wxml = f.read()
    with open(js_path, encoding="utf-8") as f:
        js = f.read()
    for handler in set(HANDLER_RE.findall(wxml)):
        name = handler.strip()
        if not name:
            continue
        if not re.search(r"\b" + re.escape(name) + r"\s*[:(]", js):
            problems.append("%s: 事件处理函数 %s 在 JS 中不存在" % (wxml_path, name))


def check_components():
    for base, _dirs, files in os.walk(MP):
        for name in files:
            if not name.endswith(".json"):
                continue
            path = os.path.join(base, name)
            with open(path, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as exc:
                    problems.append("%s: JSON 解析失败 %s" % (path, exc))
                    continue
            for key, value in (data.get("usingComponents") or {}).items():
                if value.startswith("/"):
                    full = os.path.join(MP, value.lstrip("/"))
                else:
                    full = os.path.normpath(os.path.join(base, value))
                if not os.path.exists(full + ".json"):
                    problems.append("%s: 组件 %s 路径不存在 (%s)" % (path, key, value))


def check_wxss_imports():
    for base, _dirs, files in os.walk(MP):
        for name in files:
            if not name.endswith(".wxss"):
                continue
            path = os.path.join(base, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            for target in re.findall(r'@import\s+"([^"]+)"', text):
                full = os.path.normpath(os.path.join(base, target))
                if not os.path.exists(full):
                    problems.append("%s: @import 目标不存在 %s" % (path, target))


def check_requires():
    """require 的相对路径写错时，页面会整体白屏，必须在提交前拦住。"""
    for base, _dirs, files in os.walk(MP):
        for name in files:
            if not name.endswith(".js"):
                continue
            path = os.path.join(base, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            for match in REQUIRE_RE.finditer(text):
                target = match.group(1)
                if not target.startswith("."):
                    continue
                full = os.path.normpath(os.path.join(base, target))
                if not (os.path.exists(full) or os.path.exists(full + ".js")):
                    problems.append("%s: require 路径不存在 %s" % (path, target))


for base, _dirs, files in os.walk(MP):
    for name in files:
        if name.endswith(".wxml"):
            full = os.path.join(base, name)
            check_wxml(full)
            check_handlers(full)

check_components()
check_wxss_imports()
check_requires()

if problems:
    print("发现 %d 个问题：" % len(problems))
    for item in problems:
        print(" -", item.replace(MP + os.sep, ""))
    sys.exit(1)

print("WXML / 组件 / 样式 / require 检查通过")
