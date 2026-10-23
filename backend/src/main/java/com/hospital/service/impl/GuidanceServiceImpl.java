package com.hospital.service.impl;

import com.hospital.common.BusinessException;
import com.hospital.mapper.DepartmentMapper;
import com.hospital.service.GuidanceService;
import com.hospital.service.TriageEngine;
import com.hospital.vo.DepartmentVO;
import com.hospital.vo.TriageItemVO;
import com.hospital.vo.TriageVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class GuidanceServiceImpl implements GuidanceService {

    private static final String EMERGENCY_DEPARTMENT = "急诊科";

    private final DepartmentMapper departmentMapper;

    @Override
    public TriageVO triage(String symptoms) {
        String text = TriageEngine.stripNegation(symptoms.trim());
        Map<String, DepartmentVO> departments = new LinkedHashMap<>();
        for (DepartmentVO department : departmentMapper.selectAllActive()) {
            departments.put(department.getName(), department);
        }

        List<TriageEngine.Match> matches = TriageEngine.match(text);
        List<String> emergencyKeywords = TriageEngine.emergencyHits(text);

        List<TriageItemVO> results = new ArrayList<>();
        String advice = null;

        if (!emergencyKeywords.isEmpty()) {
            DepartmentVO emergency = departments.get(EMERGENCY_DEPARTMENT);
            if (emergency != null) {
                results.add(toItem(emergency, emergencyKeywords, 96));
            }
            advice = "您描述的「" + String.join("、", emergencyKeywords)
                    + "」可能提示急症，请立即前往急诊科就诊或拨打 120，不要等待门诊号源。";
        }

        for (TriageEngine.Match match : matches) {
            DepartmentVO department = departments.get(match.getDepartment());
            if (department == null || EMERGENCY_DEPARTMENT.equals(department.getName())) {
                continue;
            }
            int confidence = Math.min(93, 48 + match.getKeywords().size() * 13);
            results.add(toItem(department, match.getKeywords(), confidence));
        }

        if (results.isEmpty()) {
            throw new BusinessException("未能识别您的症状，建议前往导诊台咨询");
        }

        TriageVO vo = new TriageVO();
        vo.setEmergency(!emergencyKeywords.isEmpty());
        vo.setAdvice(advice);
        vo.setResults(results);
        return vo;
    }

    private TriageItemVO toItem(DepartmentVO department, List<String> keywords, int confidence) {
        TriageItemVO item = new TriageItemVO();
        item.setDepartmentId(department.getId());
        item.setDepartmentName(department.getName());
        item.setDescription(department.getDescription());
        item.setLocation(department.getLocation());
        item.setConfidence(confidence);
        item.setMatchedKeywords(new ArrayList<>(keywords));
        return item;
    }
}
