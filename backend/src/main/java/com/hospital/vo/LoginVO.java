package com.hospital.vo;

import lombok.Data;

@Data
public class LoginVO {

    private String token;
    private long expiresIn;
    private String role;
    private Long userId;
    private String nickname;
    private String avatarUrl;
}
