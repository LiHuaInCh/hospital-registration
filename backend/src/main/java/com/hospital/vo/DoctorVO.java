package com.hospital.vo;

import lombok.Data;

import java.math.BigDecimal;

@Data
public class DoctorVO {

    private Long id;
    private Long departmentId;
    private String departmentName;
    private String name;
    private Integer gender;
    private String title;
    private String specialty;
    private String description;
    private String avatar;
    private BigDecimal consultationFee;
    private Integer status;
}
