package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.entity.Schedule;
import com.hospital.vo.ScheduleVO;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

public interface ScheduleService extends IService<Schedule> {

    List<ScheduleVO> listBookable(Long doctorId);

    List<ScheduleVO> listForAdmin(LocalDate date, Long departmentId);

    ScheduleVO detail(Long id);

    ScheduleVO create(Schedule schedule);

    ScheduleVO update(Long id, Schedule schedule);

    void delete(Long id);

    /** 校验排班可用于挂号，返回排班实体 */
    Schedule requireBookable(Long id);

    boolean decreaseStock(Long id);

    void increaseStock(Long id);

    /** 该排班的开诊时间 */
    LocalDateTime startAt(Schedule schedule);
}
