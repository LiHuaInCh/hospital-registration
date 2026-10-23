package com.hospital.controller;

import com.hospital.common.R;
import com.hospital.common.UserContext;
import com.hospital.dto.WxLoginDTO;
import com.hospital.entity.User;
import com.hospital.service.UserService;
import com.hospital.vo.LoginVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping("/login")
    public R<LoginVO> login(@Valid @RequestBody WxLoginDTO dto) {
        return R.ok(userService.login(dto));
    }

    @GetMapping("/me")
    public R<User> me() {
        return R.ok(userService.getById(UserContext.userId()));
    }
}
