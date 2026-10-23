package com.hospital.vo;

import lombok.Data;

import java.util.List;

@Data
public class TriageVO {

    private boolean emergency;
    private String advice;
    private List<TriageItemVO> results;
}
