package com.hospital.vo;

import lombok.Data;

@Data
public class DepartmentVO {

    private Long id;
    private String name;
    private String description;
    private String icon;
    private String location;
    private String phone;
    private Integer sortOrder;
    private Integer status;
    private Integer doctorCount;
}
