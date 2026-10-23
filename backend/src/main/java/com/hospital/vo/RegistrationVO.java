package com.hospital.vo;

import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Data
public class RegistrationVO {

    private Long id;
    private Long patientId;
    private String patientName;
    private Long scheduleId;
    private Long departmentId;
    private String departmentName;
    private Long doctorId;
    private String doctorName;
    private String title;
    private LocalDate workDate;
    private String timeSlot;
    private LocalTime startTime;
    private LocalTime endTime;
    private BigDecimal fee;
    private Integer status;
    private String cancelReason;
    private LocalDateTime createTime;
}
