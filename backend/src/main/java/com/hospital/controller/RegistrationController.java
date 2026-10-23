package com.hospital.controller;

import com.hospital.common.PageResult;
import com.hospital.common.R;
import com.hospital.common.UserContext;
import com.hospital.dto.CancelDTO;
import com.hospital.dto.RegistrationCreateDTO;
import com.hospital.service.RegistrationService;
import com.hospital.vo.RegistrationVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/registration")
@RequiredArgsConstructor
public class RegistrationController {

    private final RegistrationService registrationService;

    @PostMapping("/create")
    public R<RegistrationVO> create(@Valid @RequestBody RegistrationCreateDTO dto) {
        return R.ok(registrationService.create(UserContext.userId(), dto));
    }

    @GetMapping("/list")
    public R<PageResult<RegistrationVO>> list(
            @RequestParam(required = false) List<Integer> status,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        return R.ok(registrationService.pageForUser(UserContext.userId(), status, page, size));
    }

    @GetMapping("/detail")
    public R<RegistrationVO> detail(@RequestParam Long id) {
        return R.ok(registrationService.detail(id, UserContext.userId()));
    }

    @PostMapping("/cancel")
    public R<Void> cancel(@Valid @RequestBody CancelDTO dto) {
        registrationService.cancel(UserContext.userId(), dto.getId(), dto.getReason());
        return R.ok();
    }
}
