package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.Size;

@Data
public class WxLoginDTO {

    @Size(max = 64, message = "登录凭证过长")
    private String code;

    @Size(max = 50, message = "昵称过长")
    private String nickname;

    @Size(max = 500, message = "头像地址过长")
    private String avatarUrl;
}
