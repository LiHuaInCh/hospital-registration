package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

@Data
public class LoginDTO {

    @NotBlank(message = "请输入用户名")
    @Size(max = 50, message = "用户名过长")
    private String username;

    @NotBlank(message = "请输入密码")
    @Size(max = 64, message = "密码过长")
    private String password;
}
