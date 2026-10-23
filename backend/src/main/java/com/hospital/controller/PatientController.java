package com.hospital.controller;

import com.hospital.common.R;
import com.hospital.common.UserContext;
import com.hospital.dto.PatientDTO;
import com.hospital.entity.Patient;
import com.hospital.service.PatientService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/patient")
@RequiredArgsConstructor
public class PatientController {

    private final PatientService patientService;

    @GetMapping("/list")
    public R<List<Patient>> list() {
        return R.ok(patientService.list(UserContext.userId()));
    }

    @GetMapping("/detail")
    public R<Patient> detail(@RequestParam Long id) {
        return R.ok(patientService.detail(id, UserContext.userId()));
    }

    @PostMapping("/add")
    public R<Patient> add(@Valid @RequestBody PatientDTO dto) {
        return R.ok(patientService.create(UserContext.userId(), dto));
    }

    @PutMapping("/update")
    public R<Patient> update(@Valid @RequestBody PatientDTO dto) {
        return R.ok(patientService.update(UserContext.userId(), dto));
    }

    @DeleteMapping("/delete")
    public R<Void> delete(@RequestParam Long id) {
        patientService.delete(id, UserContext.userId());
        return R.ok();
    }
}
