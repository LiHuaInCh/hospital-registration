package com.hospital.vo;

import lombok.Data;

import java.util.List;

@Data
public class TriageItemVO {

    private Long departmentId;
    private String departmentName;
    private String description;
    private String location;
    private Integer confidence;
    private List<String> matchedKeywords;
}
