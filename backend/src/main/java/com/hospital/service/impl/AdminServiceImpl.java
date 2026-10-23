package com.hospital.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.BusinessException;
import com.hospital.common.Role;
import com.hospital.entity.Admin;
import com.hospital.mapper.AdminMapper;
import com.hospital.service.AdminService;
import com.hospital.util.JwtUtil;
import com.hospital.vo.LoginVO;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AdminServiceImpl extends ServiceImpl<AdminMapper, Admin> implements AdminService {

    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;

    @Override
    public LoginVO login(String username, String password) {
        Admin admin = baseMapper.selectOne(new LambdaQueryWrapper<Admin>()
                .eq(Admin::getUsername, username)
                .eq(Admin::getStatus, 1));

        if (admin == null || !passwordEncoder.matches(password, admin.getPassword())) {
            throw new BusinessException("用户名或密码错误");
        }

        LoginVO vo = new LoginVO();
        vo.setToken(jwtUtil.issue(admin.getId(), Role.ADMIN));
        vo.setExpiresIn(jwtUtil.getExpireMillis());
        vo.setRole(Role.ADMIN);
        vo.setUserId(admin.getId());
        vo.setNickname(admin.getRealName() == null ? admin.getUsername() : admin.getRealName());
        return vo;
    }
}
