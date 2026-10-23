package com.hospital.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.BusinessException;
import com.hospital.common.ScheduleStatus;
import com.hospital.entity.Doctor;
import com.hospital.entity.Schedule;
import com.hospital.mapper.DoctorMapper;
import com.hospital.mapper.RegistrationMapper;
import com.hospital.mapper.ScheduleMapper;
import com.hospital.service.ScheduleService;
import com.hospital.util.TimeSlots;
import com.hospital.vo.ScheduleVO;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ScheduleServiceImpl extends ServiceImpl<ScheduleMapper, Schedule> implements ScheduleService {

    private final DoctorMapper doctorMapper;
    private final RegistrationMapper registrationMapper;

    @Value("${app.booking.bookable-days:7}")
    private int bookableDays;

    @Override
    public List<ScheduleVO> listBookable(Long doctorId) {
        if (doctorId == null) {
            throw new BusinessException("请选择医生");
        }
        if (doctorMapper.selectById(doctorId) == null) {
            throw new BusinessException(404, "医生不存在");
        }
        LocalDate today = LocalDate.now();
        return baseMapper.selectBookable(doctorId, today, today.plusDays(Math.max(0, bookableDays - 1)));
    }

    @Override
    public List<ScheduleVO> listForAdmin(LocalDate date, Long departmentId) {
        LocalDate target = date == null ? LocalDate.now() : date;
        return baseMapper.selectForAdmin(target, departmentId, null);
    }

    @Override
    public ScheduleVO detail(Long id) {
        ScheduleVO vo = baseMapper.selectDetail(id);
        if (vo == null) {
            throw new BusinessException(404, "排班不存在");
        }
        return vo;
    }

    @Override
    @Transactional
    public ScheduleVO create(Schedule form) {
        if (form.getDoctorId() == null) {
            throw new BusinessException("请选择医生");
        }
        Doctor doctor = doctorMapper.selectById(form.getDoctorId());
        if (doctor == null) {
            throw new BusinessException("医生不存在");
        }
        if (doctor.getStatus() == null || doctor.getStatus() != 1) {
            throw new BusinessException("该医生已离职或停诊，无法排班");
        }
        if (form.getWorkDate() == null) {
            throw new BusinessException("请选择出诊日期");
        }
        if (form.getWorkDate().isBefore(LocalDate.now())) {
            throw new BusinessException("不能为已过去的日期排班");
        }
        String slot = form.getTimeSlot();
        if (!TimeSlots.supported(slot)) {
            throw new BusinessException("请选择正确的出诊时段");
        }
        int total = form.getTotalCount() == null ? 30 : form.getTotalCount();
        if (total < 1 || total > 200) {
            throw new BusinessException("号源数应在 1-200 之间");
        }
        Long duplicated = baseMapper.selectCount(new LambdaQueryWrapper<Schedule>()
                .eq(Schedule::getDoctorId, form.getDoctorId())
                .eq(Schedule::getWorkDate, form.getWorkDate())
                .eq(Schedule::getTimeSlot, slot));
        if (duplicated != null && duplicated > 0) {
            throw new BusinessException("该医生当天「" + slot + "」已排班，请直接修改号源数");
        }

        LocalTime start = form.getStartTime() == null ? TimeSlots.start(slot) : form.getStartTime();
        LocalTime end = form.getEndTime() == null ? TimeSlots.end(slot) : form.getEndTime();
        if (!end.isAfter(start)) {
            throw new BusinessException("结束时间必须晚于开始时间");
        }

        Schedule schedule = new Schedule();
        schedule.setDoctorId(form.getDoctorId());
        schedule.setWorkDate(form.getWorkDate());
        schedule.setTimeSlot(slot);
        schedule.setStartTime(start);
        schedule.setEndTime(end);
        schedule.setTotalCount(total);
        schedule.setRemainCount(total);
        schedule.setStatus(ScheduleStatus.OPEN);
        save(schedule);
        return detail(schedule.getId());
    }

    @Override
    @Transactional
    public ScheduleVO update(Long id, Schedule form) {
        Schedule schedule = getById(id);
        if (schedule == null) {
            throw new BusinessException(404, "排班不存在");
        }
        if (schedule.getWorkDate().isBefore(LocalDate.now())) {
            throw new BusinessException("该排班已过去，无法修改");
        }
        if (form.getDoctorId() != null && !form.getDoctorId().equals(schedule.getDoctorId())) {
            throw new BusinessException("排班创建后不能更换医生，请删除后重新添加");
        }

        if (form.getWorkDate() != null) {
            schedule.setWorkDate(form.getWorkDate());
        }
        if (TimeSlots.supported(form.getTimeSlot())) {
            schedule.setTimeSlot(form.getTimeSlot());
            schedule.setStartTime(TimeSlots.start(form.getTimeSlot()));
            schedule.setEndTime(TimeSlots.end(form.getTimeSlot()));
        }
        if (form.getTotalCount() != null) {
            int booked = schedule.getTotalCount() - schedule.getRemainCount();
            if (form.getTotalCount() < booked) {
                throw new BusinessException("号源数不能小于已预约的 " + booked + " 个");
            }
            schedule.setTotalCount(form.getTotalCount());
            schedule.setRemainCount(form.getTotalCount() - booked);
        }
        if (form.getStatus() != null) {
            schedule.setStatus(form.getStatus());
        }

        Long duplicated = baseMapper.selectCount(new LambdaQueryWrapper<Schedule>()
                .eq(Schedule::getDoctorId, schedule.getDoctorId())
                .eq(Schedule::getWorkDate, schedule.getWorkDate())
                .eq(Schedule::getTimeSlot, schedule.getTimeSlot())
                .ne(Schedule::getId, id));
        if (duplicated != null && duplicated > 0) {
            throw new BusinessException("该医生当天已有相同的排班");
        }

        updateById(schedule);
        return detail(id);
    }

    @Override
    @Transactional
    public void delete(Long id) {
        detail(id);
        int active = registrationMapper.countActiveBySchedule(id);
        if (active > 0) {
            throw new BusinessException("该排班已有 " + active + " 个未完成的挂号，无法删除");
        }
        removeById(id);
    }

    @Override
    public Schedule requireBookable(Long id) {
        Schedule schedule = getById(id);
        if (schedule == null) {
            throw new BusinessException("排班不存在");
        }
        if (schedule.getStatus() == null || schedule.getStatus() != ScheduleStatus.OPEN) {
            throw new BusinessException("该时段已停诊，请选择其他时段");
        }
        if (schedule.getWorkDate().isBefore(LocalDate.now())) {
            throw new BusinessException("该排班已过期");
        }
        if (schedule.getRemainCount() == null || schedule.getRemainCount() <= 0) {
            throw new BusinessException("该时段号源已约满");
        }
        return schedule;
    }

    @Override
    public boolean decreaseStock(Long id) {
        return baseMapper.decreaseStock(id) > 0;
    }

    @Override
    public void increaseStock(Long id) {
        baseMapper.increaseStock(id);
    }

    @Override
    public LocalDateTime startAt(Schedule schedule) {
        LocalTime start = schedule.getStartTime() != null
                ? schedule.getStartTime()
                : TimeSlots.start(schedule.getTimeSlot());
        return LocalDateTime.of(schedule.getWorkDate(), start);
    }
}
