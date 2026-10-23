package com.hospital.controller;

import com.hospital.common.R;
import com.hospital.dto.GuidanceDTO;
import com.hospital.service.GuidanceService;
import com.hospital.vo.TriageVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

@RestController
@RequestMapping("/api/guidance")
@RequiredArgsConstructor
public class GuidanceController {

    private final GuidanceService guidanceService;

    @PostMapping("/triage")
    public R<TriageVO> triage(@Valid @RequestBody GuidanceDTO dto) {
        return R.ok(guidanceService.triage(dto.getSymptoms()));
    }
}
