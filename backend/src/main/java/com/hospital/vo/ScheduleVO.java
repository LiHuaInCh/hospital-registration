package com.hospital.vo;

import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalTime;

@Data
public class ScheduleVO {

    private Long id;
    private Long doctorId;
    private String doctorName;
    private String title;
    private Long departmentId;
    private String departmentName;
    private LocalDate workDate;
    private String timeSlot;
    private LocalTime startTime;
    private LocalTime endTime;
    private Integer totalCount;
    private Integer remainCount;
    private Integer status;
    private BigDecimal consultationFee;
}
