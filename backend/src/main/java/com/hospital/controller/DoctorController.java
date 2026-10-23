package com.hospital.controller;

import com.hospital.common.R;
import com.hospital.entity.Doctor;
import com.hospital.service.DoctorService;
import com.hospital.vo.DoctorVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/doctor")
@RequiredArgsConstructor
public class DoctorController {

    private final DoctorService doctorService;

    @GetMapping("/list")
    public R<List<DoctorVO>> list(@RequestParam(required = false) Long departmentId) {
        return R.ok(doctorService.list(departmentId));
    }

    @GetMapping("/search")
    public R<List<DoctorVO>> search(@RequestParam(required = false) String keyword) {
        return R.ok(doctorService.search(keyword));
    }

    @GetMapping("/detail")
    public R<DoctorVO> detail(@RequestParam Long id) {
        return R.ok(doctorService.detail(id));
    }

    @PostMapping("/add")
    public R<DoctorVO> add(@RequestBody Doctor doctor) {
        return R.ok(doctorService.create(doctor));
    }

    @PutMapping("/update")
    public R<DoctorVO> update(@RequestBody Doctor doctor) {
        if (doctor.getId() == null) {
            return R.fail("缺少医生标识");
        }
        return R.ok(doctorService.update(doctor.getId(), doctor));
    }

    @DeleteMapping("/delete")
    public R<Void> delete(@RequestParam Long id) {
        doctorService.delete(id);
        return R.ok();
    }
}
