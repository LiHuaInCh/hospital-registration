package com.hospital.service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 症状关键词 -> 科室的匹配引擎。
 *
 * 说明：这里只做纯文本匹配，不涉及数据库；科室用名称标识，
 * 因此新增/删除科室时不需要改动代码。一个关键词可以指向多个科室
 * （例如「腰痛」同时属于骨科与泌尿外科）。
 */
public final class TriageEngine {

    /**
     * 一条症状规则：关键词 + 可能对应的科室。
     */
    private static final List<Rule> RULES = Arrays.asList(
            // 呼吸内科
            new Rule("咳嗽", "呼吸内科"),
            new Rule("咳痰", "呼吸内科"),
            new Rule("发烧", "呼吸内科", "儿科"),
            new Rule("发热", "呼吸内科", "儿科"),
            new Rule("感冒", "呼吸内科"),
            new Rule("流鼻涕", "呼吸内科"),
            new Rule("喉咙痛", "呼吸内科"),
            new Rule("咽痛", "呼吸内科"),
            new Rule("打喷嚏", "呼吸内科"),
            new Rule("鼻塞", "呼吸内科"),
            new Rule("气喘", "呼吸内科"),
            new Rule("肺炎", "呼吸内科"),
            new Rule("流感", "呼吸内科"),
            new Rule("呼吸困难", "呼吸内科", "急诊科"),

            // 心血管内科
            new Rule("胸痛", "心血管内科", "急诊科"),
            new Rule("胸闷", "心血管内科", "呼吸内科"),
            new Rule("心慌", "心血管内科"),
            new Rule("心悸", "心血管内科"),
            new Rule("心跳快", "心血管内科"),
            new Rule("心跳慢", "心血管内科"),
            new Rule("血压高", "心血管内科"),
            new Rule("高血压", "心血管内科"),
            new Rule("气短", "心血管内科", "呼吸内科"),
            new Rule("心绞痛", "心血管内科", "急诊科"),
            new Rule("心衰", "心血管内科"),

            // 消化内科
            new Rule("腹痛", "消化内科"),
            new Rule("肚子疼", "消化内科"),
            new Rule("胃痛", "消化内科"),
            new Rule("胃胀", "消化内科"),
            new Rule("腹泻", "消化内科"),
            new Rule("拉肚子", "消化内科"),
            new Rule("恶心", "消化内科"),
            new Rule("想吐", "消化内科"),
            new Rule("呕吐", "消化内科"),
            new Rule("便秘", "消化内科"),
            new Rule("消化不良", "消化内科"),
            new Rule("反酸", "消化内科"),
            new Rule("烧心", "消化内科"),
            new Rule("食欲不振", "消化内科"),
            new Rule("便血", "消化内科"),
            new Rule("黑便", "消化内科"),

            // 神经内科
            new Rule("头痛", "神经内科"),
            new Rule("偏头痛", "神经内科"),
            new Rule("头晕", "神经内科", "心血管内科"),
            new Rule("眩晕", "神经内科"),
            new Rule("失眠", "神经内科"),
            new Rule("睡不着", "神经内科"),
            new Rule("手脚发麻", "神经内科"),
            new Rule("麻木", "神经内科"),
            new Rule("抽搐", "神经内科", "急诊科"),
            new Rule("记忆力下降", "神经内科"),
            new Rule("帕金森", "神经内科"),
            new Rule("癫痫", "神经内科"),
            new Rule("手抖", "神经内科"),
            new Rule("面瘫", "神经内科"),

            // 骨科
            new Rule("骨折", "骨科"),
            new Rule("扭伤", "骨科"),
            new Rule("腰疼", "骨科"),
            new Rule("腰痛", "骨科", "泌尿外科"),
            new Rule("背痛", "骨科"),
            new Rule("颈椎", "骨科"),
            new Rule("脖子痛", "骨科"),
            new Rule("肩膀痛", "骨科"),
            new Rule("关节痛", "骨科"),
            new Rule("膝盖痛", "骨科"),
            new Rule("腿痛", "骨科"),
            new Rule("脚痛", "骨科"),
            new Rule("手腕痛", "骨科"),
            new Rule("骨痛", "骨科"),
            new Rule("关节炎", "骨科"),
            new Rule("腰椎", "骨科"),
            new Rule("椎间盘", "骨科"),
            new Rule("落枕", "骨科"),

            // 皮肤科
            new Rule("皮疹", "皮肤科"),
            new Rule("皮肤痒", "皮肤科"),
            new Rule("瘙痒", "皮肤科"),
            new Rule("过敏", "皮肤科"),
            new Rule("红肿", "皮肤科"),
            new Rule("起包", "皮肤科"),
            new Rule("痘痘", "皮肤科"),
            new Rule("痤疮", "皮肤科"),
            new Rule("脱发", "皮肤科"),
            new Rule("湿疹", "皮肤科"),
            new Rule("疱疹", "皮肤科"),
            new Rule("皮肤溃烂", "皮肤科"),
            new Rule("荨麻疹", "皮肤科"),
            new Rule("牛皮癣", "皮肤科"),
            new Rule("红斑", "皮肤科"),

            // 眼科
            new Rule("眼睛痛", "眼科"),
            new Rule("眼痛", "眼科"),
            new Rule("眼红", "眼科"),
            new Rule("视力模糊", "眼科"),
            new Rule("视力下降", "眼科"),
            new Rule("看不清", "眼科"),
            new Rule("眼睛干", "眼科"),
            new Rule("流泪", "眼科"),
            new Rule("眼睛痒", "眼科"),
            new Rule("飞蚊症", "眼科"),
            new Rule("白内障", "眼科"),
            new Rule("眼屎", "眼科"),

            // 口腔科
            new Rule("牙痛", "口腔科"),
            new Rule("牙疼", "口腔科"),
            new Rule("牙龈出血", "口腔科"),
            new Rule("牙龈肿", "口腔科"),
            new Rule("口腔溃疡", "口腔科"),
            new Rule("口臭", "口腔科"),
            new Rule("牙齿松动", "口腔科"),
            new Rule("牙酸", "口腔科"),
            new Rule("蛀牙", "口腔科"),

            // 妇科
            new Rule("月经不调", "妇科"),
            new Rule("痛经", "妇科"),
            new Rule("白带异常", "妇科"),
            new Rule("妇科炎症", "妇科"),
            new Rule("外阴瘙痒", "妇科"),
            new Rule("更年期", "妇科"),
            new Rule("乳房胀痛", "妇科"),
            new Rule("不孕", "妇科"),
            new Rule("孕期", "妇科"),

            // 儿科
            new Rule("小儿", "儿科"),
            new Rule("小孩", "儿科"),
            new Rule("宝宝", "儿科"),
            new Rule("婴儿", "儿科"),
            new Rule("儿童", "儿科"),

            // 内分泌科
            new Rule("糖尿病", "内分泌科"),
            new Rule("血糖高", "内分泌科"),
            new Rule("甲亢", "内分泌科"),
            new Rule("甲减", "内分泌科"),
            new Rule("肥胖", "内分泌科"),
            new Rule("消瘦", "内分泌科"),
            new Rule("多尿", "内分泌科", "泌尿外科"),
            new Rule("多饮", "内分泌科"),
            new Rule("痛风", "内分泌科"),
            new Rule("口渴", "内分泌科"),

            // 泌尿外科
            new Rule("尿痛", "泌尿外科"),
            new Rule("尿频", "泌尿外科"),
            new Rule("尿急", "泌尿外科"),
            new Rule("尿血", "泌尿外科"),
            new Rule("血尿", "泌尿外科"),
            new Rule("肾结石", "泌尿外科"),
            new Rule("前列腺", "泌尿外科"),
            new Rule("排尿困难", "泌尿外科")
    );

    private static final List<String> EMERGENCY_KEYWORDS = Arrays.asList(
            "胸痛", "呼吸困难", "昏迷", "意识模糊", "大出血", "抽搐", "晕厥",
            "口角歪斜", "半身不遂", "剧烈头痛", "心跳骤停", "喘不上气", "休克", "中毒");

    private static final Map<String, List<String>> KEYWORD_INDEX;

    static {
        Map<String, LinkedHashSet<String>> index = new LinkedHashMap<>();
        for (Rule rule : RULES) {
            LinkedHashSet<String> departments = index.computeIfAbsent(rule.keyword, k -> new LinkedHashSet<>());
            departments.addAll(Arrays.asList(rule.departments));
        }
        Map<String, List<String>> frozen = new LinkedHashMap<>();
        index.forEach((keyword, departments) ->
                frozen.put(keyword, Collections.unmodifiableList(new ArrayList<>(departments))));
        KEYWORD_INDEX = Collections.unmodifiableMap(frozen);
    }

    private TriageEngine() {
    }

    /**
     * 匹配科室，按命中关键词数量降序。
     */
    public static List<Match> match(String text) {
        Map<String, List<String>> hits = new LinkedHashMap<>();
        for (Map.Entry<String, List<String>> entry : KEYWORD_INDEX.entrySet()) {
            if (!text.contains(entry.getKey())) {
                continue;
            }
            for (String department : entry.getValue()) {
                List<String> keywords = hits.computeIfAbsent(department, k -> new ArrayList<>());
                if (!keywords.contains(entry.getKey())) {
                    keywords.add(entry.getKey());
                }
            }
        }
        List<Match> matches = new ArrayList<>();
        hits.forEach((department, keywords) -> matches.add(new Match(department, keywords)));
        matches.sort((a, b) -> b.keywords.size() - a.keywords.size());
        return matches;
    }

    public static List<String> emergencyHits(String text) {
        List<String> hits = new ArrayList<>();
        for (String keyword : EMERGENCY_KEYWORDS) {
            if (text.contains(keyword)) {
                hits.add(keyword);
            }
        }
        return hits;
    }

    /**
     * 去掉「不咳嗽」「没有发烧」这类否定描述，减少误判。
     */
    public static String stripNegation(String text) {
        String result = text;
        for (String keyword : KEYWORD_INDEX.keySet()) {
            if (!result.contains(keyword)) {
                continue;
            }
            result = result.replaceAll("(没有|没|不|无|未)" + java.util.regex.Pattern.quote(keyword), " ");
        }
        return result;
    }

    public static Set<String> keywords() {
        return KEYWORD_INDEX.keySet();
    }

    public static int ruleCount() {
        return RULES.size();
    }

    private static final class Rule {
        private final String keyword;
        private final String[] departments;

        private Rule(String keyword, String... departments) {
            this.keyword = keyword;
            this.departments = departments;
        }
    }

    public static final class Match {
        private final String department;
        private final List<String> keywords;

        private Match(String department, List<String> keywords) {
            this.department = department;
            this.keywords = Collections.unmodifiableList(keywords);
        }

        public String getDepartment() {
            return department;
        }

        public List<String> getKeywords() {
            return keywords;
        }
    }
}
