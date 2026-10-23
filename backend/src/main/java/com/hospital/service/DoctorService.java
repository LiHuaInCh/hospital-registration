package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.entity.Doctor;
import com.hospital.vo.DoctorVO;

import java.util.List;

public interface DoctorService extends IService<Doctor> {

    List<DoctorVO> list(Long departmentId);

    List<DoctorVO> search(String keyword);

    DoctorVO detail(Long id);

    DoctorVO create(Doctor doctor);

    DoctorVO update(Long id, Doctor doctor);

    void delete(Long id);
}
