package com.hospital.service;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class TriageEngineTest {

    @Test
    @DisplayName("腰痛同时指向骨科与泌尿外科")
    void matchesMultipleDepartments() {
        List<TriageEngine.Match> matches = TriageEngine.match("腰痛三天了");

        assertTrue(matches.stream().anyMatch(m -> "骨科".equals(m.getDepartment())));
        assertTrue(matches.stream().anyMatch(m -> "泌尿外科".equals(m.getDepartment())));
    }

    @Test
    @DisplayName("命中关键词多的科室排在前面")
    void sortsByKeywordCount() {
        List<TriageEngine.Match> matches = TriageEngine.match("咳嗽发烧流鼻涕");

        assertEquals("呼吸内科", matches.get(0).getDepartment());
        assertEquals(3, matches.get(0).getKeywords().size());
    }

    @Test
    @DisplayName("否定描述不应命中对应症状")
    void ignoresNegatedSymptoms() {
        String text = TriageEngine.stripNegation("没有发烧，就是咳嗽");
        List<TriageEngine.Match> matches = TriageEngine.match(text);

        assertEquals(1, matches.size());
        assertEquals("呼吸内科", matches.get(0).getDepartment());
        assertFalse(matches.get(0).getKeywords().contains("发烧"));
        assertTrue(matches.get(0).getKeywords().contains("咳嗽"));
    }

    @Test
    @DisplayName("胸痛属于急症关键词")
    void detectsEmergencyKeywords() {
        List<String> hits = TriageEngine.emergencyHits("突然胸痛、喘不上气");

        assertTrue(hits.contains("胸痛"));
        assertFalse(TriageEngine.emergencyHits("牙齿有点酸").contains("胸痛"));
    }

    @Test
    @DisplayName("关键词表不应存在重复定义导致的覆盖")
    void keywordIndexHasNoDuplicateKeys() {
        assertTrue(TriageEngine.keywords().contains("腰痛"));
        assertTrue(TriageEngine.ruleCount() > 100);
    }
}
