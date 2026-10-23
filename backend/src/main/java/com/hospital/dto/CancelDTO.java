package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Data
public class CancelDTO {

    @NotNull(message = "缺少挂号记录")
    private Long id;

    @Size(max = 100, message = "取消原因请控制在 100 字以内")
    private String reason;
}
