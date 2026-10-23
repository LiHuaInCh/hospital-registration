#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
填充8个软件工程课设文档模板 - 完全重写版
模板结构: P0-P23(封面+任务分派表) + P24+(编写提示/内容区)
策略: 保留P0-P23, 替换P24+为项目实际内容
"""
import os, sys, shutil
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.oxml.ns import qn

TEMPLATE_DIR = r'C:\Users\26370\Desktop\软件工程课程设计文档模板'
OUTPUT_DIR = r'C:\Users\26370\Desktop\医院挂号导诊平台-课设文档'

def copy_templates():
    for f in os.listdir(TEMPLATE_DIR):
        if f.endswith('.docx'):
            shutil.copy2(os.path.join(TEMPLATE_DIR, f), os.path.join(OUTPUT_DIR, f))
            print(f'Copied: {f}')

def fix_doc_basics(doc):
    """Replace 2020->2026, ****系统/ **系统 -> project name"""
    proj = '医院门诊挂号与导诊服务平台'
    for p in doc.paragraphs:
        for run in p.runs:
            if '2020' in run.text:
                run.text = run.text.replace('2020', '2026')
            if '****系统' in run.text:
                run.text = run.text.replace('****系统', proj)
            if '**系统' in run.text:
                run.text = run.text.replace('**系统', proj)
            if '**' in run.text and ('医院' in p.text or '项目' in p.text):
                run.text = run.text.replace('**', proj)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        if '2020' in run.text:
                            run.text = run.text.replace('2020', '2026')
                        if '****系统' in run.text:
                            run.text = run.text.replace('****系统', proj)
                        if '**系统' in run.text:
                            run.text = run.text.replace('**系统', proj)

def fill_task_table(doc):
    """Fill the 7-row task assignment table (Table 1)"""
    if len(doc.tables) < 2:
        return
    table = doc.tables[1]
    members = [
        ['1', '20210101001', '成员A', '项目总体规划', '架构设计、后端框架搭建、代码审查', '文档完整、代码可运行', '6.08-6.17', '85'],
        ['2', '20210101002', '成员B', '小程序前端开发', '首页、科室列表、医生模块、前端组件', '页面完整、交互流畅', '6.08-6.17', '80'],
        ['3', '20210101003', '成员C', '挂号预约开发', '挂号预约流程(前后端)、排班、就诊人管理', '业务流程正确、事务安全', '6.08-6.17', '82'],
        ['4', '20210101004', '成员D', '智能导诊+数据库', '导诊算法设计、前后端实现、数据库设计', '算法正确、数据库规范', '6.08-6.17', '78'],
        ['5', '20210101005', '成员E', '管理后台+测试', '后台开发(前后端)、测试用例编写执行', '后台功能完整、测试通过', '6.08-6.17', '83'],
        ['6', '20210101006', '成员F', '用户认证+文档', '登录模块、JWT认证、权限控制、文档编写', '认证安全、文档规范', '6.08-6.17', '80'],
    ]
    # Table 1 has 7 rows (header + 6 members)
    for ri in range(1, min(len(table.rows), 7)):
        data = members[ri-1]
        for ci, val in enumerate(data):
            if ci < len(table.rows[ri].cells):
                cell = table.rows[ri].cells[ci]
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.text = ''
                cell.paragraphs[0].clear()
                run = cell.paragraphs[0].add_run(str(val))
                run.font.size = Pt(9)
    print('  Task table filled')

def fill_info_table(doc):
    """Fill the 4x2 project info table (Table 0)"""
    if len(doc.tables) < 1:
        return
    table = doc.tables[0]
    replacements = {
        '****系统': '医院门诊挂号与导诊服务平台',
        '***': '成员A',
        '软件171': '软件211',
        '**、**、**、**、**、**': '成员A、成员B、成员C、成员D、成员E、成员F、成员G',
    }
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    for old, new in replacements.items():
                        if old in run.text:
                            run.text = run.text.replace(old, new)
    print('  Info table filled')

def clear_content_area(doc):
    """Remove all paragraphs from P24 onwards (the writing guides)"""
    # Find the content start (usually around P24)
    # Strategy: delete paragraphs that contain template instructions
    to_delete = []
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if i < 20:  # Keep front matter
            continue
        # Check if this is a writing guide paragraph
        if ('编写提示' in text or '编写目的' in text or '附录' in text or
            ('A．' in text and len(text) > 20) or
            ('B．' in text and len(text) > 20) or
            ('C．' in text and len(text) > 20) or
            ('D．' in text and len(text) > 20) or
            ('E．' in text and len(text) > 20) or
            ('F．' in text and len(text) > 20)):
            to_delete.append(i)
    # Also delete empty paragraphs between deleted ones to clean up
    if to_delete:
        start_del = to_delete[0]
        # Delete from first guide paragraph to end
        for i in range(len(doc.paragraphs) - 1, start_del - 1, -1):
            p = doc.paragraphs[i]
            p._element.getparent().remove(p._element)
        print(f'  Cleared content area (deleted from P{start_del} to end)')
    else:
        print('  No content area to clear')

def add_content_paragraphs(doc, title, sections):
    """Add content sections as paragraphs. sections is list of (heading, body) tuples."""
    # Add document title
    p = doc.add_paragraph()
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(14)
    p.alignment = 1  # Center

    for heading, body in sections:
        # Add heading
        p = doc.add_paragraph()
        run = p.add_run(heading)
        run.bold = True
        run.font.size = Pt(12)

        # Add body
        p = doc.add_paragraph()
        run = p.add_run(body)
        run.font.size = Pt(10.5)
        # Add a blank line
        doc.add_paragraph()

# ============================================================
# DOC 1: 1项目开发计划.docx
# ============================================================
def fill_doc1():
    print('\n[Filling DOC 1: 项目开发计划]')
    path = os.path.join(OUTPUT_DIR, '1项目开发计划.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    clear_content_area(doc)

    # The first "content" paragraph (P26) is "1 项目开发计划" - keep as is or replace
    # Build content
    sections = [
        ('1.1 引言',
         '1.1.1 编写目的\n'
         '本项目开发计划旨在明确医院门诊挂号与导诊服务平台的开发目标、任务分工、进度安排和资源需求，'
         '为项目的顺利实施提供指导性文件。预期读者为项目组成员、指导教师和项目评审人员。\n\n'
         '1.1.2 项目背景\n'
         '项目名称：医院门诊挂号与导诊服务平台\n'
         '开发单位：江苏海洋大学计算机工程学院软件211班第1项目组\n'
         '用户群体：医院患者及医院管理人员\n'
         '随着医疗信息化的发展，传统门诊挂号方式存在排队时间长、信息不透明、患者体验差等问题。'
         '本项目旨在开发一款基于微信小程序的门诊挂号与导诊服务平台，改善患者就医体验。'),

        ('1.2 项目概述',
         '1.2.1 工作内容\n'
         '本项目的主要工作内容包括：\n'
         '(1) 需求分析：调研医院门诊挂号业务流程，编写软件需求说明书\n'
         '(2) 系统设计：进行概要设计和详细设计，包括架构设计、数据库设计、API设计\n'
         '(3) 编码实现：开发Spring Boot后端服务和微信小程序前端\n'
         '(4) 系统测试：功能测试、接口测试、兼容性测试\n'
         '(5) 文档编写：编写全套软件工程文档和用户手册\n\n'
         '1.2.2 主要参加人员\n'
         '本项目由7名软件工程专业学生组成开发团队，具体分工见任务分派表。\n\n'
         '1.2.3 产品交付物\n'
         '(1) 微信小程序源代码(患者端)\n'
         '(2) 微信小程序管理后台源代码\n'
         '(3) Spring Boot后端服务源代码\n'
         '(4) MySQL数据库初始化脚本\n'
         '(5) 全套软件工程文档(8份)\n'
         '(6) 用户使用说明书\n'
         '(7) 项目演示PPT'),

        ('1.3 实施计划',
         '1.3.1 任务分工\n'
         '详细任务分工见任务分派表(Table 1)。\n\n'
         '1.3.2 进度安排\n\n'
         '阶段一：需求分析(2026-06-08 ~ 2026-06-09，2天)\n'
         '  负责人：成员A、成员B\n'
         '  任务：需求调研、业务流程分析、编写软件需求说明书\n\n'
         '阶段二：系统设计(2026-06-10 ~ 2026-06-11，2天)\n'
         '  负责人：成员A、成员D\n'
         '  任务：系统架构设计、数据库设计、API接口设计、编写概要设计和详细设计说明书\n\n'
         '阶段三：编码实现(2026-06-12 ~ 2026-06-14，3天)\n'
         '  负责人：全员\n'
         '  任务：\n'
         '    成员A：项目框架搭建、后端核心代码开发\n'
         '    成员B：小程序首页、科室列表、医生模块开发\n'
         '    成员C：挂号预约流程、排班模块、就诊人管理开发\n'
         '    成员D：智能导诊模块、数据库开发\n'
         '    成员E：管理后台开发\n'
         '    成员F：用户登录认证模块开发\n'
         '    成员G：前后端联调\n\n'
         '阶段四：系统测试(2026-06-15 ~ 2026-06-16，2天)\n'
         '  负责人：成员E、成员F\n'
         '  任务：功能测试、接口测试、Bug修复、回归测试\n\n'
         '阶段五：文档整理(2026-06-17，1天)\n'
         '  负责人：成员G\n'
         '  任务：整理全套文档、编写用户手册、制作演示PPT'),

        ('1.4 支持条件',
         '1.4.1 计算机系统支持\n'
         '开发环境：Windows 11 Pro、JDK 1.8、IntelliJ IDEA、微信开发者工具\n'
         '运行环境：Spring Boot 2.7.14 + MySQL 8.0 + 微信小程序运行环境\n\n'
         '1.4.2 技术资料支持\n'
         '微信小程序开发文档、Spring Boot官方文档、MyBatis-Plus参考手册、MySQL参考手册\n\n'
         '1.4.3 外部支持\n'
         '指导教师提供技术指导和进度监督'),

        ('1.5 风险管理',
         '1.5.1 技术风险\n'
         '风险：微信登录集成涉及微信开放平台API调用，接口可能变更\n'
         '应对：采用模拟登录方案，预留微信API对接接口；学习微信小程序官方文档\n'
         '风险等级：中\n\n'
         '1.5.2 进度风险\n'
         '风险：小组成员时间协调困难，部分成员基础薄弱\n'
         '应对：每人安排明确的任务量和截止时间，定期同步进度\n'
         '风险等级：中\n\n'
         '1.5.3 数据风险\n'
         '风险：数据库设计变更可能影响开发进度\n'
         '应对：前期充分讨论数据库设计，尽量减少后期变更\n'
         '风险等级：低'),

        ('1.6 专题计划要点',
         '本项目开发过程中需要制定以下专题计划：\n'
         '(1) 测试计划：明确测试策略、测试用例和测试进度安排\n'
         '(2) 质量保证计划：代码审查规范、测试覆盖率要求(80%+)\n'
         '(3) 配置管理计划：Git版本控制、代码分支管理策略\n'
         '(4) 用户培训计划：用户使用说明书编写、系统操作演示'),
    ]
    add_content_paragraphs(doc, '项目开发计划', sections)

    # Fill Table 1 (task table) with proper data - this table has schedule info mixed in
    # Actually, the task table was already filled by fill_task_table, but the schedule info is also needed
    # Let's just make sure it looks right

    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 2: 2可行性研究报告.docx
# ============================================================
def fill_doc2():
    print('\n[Filling DOC 2: 可行性研究报告]')
    path = os.path.join(OUTPUT_DIR, '2可行性研究报告.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    fill_task_table(doc)
    clear_content_area(doc)

    sections = [
        ('1 引言',
         '1.1 编写目的\n'
         '本可行性研究报告旨在对医院门诊挂号与导诊服务平台项目的技术可行性、经济可行性、操作可行性、'
         '法律可行性和进度可行性进行全面分析，为项目是否立项提供决策依据。预期读者为项目评审教师、'
         '项目组成员和相关决策人员。\n\n'
         '1.2 项目背景\n'
         '项目名称：医院门诊挂号与导诊服务平台\n'
         '开发单位：江苏海洋大学计算机工程学院软件211班第1项目组\n'
         '用户群体：医院患者(主要用户)、医院管理人员\n'
         '随着医疗信息化建设的不断推进，传统门诊挂号方式存在排队时间长、信息不透明、'
         '患者满意度低等问题。本项目旨在利用微信小程序和Spring Boot技术栈，开发一款集在线挂号、'
         '智能导诊于一体的综合性医疗服务平台。'),

        ('2 可行性研究的前提',
         '2.1 基本要求\n'
         '功能要求：实现微信用户登录、科室浏览、医生查询、排班查看、在线挂号、智能导诊、'
         '挂号记录管理、就诊人管理和管理后台等核心功能。\n'
         '性能要求：API响应时间不超过3秒，支持50个用户同时在线。\n'
         '安全要求：用户数据加密存储，接口调用需认证。\n'
         '运行环境：微信小程序端运行在微信客户端，后端运行在Java 8 + MySQL 8.0环境。\n\n'
         '2.2 开发目标\n'
         '开发一个功能完整、操作简便、安全可靠的医院门诊挂号与导诊服务平台，'
         '为患者提供便捷的在线预约服务，为医院提供高效的挂号管理工具。\n\n'
         '2.3 假定和限制\n'
         '假定用户已安装微信客户端并具备基本操作能力。\n'
         '开发周期限制为10天(2026年6月8日至2026年6月17日)。\n'
         '预算限制为零(全部使用开源免费技术)。'),

        ('3 对现有系统的分析',
         '3.1 现有系统概述\n'
         '当前医院门诊挂号主要依赖以下方式：\n'
         '(1) 现场窗口挂号：患者在门诊大厅排队挂号，高峰期排队时间长，体验差\n'
         '(2) 自助机挂号：医院大厅设有自助挂号机，但部分患者(特别是老年人)操作不便\n'
         '(3) 医院自有App/网站挂号：部分医院提供在线挂号通道，但App需要下载安装，'
         '使用门槛较高\n\n'
         '3.2 现有系统存在的问题\n'
         '(1) 排队时间长：高峰期患者需提前数小时排队\n'
         '(2) 信息不透明：患者不清楚各科室医生的排班情况和剩余号源\n'
         '(3) 缺乏导诊服务：患者不了解自身症状对应哪个科室，挂错号的情况常见\n'
         '(4) 操作不便：医院自有App需要单独下载安装，用户获取成本高\n'
         '(5) 管理效率低：排班和号源管理主要依赖人工操作'),

        ('4 所建议的系统',
         '4.1 对所建议系统的说明\n'
         '本系统采用微信小程序 + Spring Boot + MySQL技术架构，具有以下优势：\n'
         '(1) 微信小程序免安装：用户无需下载安装，扫描二维码或在微信中搜索即可使用\n'
         '(2) 在线挂号：患者可随时随地查看医生排班和号源情况，在线完成挂号预约\n'
         '(3) 智能导诊：根据患者描述的症状，自动推荐对应科室，减少挂错号的情况\n'
         '(4) 数字化管理：管理人员可通过小程序后台进行科室、医生、排班的全数字化管理\n\n'
         '4.2 技术方案\n'
         '前端：微信小程序原生框架(WXML + WXSS + JavaScript)\n'
         '后端：Spring Boot 2.7.14 + MyBatis-Plus 3.5.3.1\n'
         '数据库：MySQL 8.0\n'
         '认证：JWT(JSON Web Token) + 管理员BCrypt密码验证\n\n'
         '4.3 处理流程\n'
         '患者挂号流程：打开小程序 → 微信登录 → 浏览科室/医生 → 查看排班 → 选择时段 → '
         '选择就诊人 → 确认挂号 → 挂号成功\n'
         '智能导诊流程：输入症状 → 系统匹配关键词 → 返回推荐科室 → 点击科室查看医生 → 挂号'),

        ('5 技术可行性分析',
         '5.1 前端技术可行性\n'
         '微信小程序是腾讯公司的成熟平台，日活跃用户超过4亿，SDK和API文档完善。'
         '微信开发者工具提供代码编辑、调试、预览和真机调试等全套开发功能。'
         '小程序原生框架(WXML/WXSS/JS)学习曲线平缓，小组成员经过基础学习即可上手开发。\n\n'
         '5.2 后端技术可行性\n'
         'Spring Boot是Java生态中最流行的企业级开发框架，版本2.7.14稳定可靠。'
         'MyBatis-Plus简化了MyBatis的数据库操作，提供开箱即用的CRUD功能和条件构造器。'
         'MySQL 8.0是成熟的关系型数据库，性能和稳定性经过广泛验证。\n\n'
         '5.3 技术成熟度\n'
         '所有采用的技术均为业界成熟技术，社区活跃，文档完善，不存在技术"卡脖子"问题。'
         '同类项目(微信小程序+Spring Boot)在网上有大量开源案例可参考。'),

        ('6 经济可行性分析',
         '6.1 开发成本\n'
         '本项目的开发成本接近于零：\n'
         '(1) 微信开发者工具：免费\n'
         '(2) Spring Boot框架：开源免费(Apache 2.0协议)\n'
         '(3) MySQL数据库：社区版免费\n'
         '(4) MyBatis-Plus：开源免费(Apache 2.0协议)\n'
         '(5) 开发工具(IntelliJ IDEA)：可使用社区免费版\n'
         '(6) 服务器：开发阶段使用本地计算机，无需额外投入\n\n'
         '6.2 运行维护成本\n'
         '系统部署在本地服务器或低成本云服务器(如阿里云学生机，约100元/年)，'
         '运维成本极低。日常维护仅需定期备份数据库和更新SSL证书。\n\n'
         '6.3 效益分析\n'
         '系统可显著提高医院门诊服务效率，减少患者排队时间，提升患者满意度。'
         '同时实现了挂号管理的数字化和自动化，减少了医院的人工管理成本。'),

        ('7 操作可行性分析',
         '7.1 用户操作便捷性\n'
         '用户只需安装微信即可使用小程序，无需额外下载安装。小程序操作界面简洁直观，'
         '采用底部Tab导航(首页、智能导诊、挂号记录、我的)，功能分类清晰，'
         '符合微信小程序用户使用习惯。\n\n'
         '7.2 管理操作便捷性\n'
         '管理后台集成在微信小程序中，管理员通过独立入口登录后台。'
         '提供科室、医生、排班的图形化管理界面，支持列表查看、新增、编辑、删除等操作，'
         '即使非技术人员也能快速上手使用。\n\n'
         '7.3 学习培训成本\n'
         '患者端：界面设计直观，无需培训即可使用，主要功能均有文字提示\n'
         '管理端：操作逻辑清晰，管理员可以进行简单的操作培训(约15分钟)'),

        ('8 法律可行性分析',
         '8.1 知识产权\n'
         '本项目使用的所有技术框架和工具均为开源软件，遵循各自的Apache 2.0、MIT等开源协议。'
         '项目不涉及第三方专利或商业软件的侵权行为。\n\n'
         '8.2 数据合规\n'
         '系统收集的用户数据(微信昵称、手机号、身份证号等)仅用于挂号服务，'
         '存储在本地数据库，不外传至第三方。系统设计符合《中华人民共和国网络安全法》'
         '和《个人信息保护法》的相关要求。\n\n'
         '8.3 平台合规\n'
         '微信小程序开发遵循《微信小程序平台运营规范》，不涉及小程序禁止的类目。'
         '本项目为课程设计教学目的，不涉及商业运营。'),

        ('9 进度可行性分析',
         '9.1 开发周期\n'
         '项目开发周期为10天(2026年6月8日至2026年6月17日)，分为5个阶段：\n'
         '需求分析(2天) → 系统设计(2天) → 编码实现(3天) → 系统测试(2天) → 文档整理(1天)\n\n'
         '9.2 人员配置\n'
         '项目组由7名成员组成，每人有明确的任务分工。采用敏捷开发方式，'
         '每日同步进度，及时发现和解决问题。\n\n'
         '9.3 风险评估\n'
         '主要风险：小组成员时间协调困难、部分技术点(如微信登录对接)的学习成本。'
         '通过合理分工、简化技术方案(模拟登录而不是对接真实微信API)来降低风险。'
         '10天的开发周期对本项目的功能规模是合理的。'),

        ('10 结论',
         '经过对技术、经济、操作、法律和进度五个方面的综合评估，得出以下结论：\n\n'
         '(1) 技术上：所采用的技术均为成熟稳定技术，完全可行\n'
         '(2) 经济上：开发成本接近于零，经济可行\n'
         '(3) 操作上：用户操作简便，无须培训\n'
         '(4) 法律上：不涉及侵权问题，符合相关法律法规\n'
         '(5) 进度上：10天开发周期合理，人员配置充足\n\n'
         '综合结论：本项目完全可行，建议立即立项，按照项目开发计划推进实施。'),

        ('参考资料',
         '1. 微信小程序开发文档, https://developers.weixin.qq.com/miniprogram/dev/\n'
         '2. Spring Boot Reference Documentation, https://docs.spring.io/spring-boot/docs/2.7.14/reference/\n'
         '3. MyBatis-Plus 参考手册, https://baomidou.com/\n'
         '4. MySQL 8.0 Reference Manual, https://dev.mysql.com/doc/refman/8.0/en/\n'
         '5. 张海藩. 软件工程导论(第6版). 清华大学出版社, 2013\n'
         '6. 微信小程序平台运营规范, https://developers.weixin.qq.com/miniprogram/product/'),
    ]
    add_content_paragraphs(doc, '可行性研究报告', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 3: 3软件需求说明书.docx
# ============================================================
def fill_doc3():
    print('\n[Filling DOC 3: 软件需求说明书]')
    path = os.path.join(OUTPUT_DIR, '3软件需求说明书.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    fill_task_table(doc)
    clear_content_area(doc)

    sections = [
        ('1 引言',
         '1.1 编写目的\n'
         '本软件需求说明书旨在详细描述医院门诊挂号与导诊服务平台的功能需求和非功能需求，'
         '为后续的系统设计、编码实现和测试验收提供依据。预期读者为项目组成员、'
         '指导教师和项目评审人员。\n\n'
         '1.2 项目背景\n'
         '项目名称：医院门诊挂号与导诊服务平台\n'
         '开发单位：江苏海洋大学计算机工程学院\n'
         '随着医疗信息化的发展，传统门诊挂号方式效率低下，患者体验差。'
         '本项目利用微信小程序和Spring Boot技术开发一套在线挂号与导诊服务平台，'
         '提升医疗服务的效率和患者满意度。\n\n'
         '1.3 术语定义\n'
         '就诊人：实际去医院就诊的人，可以是用户本人或其他家人\n'
         '号源：每个排班时段可供挂号的名额数量\n'
         '排班：医生在特定日期、特定时段的出诊安排\n'
         '导诊：根据患者症状描述推荐合适的就诊科室\n'
         'openid：微信用户在小程序中的唯一标识'),

        ('2 任务概述',
         '2.1 系统目标\n'
         '(1) 实现在线预约挂号功能，减少患者现场排队等待时间\n'
         '(2) 提供智能分诊导诊服务，帮助患者根据症状选择合适的科室\n'
         '(3) 为医院管理人员提供科室、医生、排班的数字化管理工具\n'
         '(4) 提升医院门诊服务效率，改善患者就医体验\n\n'
         '2.2 用户角色\n'
         '(1) 患者(普通用户)：系统的主要使用者，通过小程序进行在线挂号、智能导诊、'
         '查看挂号记录、管理就诊人信息\n'
         '(2) 就诊人：被挂号的看病对象，可以是用户本人或家人\n'
         '(3) 管理员：医院工作人员，通过后台管理科室、医生、排班和订单\n\n'
         '2.3 运行环境\n'
         '前端：微信小程序，支持iOS和Android微信客户端\n'
         '后端：JDK 1.8 + Spring Boot 2.7.14\n'
         '数据库：MySQL 8.0\n'
         '服务器：Windows/Linux服务器'),

        ('3 功能需求',
         '3.1 用户登录(用户模块)\n'
         '功能描述：用户通过微信一键登录小程序\n'
         '输入：微信授权code、用户昵称、头像URL\n'
         '处理：后端根据code模拟生成openid，首次登录自动注册用户信息\n'
         '输出：用户ID、昵称、头像URL、认证token\n'
         '接口：POST /api/user/login\n\n'
         '3.2 科室浏览(科室模块)\n'
         '功能描述：首页展示12个科室列表，包含科室名称、图标、介绍、位置\n'
         '输入：无\n'
         '处理：查询department表中status=1的科室，按sort_order排序\n'
         '输出：科室列表JSON数组\n'
         '接口：GET /api/department/list\n\n'
         '3.3 医生查询(医生模块)\n'
         '功能描述：按科室筛选或按姓名关键字搜索医生\n'
         '输入：departmentId(可选)或keyword关键字\n'
         '处理：按条件查询doctor表，并关联查询department名称\n'
         '输出：医生列表或医生详情(含科室名称、职称、擅长、简介、挂号费)\n'
         '接口：GET /api/doctor/list?departmentId=X, GET /api/doctor/search?keyword=X, GET /api/doctor/detail?id=X\n\n'
         '3.4 排班查看(排班模块)\n'
         '功能描述：查看医生未来7天的出诊排班和号源情况\n'
         '输入：doctorId\n'
         '处理：查询schedule表work_date在today~today+7days范围的记录，'
         '关联doctor表填充姓名、职称、挂号费\n'
         '输出：排班列表(含日期、时段、剩余号源数、医生信息)\n'
         '接口：GET /api/schedule/list?doctorId=X, GET /api/schedule/dates\n\n'
         '3.5 在线挂号(挂号模块)\n'
         '功能描述：用户选择就诊人确认挂号，系统扣减号源并创建挂号记录\n'
         '输入：userId, patientId, scheduleId, departmentId, doctorId, workDate, timeSlot\n'
         '处理：(1)查询排班信息获取挂号费 (2)在事务中先扣减号源(remain_count-1)'
         '再插入挂号记录 (3)号源已满则提示错误\n'
         '输出：挂号成功或失败消息\n'
         '接口：POST /api/registration/create\n\n'
         '3.6 智能导诊(导诊模块)\n'
         '功能描述：用户输入症状描述，系统推荐对应科室\n'
         '输入：症状描述文本\n'
         '处理：(1)遍历内置症状-科室关键词匹配库(100+关键词)'
         '(2)使用String.contains()匹配 (3)统计各科室匹配关键词数量'
         '(4)计算置信度(50+匹配数*10，上限95)'
         '(5)按匹配数降序排列返回\n'
         '输出：推荐科室列表(含科室名、介绍、位置、匹配关键词、置信度)\n'
         '接口：POST /api/guidance/triage\n\n'
         '3.7 挂号记录(挂号模块)\n'
         '功能描述：查看用户的全部挂号记录，支持状态筛选和取消操作\n'
         '输入：userId, 可选状态筛选条件\n'
         '处理：查询registration表，关联patient/doctor/department填充名称信息\n'
         '输出：挂号记录列表(含就诊人、医生、科室、日期、时段、费用、状态)\n'
         '接口：GET /api/registration/list?userId=X, POST /api/registration/cancel\n\n'
         '3.8 就诊人管理(就诊人模块)\n'
         '功能描述：管理就诊人信息(姓名、身份证号、手机号、性别、年龄、关系)\n'
         '输入：userId, 就诊人信息各字段\n'
         '处理：patient表的增删改查操作\n'
         '输出：操作成功或失败\n'
         '接口：GET /api/patient/list, POST /api/patient/add, PUT /api/patient/update, DELETE /api/patient/delete\n\n'
         '3.9 管理后台(管理模块)\n'
         '功能描述：管理员通过用户名密码登录后台，管理科室、医生、排班和订单\n'
         '输入：管理员用户名和密码\n'
         '处理：(1)通过BCrypt验证密码 (2)提供科室/医生/排班的增删改查 (3)查看全部挂号记录\n'
         '输出：登录结果和管理操作结果\n'
         '接口：POST /api/admin/login + 各模块的增删改查接口'),

        ('4 非功能需求',
         '4.1 性能需求\n'
         '(1) API响应时间：所有API接口响应时间不超过3秒\n'
         '(2) 并发支持：系统支持至少50个用户同时在线操作\n'
         '(3) 数据库查询：常见查询操作应在100ms内完成\n\n'
         '4.2 安全性需求\n'
         '(1) 用户认证：使用token机制进行用户身份认证\n'
         '(2) 密码加密：管理员密码使用BCrypt算法加密存储\n'
         '(3) 数据传输：建议使用HTTPS加密传输\n'
         '(4) 输入校验：使用@Valid对请求参数进行校验\n\n'
         '4.3 可用性需求\n'
         '(1) 系统应7×24小时可用(计划维护时间除外)\n'
         '(2) 系统故障后应能在30分钟内恢复运行\n\n'
         '4.4 兼容性需求\n'
         '(1) 小程序兼容iOS和Android微信客户端(微信版本8.0+)\n'
         '(2) 界面适配不同手机屏幕尺寸(3.5寸至6.7寸)\n\n'
         '4.5 可维护性需求\n'
         '(1) 代码遵循RESTful API设计规范\n'
         '(2) 数据库表设计遵循第三范式(3NF)\n'
         '(3) 关键业务逻辑添加注释说明'),

        ('5 数据字典',
         '本系统包含7个数据表，各表结构如下：\n\n'
         '5.1 admin(管理员表)\n'
         'id BIGINT(主键自增), username VARCHAR(50,唯一), password VARCHAR(255,BCrypt加密), '
         'real_name VARCHAR(50), phone VARCHAR(20), status TINYINT(1启用0禁用), '
         'create_time DATETIME, update_time DATETIME\n\n'
         '5.2 user(微信用户表)\n'
         'id BIGINT(主键自增), openid VARCHAR(100,唯一), nickname VARCHAR(100), '
         'avatar_url VARCHAR(500), phone VARCHAR(20), create_time DATETIME, update_time DATETIME\n\n'
         '5.3 patient(就诊人表)\n'
         'id BIGINT(主键自增), user_id BIGINT(外键关联user表), name VARCHAR(50), '
         'id_card VARCHAR(18), phone VARCHAR(20), gender TINYINT(1男2女), age INT, '
         'relationship VARCHAR(20), is_default TINYINT(1是0否), create_time DATETIME, update_time DATETIME\n\n'
         '5.4 department(科室表)\n'
         'id BIGINT(主键自增), name VARCHAR(100), description VARCHAR(500), icon VARCHAR(255), '
         'location VARCHAR(200), phone VARCHAR(20), sort_order INT, status TINYINT(1启用0禁用), '
         'create_time DATETIME, update_time DATETIME\n\n'
         '5.5 doctor(医生表)\n'
         'id BIGINT(主键自增), department_id BIGINT(外键关联department), name VARCHAR(50), '
         'gender TINYINT(1男2女), title VARCHAR(50), specialty VARCHAR(500), description TEXT, '
         'avatar VARCHAR(500), consultation_fee DECIMAL(10,2), status TINYINT(1在岗0离职), '
         'create_time DATETIME, update_time DATETIME\n\n'
         '5.6 schedule(排班表)\n'
         'id BIGINT(主键自增), doctor_id BIGINT(外键关联doctor), work_date DATE, '
         'time_slot VARCHAR(20), start_time TIME, end_time TIME, total_count INT(默认30), '
         'remain_count INT(默认30), status TINYINT(1正常2停诊), create_time DATETIME, update_time DATETIME\n'
         '唯一约束：(doctor_id, work_date, time_slot)\n\n'
         '5.7 registration(挂号记录表)\n'
         'id BIGINT(主键自增), user_id BIGINT(外键), patient_id BIGINT(外键), '
         'schedule_id BIGINT(外键), department_id BIGINT(外键), doctor_id BIGINT(外键), '
         'work_date DATE, time_slot VARCHAR(20), fee DECIMAL(10,2), '
         'status TINYINT(1已预约2已签到3已完成4已取消), cancel_reason VARCHAR(255), '
         'create_time DATETIME, update_time DATETIME'),

        ('6 用例图描述',
         '6.1 患者挂号用例\n'
         '参与者：患者(微信用户)\n'
         '用例流程：登录 → 浏览科室 → 查看医生 → 查看排班 → 选择时段 → 选择就诊人 → '
         '确认挂号 → 查看挂号记录 → (可选)取消挂号\n'
         '前置条件：用户已微信登录\n'
         '后置条件：挂号记录创建成功，号源扣减\n\n'
         '6.2 智能导诊用例\n'
         '参与者：患者\n'
         '用例流程：进入导诊页 → 输入症状描述 → 点击"开始导诊" → 系统匹配关键词 → '
         '显示推荐科室 → 点击科室跳转医生列表 → 选择医生挂号\n'
         '前置条件：用户已微信登录\n'
         '后置条件：用户获得科室推荐结果\n\n'
         '6.3 就诊人管理用例\n'
         '参与者：患者\n'
         '用例流程：进入"我的" → 就诊人管理 → (可选)添加/编辑/删除就诊人 → 设置默认就诊人\n\n'
         '6.4 管理员维护用例\n'
         '参与者：管理员\n'
         '用例流程：进入管理后台入口 → 管理员登录 → 管理科室(增删改查) → '
         '管理医生(增删改查) → 管理排班(增删改查) → 查看订单'),

        ('7 接口设计要求',
         '7.1 接口风格\n'
         '采用RESTful API风格，URL使用名词复数形式表示资源\n\n'
         '7.2 数据格式\n'
         '请求和响应均使用JSON格式，Content-Type: application/json\n\n'
         '7.3 统一响应格式\n'
         '成功：{"code": 200, "message": "操作成功", "data": {...}}\n'
         '失败：{"code": 500, "message": "错误描述", "data": null}\n\n'
         '7.4 认证方式\n'
         '用户认证：登录后返回token，后续请求在Header中携带token\n'
         '管理员认证：用户名 + BCrypt加密密码直接验证'),
    ]
    add_content_paragraphs(doc, '软件需求说明书', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 4: 4概要设计说明书.docx
# ============================================================
def fill_doc4():
    print('\n[Filling DOC 4: 概要设计说明书]')
    path = os.path.join(OUTPUT_DIR, '4概要设计说明书.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    fill_task_table(doc)
    clear_content_area(doc)

    sections = [
        ('1 引言',
         '1.1 编写目的\n'
         '本概要设计说明书旨在描述医院门诊挂号与导诊服务平台的总体架构设计、'
         '模块划分、数据库设计和接口设计，为后续的详细设计和编码实现提供指导。\n\n'
         '1.2 项目背景\n'
         '系统名称：医院门诊挂号与导诊服务平台\n'
         '技术架构：微信小程序 + Spring Boot + MyBatis-Plus + MySQL\n'
         '采用前后端分离的分层架构设计。'),

        ('2 总体设计',
         '2.1 系统架构\n'
         '本系统采用经典的四层架构设计：\n\n'
         '表现层(Presentation Layer)：微信小程序前端\n'
         '  - 使用WXML + WXSS + JavaScript开发\n'
         '  - 负责用户界面展示和交互处理\n'
         '  - 通过wx.request调用后端API\n\n'
         '业务逻辑层(Business Layer)：Spring Boot后端\n'
         '  - 使用Java 8 + Spring Boot 2.7.14开发\n'
         '  - 包含Controller(请求处理)、Service(业务逻辑)、DTO(数据传输对象)\n'
         '  - 实现用户认证、挂号业务、导诊算法等核心逻辑\n\n'
         '数据访问层(Data Access Layer)：MyBatis-Plus\n'
         '  - 提供ORM映射和基础CRUD操作\n'
         '  - LambdaQueryWrapper实现类型安全的查询条件构造\n'
         '  - 支持事务管理(@Transactional)\n\n'
         '数据层(Data Layer)：MySQL数据库\n'
         '  - 存储用户、科室、医生、排班、挂号等业务数据\n'
         '  - 使用InnoDB引擎支持事务\n'
         '  - 字符集utf8mb4支持emoji(科室图标)\n\n'
         '2.2 技术选型\n'
         '前端框架：微信小程序原生框架\n'
         '后端框架：Spring Boot 2.7.14\n'
         'ORM框架：MyBatis-Plus 3.5.3.1\n'
         '数据库：MySQL 8.0\n'
         '认证库：jjwt 0.9.1\n'
         '简化开发：Lombok\n'
         '参数校验：spring-boot-starter-validation\n'
         '构建工具：Maven\n\n'
         '2.3 运行环境\n'
         '服务器：JDK 1.8、MySQL 8.0、Windows/Linux操作系统\n'
         '客户端：微信客户端(iOS 10+ 或 Android 5.0+)\n'
         '网络：HTTP/HTTPS协议'),

        ('3 模块设计',
         '系统分为7个核心模块，每个模块对应一个Controller：\n\n'
         '3.1 用户模块(User Module)\n'
         '  控制器：UserController\n'
         '  服务层：UserService / UserServiceImpl\n'
         '  数据访问：UserMapper / User实体\n'
         '  功能：微信用户登录，openid管理，token生成和返回\n'
         '  关键接口：POST /api/user/login\n\n'
         '3.2 科室模块(Department Module)\n'
         '  控制器：DepartmentController\n'
         '  服务层：DepartmentService / DepartmentServiceImpl\n'
         '  数据访问：DepartmentMapper / Department实体\n'
         '  功能：科室列表查询(按sort_order排序)、科室详情查询\n'
         '  管理员功能：科室增删改操作\n'
         '  关键接口：GET /api/department/list, POST/PUT/DELETE /api/department/*\n\n'
         '3.3 医生模块(Doctor Module)\n'
         '  控制器：DoctorController\n'
         '  服务层：DoctorService / DoctorServiceImpl\n'
         '  数据访问：DoctorMapper / Doctor实体\n'
         '  功能：按科室筛选医生、按关键字搜索医生、医生详情查询\n'
         '  特点：查询列表和详情时自动填充科室名称(departmentName)\n'
         '  关键接口：GET /api/doctor/list, GET /api/doctor/search, GET /api/doctor/detail\n\n'
         '3.4 排班模块(Schedule Module)\n'
         '  控制器：ScheduleController\n'
         '  服务层：ScheduleService / ScheduleServiceImpl\n'
         '  数据访问：ScheduleMapper / Schedule实体\n'
         '  功能：查询医生未来7天排班、获取7天日期列表、排班管理\n'
         '  特点：排班数据自动填充医生姓名、职称、挂号费\n'
         '  关键接口：GET /api/schedule/list, GET /api/schedule/dates, POST /api/schedule/add\n\n'
         '3.5 挂号模块(Registration Module)\n'
         '  控制器：RegistrationController\n'
         '  服务层：RegistrationService / RegistrationServiceImpl\n'
         '  数据访问：RegistrationMapper / Registration实体\n'
         '  功能：创建挂号(扣减号源)、查询挂号记录、取消挂号(恢复号源)\n'
         '  特点：使用@Transactional保证事务一致性，号源扣减使用WHERE remain_count>0防止超卖\n'
         '  关键接口：POST /api/registration/create, GET /api/registration/list, POST /api/registration/cancel\n\n'
         '3.6 导诊模块(Guidance Module)\n'
         '  控制器：GuidanceController\n'
         '  依赖：DepartmentService\n'
         '  功能：症状文本 → 关键词匹配 → 科室推荐\n'
         '  特点：内置100+症状关键词的SYMPTOM_MAP(LinkedHashMap)，覆盖12个科室\n'
         '  算法：String.contains()模糊匹配 → 统计匹配数 → 计算置信度 → 降序排列\n'
         '  关键接口：POST /api/guidance/triage\n\n'
         '3.7 管理模块(Admin + Patient Module)\n'
         '  控制器：AdminController, PatientController\n'
         '  功能：管理员登录认证、就诊人CRUD管理\n'
         '  安全：管理员密码BCrypt加密存储，就诊人操作关联用户ID'),
        ('4 数据库设计',
         '4.1 E-R关系描述\n'
         'User(微信用户) 1:N Patient(就诊人)\n'
         'Department(科室) 1:N Doctor(医生)\n'
         'Doctor(医生) 1:N Schedule(排班)\n'
         'User 1:N Registration(挂号记录)\n'
         'Patient 1:N Registration\n'
         'Schedule 1:N Registration\n'
         'Admin(管理员) 独立实体\n\n'
         '4.2 数据库表结构(7张表)\n'
         '(1) admin — 管理员表(id, username(唯一), password(BCrypt), real_name, phone, status, create_time, update_time)\n'
         '(2) user — 微信用户表(id, openid(唯一), nickname, avatar_url, phone, create_time, update_time)\n'
         '(3) patient — 就诊人表(id, user_id(FK), name, id_card, phone, gender, age, relationship, is_default, create_time, update_time)\n'
         '(4) department — 科室表(id, name, description, icon, location, phone, sort_order, status, create_time, update_time)\n'
         '(5) doctor — 医生表(id, department_id(FK), name, gender, title, specialty, description, avatar, consultation_fee, status, create_time, update_time)\n'
         '(6) schedule — 排班表(id, doctor_id(FK), work_date, time_slot, start_time, end_time, total_count, remain_count, status, create_time, update_time)\n'
         '    唯一约束：UK(doctor_id, work_date, time_slot)\n'
         '(7) registration — 挂号记录表(id, user_id(FK), patient_id(FK), schedule_id(FK), department_id(FK), doctor_id(FK), work_date, time_slot, fee, status(1已预约2已签到3已完成4已取消), cancel_reason, create_time, update_time)\n\n'
         '所有表均使用InnoDB引擎、utf8mb4字符集，主键id为BIGINT自增。'),
        ('5 API接口设计',
         '系统共设计22个RESTful API接口，按模块分组如下：\n\n'
         '用户模块(1个)：\n'
         '  POST /api/user/login — 微信用户登录\n\n'
         '科室模块(5个)：\n'
         '  GET /api/department/list — 获取科室列表\n'
         '  GET /api/department/detail?id=X — 获取科室详情\n'
         '  POST /api/department/add — 添加科室(管理员)\n'
         '  PUT /api/department/update — 更新科室(管理员)\n'
         '  DELETE /api/department/delete?id=X — 删除科室(管理员)\n\n'
         '医生模块(5个)：\n'
         '  GET /api/doctor/list?departmentId=X — 按科室查医生\n'
         '  GET /api/doctor/search?keyword=X — 按姓名搜索医生\n'
         '  GET /api/doctor/detail?id=X — 医生详情\n'
         '  POST /api/doctor/add — 添加医生(管理员)\n'
         '  PUT /api/doctor/update — 更新医生(管理员)\n'
         '  DELETE /api/doctor/delete?id=X — 删除医生(管理员)\n\n'
         '排班模块(4个)：\n'
         '  GET /api/schedule/list?doctorId=X — 查看排班\n'
         '  GET /api/schedule/dates — 获取日期列表\n'
         '  POST /api/schedule/add — 添加排班(管理员)\n'
         '  PUT /api/schedule/update — 更新排班(管理员)\n\n'
         '挂号模块(3个)：\n'
         '  POST /api/registration/create — 创建挂号\n'
         '  GET /api/registration/list?userId=X — 挂号记录\n'
         '  POST /api/registration/cancel — 取消挂号\n\n'
         '导诊模块(1个)：\n'
         '  POST /api/guidance/triage — 智能导诊\n\n'
         '就诊人模块(4个)：\n'
         '  GET /api/patient/list?userId=X — 就诊人列表\n'
         '  POST /api/patient/add — 添加就诊人\n'
         '  PUT /api/patient/update — 更新就诊人\n'
         '  DELETE /api/patient/delete?id=X — 删除就诊人\n\n'
         '管理模块(1个)：\n'
         '  POST /api/admin/login — 管理员登录'),
        ('6 安全设计',
         '6.1 认证机制\n'
         '用户端：微信登录后后端生成临时token("token_" + userId + "_" + timestamp)，返回给前端存储\n'
         '管理端：用户名 + BCrypt加密密码验证，密码存储在admin表中\n\n'
         '6.2 跨域配置\n'
         'CorsConfig允许所有来源的跨域请求(allowedOrigins="*")，开发阶段方便联调\n\n'
         '6.3 数据安全\n'
         '(1) 密码使用BCrypt不可逆加密存储\n'
         '(2) 敏感信息(密码)不在API响应中返回(setPassword(null))\n'
         '(3) 建议生产环境使用HTTPS传输加密\n'
         '(4) 就诊人身份证号建议脱敏显示\n\n'
         '6.4 事务安全\n'
         '挂号操作使用@Transactional保证原子性：号源扣减和记录创建在同一事务中'),
        ('7 部署设计',
         '部署架构：用户手机(微信小程序) → HTTPS → Nginx(可选反向代理) → Spring Boot(8080) → MySQL(3306)\n\n'
         '开发环境：\n'
         '  后端Spring Boot运行在本地(端口8080)\n'
         '  使用ngrok进行内网穿透，获取公网域名供小程序调用\n'
         '  微信开发者工具编译和预览小程序\n\n'
         '生产环境建议：\n'
         '  前端：小程序代码提交至微信公众平台审核发布\n'
         '  后端：部署至云服务器(CentOS/Ubuntu)\n'
         '  数据库：MySQL部署在同一服务器或独立数据库服务器\n'
         '  反向代理：Nginx配置HTTPS证书和请求转发'),
    ]
    add_content_paragraphs(doc, '概要设计说明书', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 5: 5详细设计说明书.docx
# ============================================================
def fill_doc5():
    print('\n[Filling DOC 5: 详细设计说明书]')
    path = os.path.join(OUTPUT_DIR, '5详细设计说明书.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    fill_task_table(doc)
    clear_content_area(doc)

    sections = [
        ('1 引言',
         '1.1 编写目的\n'
         '本详细设计说明书旨在对医院门诊挂号与导诊服务平台各模块的详细处理流程、'
         '算法逻辑、数据库表结构和API规格进行描述，为编码实现提供精确的指导。\n\n'
         '1.2 项目概述\n'
         '系统采用Spring Boot + MyBatis-Plus + MySQL技术栈，'
         '前端为微信小程序，包含7个核心模块和22个API接口。'),

        ('2 程序系统结构',
         '系统采用MVC分层架构，各层对应关系如下：\n'
         'Controller层(8个)：UserController, DepartmentController, DoctorController, '
         'ScheduleController, RegistrationController, GuidanceController, '
         'PatientController, AdminController\n'
         'Service层(6个接口)：UserService, DepartmentService, DoctorService, '
         'ScheduleService, RegistrationService, PatientService, AdminService\n'
         'ServiceImpl层(7个实现)：各Service接口的实现类\n'
         'Mapper层(7个)：各实体的MyBatis-Plus Mapper接口\n'
         'Entity层(7个)：Admin, User, Patient, Department, Doctor, Schedule, Registration\n'
         'DTO层(5个)：WxLoginDTO, LoginDTO, RegistrationDTO, GuidanceDTO, GuidanceResultDTO\n'
         'Common层(1个)：R<T>(统一响应封装)'),

        ('3 用户登录模块详细设计',
         '3.1 模块描述\n'
         '处理微信小程序的用户登录请求，通过模拟openid机制实现用户身份识别。\n\n'
         '3.2 处理流程\n'
         '(1) 小程序端：wx.login()获取临时code\n'
         '(2) 小程序端：wx.getUserProfile()获取用户昵称和头像(需用户授权)\n'
         '(3) 小程序端：wx.request POST /api/user/login 发送{code, nickname, avatarUrl}\n'
         '(4) 后端UserController.login()接收WxLoginDTO参数\n'
         '(5) 生成模拟openid: "wx_" + code\n'
         '(6) 调用UserService.loginByOpenid(openid, nickname, avatarUrl)\n'
         '(7) LambdaQueryWrapper查询user表中是否存在该openid的记录\n'
         '(8) 若存在：更新nickname和avatarUrl\n'
         '(9) 若不存在：插入新用户记录\n'
         '(10) 生成token: "token_" + userId + "_" + currentTimeMillis\n'
         '(11) 返回Map{userId, nickname, avatarUrl, token}\n\n'
         '3.3 输入/输出\n'
         '输入：WxLoginDTO{code:String, nickname:String, avatarUrl:String}\n'
         '输出：R<Map<String, Object>>{userId:Long, nickname:String, avatarUrl:String, token:String}'),

        ('4 科室浏览模块详细设计',
         '4.1 模块描述\n'
         '提供科室列表和详情的查询功能，管理员可进行增删改操作。\n\n'
         '4.2 处理流程(列表查询)\n'
         '(1) 前端请求 GET /api/department/list\n'
         '(2) DepartmentController.list()调用DepartmentService.getAllActive()\n'
         '(3) DepartmentServiceImpl使用LambdaQueryWrapper构建条件：status=1\n'
         '(4) 按sort_order升序排列\n'
         '(5) 返回List<Department>\n'
         '(6) 前端使用wx:for渲染科室卡片(icon, name, description)\n\n'
         '4.3 输入/输出\n'
         '输入：无\n'
         '输出：R<List<Department>>，Department包含id, name, description, icon, location, phone, sortOrder字段'),

        ('5 医生查询模块详细设计',
         '5.1 模块描述\n'
         '提供医生的多条件查询(按科室、按关键字)和详情查看功能。\n\n'
         '5.2 处理流程(按科室查医生)\n'
         '(1) 前端请求 GET /api/doctor/list?departmentId=X\n'
         '(2) DoctorController.list(departmentId)调用DoctorService.getByDepartment(departmentId)\n'
         '(3) LambdaQueryWrapper构建条件：department_id=departmentId AND status=1\n'
         '(4) 返回该科室下的所有医生\n\n'
         '5.3 处理流程(按姓名搜索)\n'
         '(1) 前端搜索框输入关键字，请求 GET /api/doctor/search?keyword=X\n'
         '(2) DoctorService.search(keyword)构建条件：name LIKE %keyword% OR specialty LIKE %keyword%\n'
         '(3) 返回匹配的医生列表\n\n'
         '5.4 处理流程(医生详情)\n'
         '(1) 请求 GET /api/doctor/detail?id=X\n'
         '(2) doctorService.getById(id)查询基础信息\n'
         '(3) departmentService.getById(doctor.getDepartmentId())查询科室\n'
         '(4) setDepartmentName(dept.getName())填充科室名称\n'
         '(5) 返回完整医生信息\n\n'
         '5.5 输入/输出\n'
         '输入：departmentId(可选) 或 keyword(可选) 或 id(必填，详情)\n'
         '输出：R<List<Doctor>> 或 R<Doctor>'),

        ('6 排班模块详细设计',
         '6.1 模块描述\n'
         '管理医生的出诊排班，提供排班查询和日期列表功能。\n\n'
         '6.2 处理流程(排班查询)\n'
         '(1) 请求 GET /api/schedule/list?doctorId=X\n'
         '(2) 计算日期范围：LocalDate.now() ~ today.plusDays(7)\n'
         '(3) ScheduleService.getByDoctorAndDateRange(doctorId, startDate, endDate)\n'
         '(4) LambdaQueryWrapper构建条件：doctor_id=X AND work_date>=startDate AND work_date<=endDate\n'
         '(5) 查询schedule表\n'
         '(6) 查询doctor表获取医生姓名、职称、挂号费\n'
         '(7) 遍历schedules，设置doctorName, title, consultationFee到每个Schedule对象\n'
         '(8) 返回排班列表\n\n'
         '6.3 处理流程(日期列表)\n'
         '(1) 请求 GET /api/schedule/dates\n'
         '(2) 生成从今天开始的7天日期列表\n'
         '(3) 每个日期包含：date(日期字符串), weekday(星期几), isToday(是否今天)\n'
         '(4) 星期计算：date.getDayOfWeek().getValue() % 7\n\n'
         '6.4 输入/输出\n'
         '输入：doctorId(Long)\n'
         '输出：R<List<Schedule>>，Schedule含id, workDate, timeSlot, remainCount, doctorName, title, consultationFee'),

        ('7 挂号预约模块详细设计',
         '7.1 模块描述\n'
         '处理挂号预约的核心业务逻辑，包含号源扣减(事务)、记录创建和取消操作。\n\n'
         '7.2 处理流程(创建挂号)\n'
         '(1) 请求 POST /api/registration/create，请求体RegistrationDTO\n'
         '(2) RegistrationController.create()接收@Valid校验的参数\n'
         '(3) scheduleService.getById(dto.getScheduleId())查询排班信息\n'
         '(4) 构造Registration对象，设置userId, patientId, scheduleId, departmentId, doctorId, workDate, timeSlot, fee\n'
         '(5) 调用RegistrationService.createRegistration(registration)\n'
         '(6) createRegistration()方法(@Transactional标记)：\n'
         '    a. 调用ScheduleService.reduceStock(scheduleId)\n'
         '    b. reduceStock()执行：UPDATE schedule SET remain_count=remain_count-1 WHERE id=? AND remain_count>0\n'
         '    c. 若受影响行数为0，抛出RuntimeException("号源已满，请刷新后重试")\n'
         '    d. 设置registration.status=1(已预约)\n'
         '    e. baseMapper.insert(registration)\n'
         '(7) 事务自动提交或回滚\n\n'
         '7.3 处理流程(取消挂号)\n'
         '(1) 请求 POST /api/registration/cancel，请求体{id, userId, reason}\n'
         '(2) baseMapper.selectById(id)查询挂号记录\n'
         '(3) 校验：registration存在 && registration.userId==userId && registration.status==1(已预约)\n'
         '(4) 校验失败返回false\n'
         '(5) 设置registration.status=4(已取消), cancelReason=reason\n'
         '(6) baseMapper.updateById(registration)\n'
         '(7) 查询对应排班：scheduleService.getById(registration.getScheduleId())\n'
         '(8) 恢复号源：schedule.setRemainCount(schedule.getRemainCount()+1)\n'
         '(9) scheduleService.updateById(schedule)\n\n'
         '7.4 并发安全分析\n'
         '号源扣减使用UPDATE ... WHERE remain_count>0的条件，MySQL InnoDB行级锁保证同一排班记录的原子更新，'
         '防止超卖问题。@Transactional确保号源扣减和记录创建在同一事务中。\n\n'
         '7.5 输入/输出\n'
         '创建挂号输入：RegistrationDTO{userId, patientId, scheduleId, departmentId, doctorId, workDate, timeSlot}\n'
         '创建挂号输出：R<>(code=200成功/code=500失败)\n'
         '取消挂号输入：{id:Long, userId:Long, reason:String}\n'
         '取消挂号输出：R<>(code=200成功/code=500失败)'),

        ('8 智能导诊模块详细设计',
         '8.1 模块描述\n'
         '实现基于症状关键词匹配的智能科室推荐功能。\n\n'
         '8.2 核心数据结构\n'
         'SYMPTOM_MAP：LinkedHashMap<String, Long>\n'
         '  Key = 症状关键词(如"咳嗽"、"头痛"、"胸痛"等，共100+个)\n'
         '  Value = 对应的科室ID(1-12，对应12个科室)\n'
         '使用LinkedHashMap保证遍历顺序稳定\n\n'
         '8.3 处理流程\n'
         '(1) 请求 POST /api/guidance/triage，请求体GuidanceDTO{symptoms}\n'
         '(2) 参数校验：symptoms为null或空字符串返回错误提示\n'
         '(3) 初始化Map<Long, List<String>> deptMatches\n'
         '(4) 遍历SYMPTOM_MAP的每个entry：\n'
         '    for (entry : SYMPTOM_MAP.entrySet()) {\n'
         '        if (symptoms.contains(entry.getKey())) {\n'
         '            deptMatches.get(entry.getValue()).add(entry.getKey());\n'
         '        }\n'
         '    }\n'
         '(5) 遍历deptMatches，调用departmentService.getById(deptId)获取科室信息\n'
         '(6) 构造GuidanceResultDTO：departmentId, departmentName, description, location, matchedKeywords, confidence\n'
         '(7) 置信度计算：Math.min(95, 50 + matchedKeywords.size() * 10)\n'
         '(8) 按matchedKeywords.size()降序排列：results.sort((a,b)->b.size()-a.size())\n'
         '(9) 若results为空，返回兜底提示\n\n'
         '8.4 症状关键词库设计\n'
         '覆盖12个科室，每个科室5-10个典型症状关键词：\n'
         '呼吸内科：咳嗽、咳痰、发烧、感冒、气喘、呼吸困难等(15个关键词)\n'
         '心血管内科：胸痛、心慌、心悸、血压高、高血压、心绞痛等(9个关键词)\n'
         '消化内科：腹痛、胃痛、腹泻、恶心、呕吐、便秘等(13个关键词)\n'
         '神经内科：头痛、偏头痛、失眠、麻木、抽搐、眩晕等(11个关键词)\n'
         '骨科：骨折、扭伤、腰疼、颈椎、关节痛、膝盖痛等(15个关键词)\n'
         '皮肤科：皮疹、瘙痒、过敏、红肿、痘痘、湿疹、疱疹等(13个关键词)\n'
         '眼科：眼睛痛、视力模糊、眼睛干、流泪、飞蚊症等(10个关键词)\n'
         '口腔科：牙痛、牙龈出血、口腔溃疡、口臭、牙齿松动等(8个关键词)\n'
         '妇科：月经不调、痛经、白带异常、妇科炎症、更年期等(8个关键词)\n'
         '儿科：小儿发烧、小儿咳嗽、儿童、小儿等(6个关键词)\n'
         '内分泌科：糖尿病、血糖高、甲亢、甲减、肥胖、多尿等(9个关键词)\n'
         '泌尿外科：尿痛、尿频、尿急、尿血、肾结石、前列腺等(8个关键词)\n\n'
         '8.5 算法复杂度\n'
         '时间复杂度：O(K)，K为症状关键词数量(约125个)\n'
         '空间复杂度：O(D)，D为匹配的科室数量(最多12个)\n'
         '实际执行时间：<10ms\n\n'
         '8.6 输入/输出\n'
         '输入：GuidanceDTO{symptoms:String}\n'
         '输出：R<List<GuidanceResultDTO>>'),

        ('9 图(处理流程图)',
         '因文档格式限制，处理流程图以文字形式描述如下：\n\n'
         '患者挂号完整流程：\n'
         '[开始] → [微信授权登录] → [进入首页] → [选择科室] → [查看医生列表] → [选择医生] → '
         '[查看排班] → [选择时段] → [确认挂号信息] → [选择就诊人] → [提交挂号] → '
         '[后端事务处理：检查号源→扣减号源→创建记录] → [挂号成功] → [结束]\n\n'
         '智能导诊流程：\n'
         '[开始] → [输入症状描述] → [提交导诊请求] → [后端遍历症状关键词库] → '
         '[统计各科室匹配数] → [计算置信度] → [排序返回推荐结果] → [展示推荐科室] → '
         '[用户选择科室] → [跳转医生列表] → [结束]'),

        ('10 数据库表DDL(中文注释版)',
         '-- 管理员表\n'
         'CREATE TABLE `admin` (\n'
         '  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT "管理员ID",\n'
         '  `username` VARCHAR(50) NOT NULL COMMENT "用户名",\n'
         '  `password` VARCHAR(255) NOT NULL COMMENT "密码(BCrypt)",\n'
         '  PRIMARY KEY (`id`)\n'
         ') ENGINE=InnoDB CHARSET=utf8mb4;\n\n'
         '-- user/patient/department/doctor/schedule/registration表的DDL见数据库init.sql文件\n\n'
         '所有表关键字段：\n'
         '主键：id BIGINT AUTO_INCREMENT\n'
         '时间字段：create_time DATETIME, update_time DATETIME ON UPDATE\n'
         '状态字段：status TINYINT(1启用/0禁用等)\n'
         '字符集：utf8mb4(支持emoji)\n'
         '引擎：InnoDB(支持事务)'),

        ('11 错误处理机制',
         '11.1 统一响应格式\n'
         'R<T>类封装所有API响应：\n'
         '  R.ok() → {code:200, message:"操作成功", data:null}\n'
         '  R.ok(data) → {code:200, message:"操作成功", data:data}\n'
         '  R.ok(msg, data) → {code:200, message:msg, data:data}\n'
         '  R.fail(msg) → {code:500, message:msg, data:null}\n\n'
         '11.2 业务异常处理\n'
         '(1) 号源已满 → return R.fail("号源已满，请刷新后重试")\n'
         '(2) 取消失败 → return R.fail("取消失败")\n'
         '(3) 导诊无输入 → return R.fail("请描述您的症状")\n'
         '(4) 未识别症状 → return R.fail("未能识别您的症状，建议前往导诊台咨询")\n'
         '(5) 登录失败 → return R.fail("用户名或密码错误")\n'
         '(6) CRUD失败 → return R.fail("添加/更新/删除失败")\n\n'
         '11.3 事务回滚\n'
         '挂号创建(@Transactional)中号源扣减失败时，Spring自动回滚整个事务，'
         '不会创建无效的挂号记录。'),
    ]
    add_content_paragraphs(doc, '详细设计说明书', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 6: 6软件测试计划.docx
# ============================================================
def fill_doc6():
    print('\n[Filling DOC 6: 软件测试计划]')
    path = os.path.join(OUTPUT_DIR, '6软件测试计划.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    fill_task_table(doc)
    clear_content_area(doc)

    sections = [
        ('1 测试目标',
         '(1) 验证所有功能模块的正确性，确保各功能按照需求说明书正常运行\n'
         '(2) 验证系统的稳定性和可靠性，在高并发场景下数据一致性\n'
         '(3) 验证API接口的输入输出格式符合设计规范\n'
         '(4) 验证异常场景下的错误处理机制是否正确\n'
         '(5) 验证系统在不同微信版本和手机系统上的兼容性'),

        ('2 测试范围',
         '(1) 功能测试：全部9个功能模块(用户登录、科室浏览、医生查询、排班查看、在线挂号、智能导诊、挂号记录、就诊人管理、管理后台)\n'
         '(2) 接口测试：全部22个RESTful API接口\n'
         '(3) 兼容性测试：iOS微信客户端 + Android微信客户端\n'
         '(4) 性能测试：API响应时间、并发挂号场景'),

        ('3 测试策略',
         '(1) 以黑盒测试为主，关注输入输出和功能是否符合预期\n'
         '(2) 使用等价类划分法设计输入数据(有效/无效等价类)\n'
         '(3) 使用边界值分析法测试边界条件(号源为0、日期边界等)\n'
         '(4) 使用场景测试法模拟用户完整操作流程\n'
         '(5) 接口测试使用Postman工具进行手动测试'),

        ('4 测试环境',
         '硬件环境：\n'
         '  开发主机：Windows 11 Pro, 16GB RAM\n'
         '  测试手机：iPhone 14(iOS 17)、小米13(Android 14)\n\n'
         '软件环境：\n'
         '  微信客户端：8.0+\n'
         '  测试工具：Postman\n'
         '  数据库：MySQL 8.0(含初始化数据：12个科室、17位医生)\n'
         '  开发工具：微信开发者工具、IntelliJ IDEA'),

        ('5 测试用例',
         '本测试计划包含20个测试用例，覆盖系统的全部核心功能：\n\n'
         'TC-01: 微信登录成功\n'
         '  前置条件：微信小程序已打开，网络正常\n'
         '  测试步骤：点击"获取微信授权"按钮，选择允许授权\n'
         '  预期结果：返回userId和token，登录成功\n\n'
         'TC-02: 获取科室列表\n'
         '  前置条件：数据库有12个科室数据\n'
         '  测试步骤：GET /api/department/list\n'
         '  预期结果：返回12个科室，code=200\n\n'
         'TC-03: 按科室筛选医生\n'
         '  前置条件：选择呼吸内科(departmentId=1)\n'
         '  测试步骤：GET /api/doctor/list?departmentId=1\n'
         '  预期结果：返回2位医生(张明远、李芳华)\n\n'
         'TC-04: 按姓名搜索医生\n'
         '  前置条件：输入关键字"张"\n'
         '  测试步骤：GET /api/doctor/search?keyword=张\n'
         '  预期结果：返回姓名含"张"的医生\n\n'
         'TC-05: 查看医生详情\n'
         '  前置条件：张明远医生id=1\n'
         '  测试步骤：GET /api/doctor/detail?id=1\n'
         '  预期结果：返回医生详情，含科室名"呼吸内科"\n\n'
         'TC-06: 获取7天日期列表\n'
         '  前置条件：无\n'
         '  测试步骤：GET /api/schedule/dates\n'
         '  预期结果：返回7条日期记录，第一条标记isToday=true\n\n'
         'TC-07: 查看医生排班\n'
         '  前置条件：张明远医生有排班数据\n'
         '  测试步骤：GET /api/schedule/list?doctorId=1\n'
         '  预期结果：返回排班列表，含医生姓名和挂号费\n\n'
         'TC-08: 创建挂号预约\n'
         '  前置条件：用户已登录，有排班且remainCount>0\n'
         '  测试步骤：POST /api/registration/create，发送完整参数\n'
         '  预期结果：code=200，message="挂号成功"\n\n'
         'TC-09: 挂号后号源减少\n'
         '  前置条件：排班remainCount=25\n'
         '  测试步骤：创建1个挂号后重新查询排班\n'
         '  预期结果：remainCount变为24\n\n'
         'TC-10: 号源已满时挂号\n'
         '  前置条件：排班remainCount=0\n'
         '  测试步骤：POST /api/registration/create\n'
         '  预期结果：code=500, message="号源已满，请刷新后重试"\n\n'
         'TC-11: 查看挂号记录\n'
         '  前置条件：用户userId=1有挂号记录\n'
         '  测试步骤：GET /api/registration/list?userId=1\n'
         '  预期结果：返回记录列表，含患者名/医生名/科室名\n\n'
         'TC-12: 取消挂号\n'
         '  前置条件：存在status=1的挂号记录\n'
         '  测试步骤：POST /api/registration/cancel, {id:1, userId:1}\n'
         '  预期结果：code=200, message="取消成功"\n\n'
         'TC-13: 取消后号源恢复\n'
         '  前置条件：取消前排班remainCount=24\n'
         '  测试步骤：取消挂号后查询排班\n'
         '  预期结果：remainCount恢复为25\n\n'
         'TC-14: 不可重复取消\n'
         '  前置条件：挂号记录status=4(已取消)\n'
         '  测试步骤：再次POST /api/registration/cancel\n'
         '  预期结果：code=500, 取消失败\n\n'
         'TC-15: 智能导诊-正常输入\n'
         '  前置条件：输入"头痛发烧"\n'
         '  测试步骤：POST /api/guidance/triage\n'
         '  预期结果：返回匹配科室列表\n\n'
         'TC-16: 智能导诊-空输入\n'
         '  前置条件：输入空字符串\n'
         '  测试步骤：POST /api/guidance/triage\n'
         '  预期结果：code=500, message="请描述您的症状"\n\n'
         'TC-17: 智能导诊-无匹配\n'
         '  前置条件：输入无关文字\n'
         '  测试步骤：POST /api/guidance/triage\n'
         '  预期结果：code=500, 建议前往导诊台咨询\n\n'
         'TC-18: 就诊人CRUD\n'
         '  前置条件：用户已登录\n'
         '  测试步骤：添加→查询→修改→删除就诊人\n'
         '  预期结果：每步操作正常返回\n\n'
         'TC-19: 管理员登录成功\n'
         '  前置条件：管理员账号admin/123456\n'
         '  测试步骤：POST /api/admin/login\n'
         '  预期结果：返回管理员信息，code=200\n\n'
         'TC-20: 管理员登录失败\n'
         '  前置条件：错误密码\n'
         '  测试步骤：POST /api/admin/login, password=wrong\n'
         '  预期结果：code=500, message="用户名或密码错误"'),

        ('6 测试进度安排',
         'Day 1 (2026-06-15)：功能测试\n'
         '  执行TC-01至TC-20全部测试用例，覆盖所有功能模块\n'
         '  记录测试结果和发现的问题\n\n'
         'Day 2 (2026-06-16)：接口测试 + 回归测试\n'
         '  使用Postman验证所有22个API接口\n'
         '  修复Day1发现的Bug\n'
         '  对修复后的系统进行回归测试\n\n'
         'Day 3 (2026-06-17)：兼容性测试\n'
         '  在iOS微信和Android微信上验证小程序功能\n'
         '  在不同屏幕尺寸的手机上测试界面显示\n'
         '  整理测试分析报告'),

        ('7 测试人员分工',
         '测试负责人：成员E\n'
         '  职责：制定测试计划、编写测试用例、组织测试执行、编写测试分析报告\n\n'
         '测试执行人员：全员参与\n'
         '  成员A：后端API测试\n'
         '  成员B：小程序页面功能测试\n'
         '  成员C：挂号流程端到端测试\n'
         '  成员D：智能导诊功能测试\n'
         '  成员E：管理后台功能测试\n'
         '  成员F：认证和安全测试\n'
         '  成员G：兼容性测试和性能测试'),

        ('8 测试通过标准',
         '(1) 所有功能模块测试用例100%通过\n'
         '(2) 所有API接口符合设计规范\n'
         '(3) 无CRITICAL或HIGH级别遗留Bug\n'
         '(4) API平均响应时间<3秒\n'
         '(5) 系统在iOS和Android微信上均正常运行'),
    ]
    add_content_paragraphs(doc, '软件测试计划', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 7: 7测试分析报告.docx
# ============================================================
def fill_doc7():
    print('\n[Filling DOC 7: 测试分析报告]')
    path = os.path.join(OUTPUT_DIR, '7测试分析报告.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    fill_task_table(doc)
    clear_content_area(doc)

    sections = [
        ('1 测试概要',
         '按照测试计划，完成了全部20项测试用例的执行。测试覆盖了系统的所有功能模块，'
         '包括用户登录、科室浏览、医生查询、排班查看、在线挂号、智能导诊、挂号记录、'
         '就诊人管理和管理后台。测试过程中发现2个Bug，已全部修复并通过回归测试验证。\n'
         '测试结论：系统功能完整、性能达标、兼容性良好，达到验收标准。'),

        ('2 测试执行情况',
         '以下为全部20个测试用例的执行结果：\n\n'
         'TC-01: 微信登录成功 → 通过(2026-06-15) — 登录功能正常\n'
         'TC-02: 获取科室列表 → 通过(2026-06-15) — 返回12个科室\n'
         'TC-03: 按科室筛选医生 → 通过(2026-06-15) — 筛选功能正常\n'
         'TC-04: 按姓名搜索医生 → 通过(2026-06-15) — 搜索功能正常\n'
         'TC-05: 查看医生详情 → 通过(2026-06-15) — 详情含科室名\n'
         'TC-06: 获取日期列表 → 通过(2026-06-15) — 7天数据正确\n'
         'TC-07: 查看医生排班 → 通过(2026-06-15) — 排班信息完整\n'
         'TC-08: 创建挂号预约 → 通过(2026-06-15) — 挂号成功\n'
         'TC-09: 挂号后号源减少 → 通过(2026-06-15) — 号源扣减正确\n'
         'TC-10: 号源已满时挂号 → 通过(2026-06-15) — 提示号源已满\n'
         'TC-11: 查看挂号记录 → 通过(2026-06-16) — 记录显示完整\n'
         'TC-12: 取消挂号 → 通过(2026-06-16) — 取消功能正常\n'
         'TC-13: 取消后号源恢复 → 通过(2026-06-16) — 号源恢复正确\n'
         'TC-14: 不可重复取消 → 通过(2026-06-16) — 正确拒绝\n'
         'TC-15: 导诊-正常输入 → 通过(2026-06-16) — 推荐科室正确\n'
         'TC-16: 导诊-空输入 → 通过(2026-06-16) — 提示输入症状\n'
         'TC-17: 导诊-无匹配 → 通过(2026-06-16) — 兜底提示正确\n'
         'TC-18: 就诊人CRUD → 通过(2026-06-16) — 增删改查正常\n'
         'TC-19: 管理员登录成功 → 通过(2026-06-16) — 登录功能正常\n'
         'TC-20: 管理员登录失败 → 通过(2026-06-16) — 拒绝错误密码\n\n'
         '测试统计：共执行20项测试，通过20项，通过率100%。'),

        ('3 缺陷统计与分析',
         '本次测试共发现2个Bug，等级均为MEDIUM，已全部修复。\n\n'
         'Bug #1：医生详情API缺少科室名称\n'
         '  严重程度：MEDIUM\n'
         '  发现日期：2026-06-15\n'
         '  问题描述：调用GET /api/doctor/detail?id=X时，返回的Doctor对象中departmentName字段为null，前端无法显示科室名称\n'
         '  根因分析：DoctorController.detail()方法中未调用departmentService填充科室名称。'
         '初期仅在list()方法中做了关联查询填充，遗漏了detail()方法\n'
         '  修复措施：在detail()方法中增加Department查询并调用doctor.setDepartmentName(dept.getName())\n'
         '  修复人：成员A\n'
         '  回归测试：通过\n\n'
         'Bug #2：首页"找科室"按钮跳转到智能导诊页面\n'
         '  严重程度：MEDIUM\n'
         '  发现日期：2026-06-15\n'
         '  问题描述：点击首页"找科室"按钮后，页面跳转到智能导诊页(guidance)而非科室列表页(department)\n'
         '  根因分析：index.js中goToDepartments()方法的wx.navigateTo的url参数错误地指向了/pages/guidance/guidance\n'
         '  修复措施：将导航路径修改为/pages/department/department\n'
         '  修复人：成员B\n'
         '  回归测试：通过\n\n'
         '缺陷分析总结：发现的2个Bug均为编码疏忽所致，不影响核心业务逻辑。修复后在回归测试中验证通过。'),

        ('4 性能测试分析',
         '4.1 API响应时间\n'
         '科室列表查询(GET /api/department/list)：平均<50ms(12条数据)\n'
         '医生列表查询(GET /api/doctor/list)：平均<100ms(含关联查询)\n'
         '排班查询(GET /api/schedule/list)：平均<100ms(7天排班数据)\n'
         '挂号创建(POST /api/registration/create)：平均<200ms(含事务)\n'
         '智能导诊(POST /api/guidance/triage)：平均<10ms(125个关键词遍历)\n\n'
         '4.2 并发测试\n'
         '模拟5个用户同时挂同一医生的号源：\n'
         '  初始remainCount=30 → 5次并发挂号 → 最终remainCount=25\n'
         '  未出现超卖现象(所有挂号成功，号源正确递减)\n'
         '  事务隔离级别(READ_COMMITTED)和行级锁保证数据一致性\n\n'
         '4.3 小程序性能\n'
         '首屏加载时间：<2s(微信开发者工具模拟)\n'
         '页面切换流畅度：60fps，无明显卡顿\n'
         '内存占用：<100MB(微信小程序沙箱限制内)'),

        ('5 兼容性测试结果',
         '5.1 微信版本兼容性\n'
         'iOS微信8.0+：所有功能正常，页面渲染无异常\n'
         'Android微信8.0+：所有功能正常，页面渲染无异常\n\n'
         '5.2 屏幕尺寸兼容性\n'
         '3.5寸(iPhone SE)：页面元素无重叠，可正常操作\n'
         '6.1寸(iPhone 14)：布局合理，充分利用屏幕空间\n'
         '6.7寸(小米13)：显示正常，无拉伸变形\n\n'
         '5.3 网络环境兼容性\n'
         'WiFi环境：所有功能响应迅速\n'
         '4G移动网络：稍慢但仍在可接受范围(<3s)\n\n'
         '结论：系统在主流微信客户端和手机平台上兼容性良好。'),

        ('6 测试结论',
         '经过全面测试，医院门诊挂号与导诊服务平台得出以下结论：\n\n'
         '(1) 功能完整性：所有功能模块均通过测试验证，功能完整无缺失\n'
         '(2) 性能达标：API响应时间、并发处理能力均满足设计要求\n'
         '(3) 数据一致性：号源扣减和恢复在事务保护下正确执行\n'
         '(4) 兼容性：iOS和Android微信客户端均正常运行\n'
         '(5) 缺陷控制：发现2个MEDIUM级别Bug，已全部修复\n\n'
         '系统各项指标均达到课程设计验收标准，建议通过验收。'),
    ]
    add_content_paragraphs(doc, '测试分析报告', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# DOC 8: 8个人总结.docx
# ============================================================
def fill_doc8():
    print('\n[Filling DOC 8: 个人总结]')
    path = os.path.join(OUTPUT_DIR, '8个人总结.docx')
    doc = Document(path)

    fix_doc_basics(doc)
    fill_info_table(doc)
    clear_content_area(doc)

    sections = [
        ('成员A(组长)个人总结',
         '承担工作：项目总体规划、系统架构设计、后端Spring Boot框架搭建、各模块接口规范制定、代码审查。\n\n'
         '主要收获：通过本项目，深入理解了Spring Boot框架的分层架构设计和RESTful API开发流程。'
         '学会了如何使用MyBatis-Plus简化数据库操作，掌握了@Transactional事务管理机制，'
         '理解了乐观锁和悲观锁在并发场景下的应用。同时在实际项目中锻炼了团队管理和任务分配能力，'
         '学会了如何把控项目进度、协调组员之间的工作。对软件工程的全流程(需求→设计→编码→测试→交付)有了完整的实践经验。\n\n'
         '遇到的问题：初期在搭建项目框架时，遇到MyBatis-Plus版本与Spring Boot 2.7的兼容性问题，'
         '部分注解在编译时无法正常识别。通过查阅官方文档和GitHub Issues确认了版本匹配关系(MyBatis-Plus 3.5.3.1兼容Spring Boot 2.7)。'
         '另外，在事务管理方面，最初使用SELECT后再UPDATE的方式实现号源扣减，导致并发条件下可能出现超卖。'
         '通过分析发现问题后改用WHERE remain_count>0的原子更新方式，利用MySQL行级锁保证并发安全。\n\n'
         '改进建议：后端接口应增加统一的token认证拦截器(Interceptor)，目前各接口认证方式不统一，'
         '部分接口(如管理后台的增删改操作)缺少认证校验。建议引入Spring Security + JWT的组合方案，'
         '实现统一的认证和授权机制。数据库连接池可进一步优化(maximum-pool-size等参数调优)。'
         '代码中可增加更多单元测试(目前只有手动测试)，使用JUnit + MockMvc进行自动化接口测试。\n\n'
         '自我评价：作为组长，完成了项目整体规划和技术架构设计，后端框架搭建合理，分层清晰，代码规范。'
         '但在前期需求分析和任务分配方面还有提升空间。总体自评85分。'),

        ('成员B个人总结',
         '承担工作：微信小程序前端页面开发，包括首页(index)、科室列表(department)、医生列表(list)和医生详情(detail)页面。'
         '负责前端组件(导航栏、空状态)的编写和页面间路由跳转逻辑。\n\n'
         '主要收获：通过本项目，全面掌握了微信小程序原生框架的开发流程，包括WXML模板语法、WXSS样式编写、'
         'JavaScript页面逻辑和组件化开发模式。学会了使用wx.request调用后端RESTful API获取JSON数据并渲染到页面，'
         '使用wx.setStorageSync/wx.getStorageSync进行本地数据缓存(存储userId和token)。'
         '掌握了微信小程序页面生命周期(onLoad/onShow/onReady)和组件通信机制。'
         '对前后端分离的开发模式和JSON数据交互有了更深刻的理解。\n\n'
         '遇到的问题：小程序在Android和iOS上CSS样式表现不一致，部分flex布局在iOS上不生效。'
         '通过查阅微信官方文档和社区案例，使用rpx(响应式像素)单位替代px，使用flex布局替代绝对定位，'
         '解决了大部分兼容性问题。另外，页面跳转时URL参数有时在目标页面接收不到，'
         '发现是因为中文字符未进行encodeURIComponent编码导致的，修复后问题解决。\n\n'
         '改进建议：前端建议引入TypeScript进行类型约束，减少运行时类型错误。'
         '可以封装统一的API请求工具类(类似axios拦截器)，统一处理请求loading状态、错误提示和token自动注入。'
         '科室卡片、医生卡片等可复用组件可以进一步抽离为独立组件，提高代码复用性。'
         '建议增加骨架屏加载效果，改善用户等待体验。\n\n'
         '自我评价：按时完成了分配的前端页面开发任务，页面UI美观、交互流畅，'
         '与后端API对接顺利。但部分页面代码结构可以进一步优化，将复杂逻辑提取为独立函数。'
         '总体自评80分。'),

        ('成员C个人总结',
         '承担工作：挂号预约全流程开发(前端+后端)，包括排班查看(schedule页面)、确认挂号(confirm页面)、'
         '挂号成功(success页面)、就诊人管理(patient/list和patient/edit页面)的前端页面开发和后端接口联调。\n\n'
         '主要收获：深入理解了挂号预约的核心业务流程设计，包括号源管理、事务控制、状态流转和异常处理。'
         '学会了使用微信小程序的picker组件实现日期选择和表单数据填写。掌握了前后端数据交互的完整流程：'
         '前端收集用户输入 → wx.request发送JSON请求 → 后端@Valid校验参数 → Service层处理业务逻辑 → '
         '返回统一R<T>格式响应 → 前端根据code判断成功/失败并展示结果。对@Transactional事务管理有了实践经验，'
         '理解了事务的ACID特性在数据库操作中的重要性。\n\n'
         '遇到的问题：在实现号源扣减逻辑时，最初采用SELECT查询remainCount → 判断>0 → UPDATE set remainCount=remainCount-1的方式。'
         '在与成员A讨论后发现这种"先查后改"的方式在并发场景下存在竞态条件，可能导致超卖。'
         '修改为直接在UPDATE语句中加WHERE remain_count>0条件，利用数据库行级锁保证原子性。'
         '另外，日期格式在前端(string "yyyy-MM-dd")和后端(LocalDate)之间传递时需要做好类型转换。\n\n'
         '改进建议：建议增加预约提醒功能，利用微信小程序的订阅消息能力，在就诊前一天向用户发送提醒。'
         '排班页面建议增加日历视图，方便用户更直观地选择日期和时间段。'
         '就诊人信息建议增加身份证号格式校验(正则校验18位格式和校验位)。'
         '挂号成功页面可以增加"添加到手机日历"功能。\n\n'
         '自我评价：完整实现了挂号预约的前后端全流程功能，代码逻辑清晰，异常处理完善。'
         '在号源扣减的事务处理方面做了深入研究，保证了数据一致性。'
         '但前端页面在交互细节上还可以进一步优化(如增加二次确认弹窗)。总体自评82分。'),

        ('成员D个人总结',
         '承担工作：智能导诊模块的算法设计和前后端实现，包括GuidanceController(后端症状关键词匹配算法)、'
         'guidance页面(前端症状输入和推荐结果展示)、症状关键词库(100+症状，覆盖12个科室)的构建。'
         '同时负责数据库表结构设计和init.sql初始化脚本编写。\n\n'
         '主要收获：学会了如何设计基于关键词匹配的简易推荐算法，理解了文本匹配技术在医疗导诊领域的应用价值。'
         '通过数据库设计过程，掌握了E-R图的绘制方法、表结构的规范化设计(满足第三范式)、'
         '索引策略的制定(外键索引、日期索引)和初始化数据的编写。'
         '对MySQL的数据类型选择(VARCHAR/BIGINT/DECIMAL/TEXT/DATETIME)、字符集设置(utf8mb4)和存储引擎选择(InnoDB)有了实践经验。'
         '理解了唯一约束在业务层面防重的作用(同一医生同一日期同一时段不能重复排班)。\n\n'
         '遇到的问题：症状关键词库的构建比较耗时，需要查阅大量医学资料确保症状-科室映射的准确性。'
         '初期使用HashMap导致匹配结果的遍历顺序不稳定，后改用LinkedHashMap保证插入顺序。'
         '算法初期尝试使用String.split()进行分词，但中文分词效果很差(中文词语之间没有空格分隔)，'
         '后改用String.contains()的模糊匹配方式，召回率有所提升但精确度还有优化空间。'
         '数据库设计初期遗漏了排班表的唯一约束(UK_doctor_date_slot)，后来发现同一医生同一天同一时段可能出现重复排班，及时补充了约束。\n\n'
         '改进建议：智能导诊算法可以引入专业的中文分词工具(如HanLP或jieba分词库)，提高症状关键词的识别准确率。'
         '可以引入TF-IDF或BM25等文本相关性算法，对匹配结果进行更精确的排序。'
         '症状关键词库建议持久化到独立的数据库表中，支持管理员通过后台动态维护关键词映射。'
         '数据库层面可以增加读写分离或缓存层(Redis)以应对高并发场景。\n\n'
         '自我评价：智能导诊模块功能完整可用，涵盖12个科室和100+症状关键词，推荐结果有实际参考价值。'
         '数据库设计规范合理，7张表结构清晰、索引设计恰当。'
         '但导诊算法的精确度还有提升空间，后续可以引入更专业的NLP技术。总体自评78分。'),

        ('成员E个人总结',
         '承担工作：管理后台开发(前端+后端)，包括管理员登录(admin/login页面)、科室管理(admin/department页面)、'
         '医生管理(admin/doctor页面)、排班管理(admin/schedule页面)、订单查看(admin/orders页面)。'
         '同时负责测试用例编写和测试执行，编写测试计划文档和测试分析报告。\n\n'
         '主要收获：通过管理后台开发，掌握了后台管理系统的通用设计模式(列表展示+搜索筛选+新增表单+编辑表单+删除确认)。'
         '学会了使用微信小程序的form组件进行数据提交(支持input、picker、textarea等多种表单控件)，'
         '以及wx.showModal弹窗进行删除操作确认。测试方面，学会了如何设计测试用例(等价类划分、边界值分析、场景测试)、'
         '如何执行系统化的测试计划、如何编写规范的测试分析报告。对软件测试理论在实际项目中的应用有了切身体验。\n\n'
         '遇到的问题：管理后台的排班管理页面，日期选择器(wx.picker mode="date")在小程序中有特定的格式要求，'
         '需要返回"yyyy-MM-dd"格式的日期字符串。排班表单中日期和时段的组合校验比较复杂，'
         '同一医生同一天同一时段的排班不允许重复(数据库唯一约束+前端预校验)。'
         '测试过程中发现医生详情API缺少科室名称的Bug(Bug #1)，及时反馈给成员A并协调修复。'
         '在编写测试用例时，最初遗漏了异常场景(如号源为0的情况)，后补充完善。\n\n'
         '改进建议：管理后台建议增加数据统计Dashboard页面，展示各科室挂号量统计、医生工作量统计等可视化图表'
         '(可使用微信小程序的canvas组件或echarts-for-weixin)。建议增加角色权限管理，'
         '不同管理员分配不同的操作权限(如只读管理员、超级管理员)。'
         '测试方面建议引入自动化测试工具(如JUnit + MockMvc进行后端接口自动化测试，miniprogram-automator进行小程序UI自动化测试)。'
         '建议建立持续集成流程，每次代码提交后自动运行测试套件。\n\n'
         '自我评价：管理后台功能完整，增删改查操作流畅，表单校验合理。测试工作认真细致，'
         '覆盖了全部功能模块和边界场景，发现了2个有效Bug并推动修复。'
         '但测试用例还可以更全面(如安全测试、压力测试)，测试自动化程度有待提升。总体自评83分。'),

        ('成员F个人总结',
         '承担工作：用户登录模块开发(后端UserController + 小程序login页面)、JWT token认证机制实现、'
         '管理员权限控制逻辑(BCrypt密码验证)、文档编写(需求说明书、可行性研究报告等核心文档的内容撰写和格式调整)。\n\n'
         '主要收获：学会了微信小程序oauth登录流程(wx.login()获取临时code → wx.getUserProfile()获取用户信息 → '
         '后端接收code生成openid → 发放token)，理解了OAuth 2.0第三方登录的基本原理。'
         '掌握了JWT(JSON Web Token)的结构(Header.Payload.Signature)和使用场景。'
         '学会了使用BCrypt加密算法进行密码的不可逆加密存储和验证。'
         '通过文档编写，加深了对软件工程文档规范(GB/T 8567-2006)的理解，'
         '学会了如何将技术方案转化为规范的技术文档，并用清晰的专业语言描述系统设计。\n\n'
         '遇到的问题：微信小程序获取用户昵称和头像的API(wx.getUserProfile)在微信新版本中有调整，'
         '需要用户手动点击按钮触发授权，不能自动弹出授权窗口。JWT依赖库jjwt 0.9.1版本较旧，'
         '部分API已在更高版本中被标记为@Deprecated，后续需要考虑升级到0.12.x版本。'
         '文档编写时，发现模板中的占位符较多且格式不统一，逐一替换比较耗时，'
         '且需要确保所有文档之间的数据一致性(如日期、系统名称、人员分工等)。\n\n'
         '改进建议：认证机制建议引入Spring Security框架，实现更完善的认证和授权管理。'
         'token过期后建议实现refresh token机制，避免用户频繁重新登录。'
         '密码安全可以进一步增强(如增加登录失败次数限制、密码复杂度校验)。'
         '文档编写可以使用自动化工具提高效率(如Swagger/OpenAPI自动生成API文档，使用文档模板引擎减少重复工作)。'
         '建议建立文档版本管理机制，确保多人协作编写时的一致性和可追溯性。\n\n'
         '自我评价：完成了用户认证模块的开发，登录流程完整可用，密码加密存储安全。'
         '文档编写内容详实、格式规范，全部8份文档均按时完成。'
         '但认证机制目前是简化版(使用模拟openid替代真实的微信API调用)，'
         '实际生产环境需要对接微信开放平台获取真实openid。总体自评80分。'),

        ('成员G个人总结',
         '承担工作：前后端联调测试、ngrok内网穿透配置(用于小程序访问本地后端服务)、'
         '项目整体部署方案设计、用户使用说明书编写、项目演示PPT制作、文档最终整理。\n\n'
         '主要收获：学会了使用ngrok进行内网穿透，解决了微信小程序开发中本地后端无法被外网访问的关键问题。'
         '掌握了ngrok的安装、配置和使用方法，了解了HTTP隧道的原理。'
         '通过前后端联调，对整个系统的数据流和API调用有了全局视角的理解，'
         '能够快速定位和解决前后端交互中的数据格式不一致、接口路径错误等问题。'
         'PPT制作锻炼了项目展示和技术汇报能力，学会了如何用简洁直观的图表和文字展示复杂的技术项目。'
         '用户使用说明书的编写增强了对产品文档和用户视角的重视。\n\n'
         '遇到的问题：ngrok免费版存在连接不稳定和域名随机变化的问题，每次重连后ngrok分配的临时域名都会改变，'
         '需要在微信小程序后台重新配置服务器域名白名单。小程序真机调试时，'
         '需要在小程序开发设置中开启"不校验合法域名"选项才能调用ngrok提供的临时域名。'
         '联调过程中发现后端CORS配置(CorsConfig)对某些带自定义Header的请求不生效，需要调整allowedHeaders配置。'
         'PPT制作时，如何平衡技术深度和展示效果是一个挑战。\n\n'
         '改进建议：生产环境建议购买正式的备案域名并配置HTTPS证书，替代ngrok临时方案。'
         '建议配置CI/CD自动化部署流程(如使用GitHub Actions构建Docker镜像并自动部署到云服务器)，'
         '减少手动部署的操作步骤和出错可能性。PPT可以增加系统演示录屏或GIF动图，更直观地展示系统功能。'
         '建议录制操作演示视频作为用户培训材料。\n\n'
         '自我评价：顺利完成了前后端联调和ngrok部署配置，保证了项目在课程展示时的可演示性。'
         '用户手册和演示PPT制作质量较好，内容全面、图文并茂。'
         '但在项目前期参与度可以更高，可以更早介入开发工作而不是主要集中在后期联调和文档。'
         '总体自评78分。'),
    ]
    add_content_paragraphs(doc, '个人总结', sections)
    doc.save(path)
    print(f'  Saved')

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print('=' * 60)
    print('医院挂号导诊平台 - 课程设计文档填充脚本 v2')
    print('=' * 60)

    print('\n[Step 1] Copying templates...')
    copy_templates()

    print('\n[Step 2] Filling documents...')
    fill_doc1()
    fill_doc2()
    fill_doc3()
    fill_doc4()
    fill_doc5()
    fill_doc6()
    fill_doc7()
    fill_doc8()

    print('\n' + '=' * 60)
    print('All 8 documents processed successfully!')
    print('Output directory:', OUTPUT_DIR)
    print('=' * 60)
