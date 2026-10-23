package com.hospital.controller;

import com.hospital.common.PageResult;
import com.hospital.common.R;
import com.hospital.dto.LoginDTO;
import com.hospital.dto.RegistrationStatusDTO;
import com.hospital.service.AdminService;
import com.hospital.service.RegistrationService;
import com.hospital.service.ScheduleService;
import com.hospital.vo.LoginVO;
import com.hospital.vo.RegistrationVO;
import com.hospital.vo.ScheduleVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final AdminService adminService;
    private final RegistrationService registrationService;
    private final ScheduleService scheduleService;

    @PostMapping("/login")
    public R<LoginVO> login(@Valid @RequestBody LoginDTO dto) {
        return R.ok(adminService.login(dto.getUsername(), dto.getPassword()));
    }

    @GetMapping("/registration/list")
    public R<PageResult<RegistrationVO>> registrations(
            @RequestParam(required = false) List<Integer> status,
            @RequestParam(required = false) String date,
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        LocalDate workDate = date == null || date.trim().isEmpty() ? null : LocalDate.parse(date.trim());
        return R.ok(registrationService.pageForAdmin(status, workDate, keyword, page, size));
    }

    @PutMapping("/registration/status")
    public R<Void> changeStatus(@Valid @RequestBody RegistrationStatusDTO dto) {
        registrationService.changeStatus(dto.getId(), dto.getStatus());
        return R.ok();
    }

    @GetMapping("/schedule/list")
    public R<List<ScheduleVO>> schedules(
            @RequestParam(required = false) String date,
            @RequestParam(required = false) Long departmentId) {
        LocalDate workDate = date == null || date.trim().isEmpty() ? null : LocalDate.parse(date.trim());
        return R.ok(scheduleService.listForAdmin(workDate, departmentId));
    }
}
