package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.NotNull;

@Data
public class RegistrationStatusDTO {

    @NotNull(message = "缺少挂号记录")
    private Long id;

    @NotNull(message = "缺少目标状态")
    private Integer status;
}
