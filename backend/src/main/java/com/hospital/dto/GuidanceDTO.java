package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

@Data
public class GuidanceDTO {

    @NotBlank(message = "请描述您的症状")
    @Size(max = 300, message = "症状描述请控制在 300 字以内")
    private String symptoms;
}
