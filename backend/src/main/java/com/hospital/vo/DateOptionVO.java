package com.hospital.vo;

import lombok.Data;

import java.time.LocalDate;

@Data
public class DateOptionVO {

    private LocalDate date;
    private String weekday;
    private boolean today;
}
