package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.NotNull;

@Data
public class RegistrationCreateDTO {

    @NotNull(message = "请选择就诊人")
    private Long patientId;

    @NotNull(message = "请选择排班时段")
    private Long scheduleId;
}
