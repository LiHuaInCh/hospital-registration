package com.hospital.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.Role;
import com.hospital.dto.WxLoginDTO;
import com.hospital.entity.User;
import com.hospital.mapper.UserMapper;
import com.hospital.service.UserService;
import com.hospital.util.JwtUtil;
import com.hospital.vo.LoginVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    private static final String DEFAULT_NICKNAME = "微信用户";

    private final JwtUtil jwtUtil;

    @Override
    @Transactional
    public LoginVO login(WxLoginDTO dto) {
        String openid = resolveOpenid(dto.getCode());
        User user = baseMapper.selectByOpenid(openid);

        if (user == null) {
            user = new User();
            user.setOpenid(openid);
            user.setNickname(isBlank(dto.getNickname()) ? DEFAULT_NICKNAME : dto.getNickname().trim());
            user.setAvatarUrl(dto.getAvatarUrl());
            save(user);
        } else {
            boolean changed = false;
            if (!isBlank(dto.getNickname()) && !dto.getNickname().trim().equals(user.getNickname())) {
                user.setNickname(dto.getNickname().trim());
                changed = true;
            }
            if (!isBlank(dto.getAvatarUrl()) && !dto.getAvatarUrl().equals(user.getAvatarUrl())) {
                user.setAvatarUrl(dto.getAvatarUrl());
                changed = true;
            }
            if (changed) {
                updateById(user);
                user = getById(user.getId());
            }
        }

        LoginVO vo = new LoginVO();
        vo.setToken(jwtUtil.issue(user.getId(), Role.USER));
        vo.setExpiresIn(jwtUtil.getExpireMillis());
        vo.setRole(Role.USER);
        vo.setUserId(user.getId());
        vo.setNickname(user.getNickname());
        vo.setAvatarUrl(user.getAvatarUrl());
        return vo;
    }

    /**
     * 演示环境直接用设备侧生成的标识充当 openid；
     * 接入真实微信登录时，这里应改为调用 jscode2session 换取 openid。
     */
    private String resolveOpenid(String code) {
        String value = isBlank(code) ? UUID.randomUUID().toString().replace("-", "") : code.trim();
        String openid = "wx_" + value;
        return openid.length() > 100 ? openid.substring(0, 100) : openid;
    }

    private boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }
}
