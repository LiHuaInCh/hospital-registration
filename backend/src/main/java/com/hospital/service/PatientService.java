package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.dto.PatientDTO;
import com.hospital.entity.Patient;

import java.util.List;

public interface PatientService extends IService<Patient> {

    List<Patient> list(Long userId);

    Patient detail(Long id, Long userId);

    Patient create(Long userId, PatientDTO dto);

    Patient update(Long userId, PatientDTO dto);

    void delete(Long id, Long userId);
}
