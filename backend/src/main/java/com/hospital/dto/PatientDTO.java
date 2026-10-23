package com.hospital.dto;

import lombok.Data;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Data
public class PatientDTO {

    private Long id;

    @NotBlank(message = "请填写就诊人姓名")
    @Size(max = 30, message = "姓名过长")
    private String name;

    @NotBlank(message = "请填写身份证号")
    private String idCard;

    @NotBlank(message = "请填写手机号")
    private String phone;

    @NotNull(message = "请选择性别")
    @Min(value = 1, message = "性别参数有误")
    @Max(value = 2, message = "性别参数有误")
    private Integer gender;

    @Min(value = 0, message = "年龄不能为负数")
    @Max(value = 150, message = "年龄不合法")
    private Integer age;

    @Size(max = 20, message = "关系过长")
    private String relationship;

    private Integer isDefault;
}
