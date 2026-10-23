package com.hospital.service.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.BusinessException;
import com.hospital.common.PageResult;
import com.hospital.common.RegistrationStatus;
import com.hospital.dto.RegistrationCreateDTO;
import com.hospital.entity.Department;
import com.hospital.entity.Doctor;
import com.hospital.entity.Patient;
import com.hospital.entity.Registration;
import com.hospital.entity.Schedule;
import com.hospital.mapper.DepartmentMapper;
import com.hospital.mapper.DoctorMapper;
import com.hospital.mapper.PatientMapper;
import com.hospital.mapper.RegistrationMapper;
import com.hospital.service.RegistrationService;
import com.hospital.service.ScheduleService;
import com.hospital.util.TimeSlots;
import com.hospital.vo.RegistrationVO;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

@Service
@RequiredArgsConstructor
public class RegistrationServiceImpl extends ServiceImpl<RegistrationMapper, Registration>
        implements RegistrationService {

    private final ScheduleService scheduleService;
    private final DoctorMapper doctorMapper;
    private final DepartmentMapper departmentMapper;
    private final PatientMapper patientMapper;

    @Value("${app.booking.cancel-limit-hours:2}")
    private long cancelLimitHours;

    @Override
    @Transactional
    public RegistrationVO create(Long userId, RegistrationCreateDTO dto) {
        Patient patient = patientMapper.selectById(dto.getPatientId());
        if (patient == null || !Objects.equals(patient.getUserId(), userId)) {
            throw new BusinessException("就诊人不存在，请重新选择");
        }

        Schedule schedule = scheduleService.requireBookable(dto.getScheduleId());
        if (!LocalDateTime.now().isBefore(scheduleService.startAt(schedule))) {
            throw new BusinessException("该时段已开始，无法预约");
        }
        if (baseMapper.countActive(patient.getId(), schedule.getId()) > 0) {
            throw new BusinessException("该就诊人已预约该时段，请勿重复挂号");
        }
        if (!scheduleService.decreaseStock(schedule.getId())) {
            throw new BusinessException("号源已约满，请选择其他时段");
        }

        Doctor doctor = doctorMapper.selectById(schedule.getDoctorId());
        if (doctor == null) {
            throw new BusinessException("医生信息不存在");
        }
        Department department = departmentMapper.selectById(doctor.getDepartmentId());
        BigDecimal fee = doctor.getConsultationFee() == null ? BigDecimal.ZERO : doctor.getConsultationFee();

        Registration registration = new Registration();
        registration.setUserId(userId);
        registration.setPatientId(patient.getId());
        registration.setScheduleId(schedule.getId());
        registration.setDepartmentId(doctor.getDepartmentId());
        registration.setDoctorId(doctor.getId());
        registration.setWorkDate(schedule.getWorkDate());
        registration.setTimeSlot(schedule.getTimeSlot());
        registration.setFee(fee);
        registration.setStatus(RegistrationStatus.BOOKED);
        save(registration);

        RegistrationVO vo = new RegistrationVO();
        vo.setId(registration.getId());
        vo.setPatientId(patient.getId());
        vo.setPatientName(patient.getName());
        vo.setScheduleId(schedule.getId());
        vo.setDepartmentId(doctor.getDepartmentId());
        vo.setDepartmentName(department == null ? null : department.getName());
        vo.setDoctorId(doctor.getId());
        vo.setDoctorName(doctor.getName());
        vo.setTitle(doctor.getTitle());
        vo.setWorkDate(schedule.getWorkDate());
        vo.setTimeSlot(schedule.getTimeSlot());
        vo.setStartTime(schedule.getStartTime());
        vo.setEndTime(schedule.getEndTime());
        vo.setFee(fee);
        vo.setStatus(RegistrationStatus.BOOKED);
        vo.setCreateTime(registration.getCreateTime());
        return vo;
    }

    @Override
    public PageResult<RegistrationVO> pageForUser(Long userId, List<Integer> statuses, int page, int size) {
        Page<RegistrationVO> request = new Page<>(normalizePage(page), normalizeSize(size));
        return PageResult.of(baseMapper.selectPageVo(request, userId, statuses, null, null));
    }

    @Override
    public RegistrationVO detail(Long id, Long userId) {
        Registration registration = getById(id);
        if (registration == null || !Objects.equals(registration.getUserId(), userId)) {
            throw new BusinessException(404, "挂号记录不存在");
        }
        return baseMapper.selectDetail(id);
    }

    @Override
    @Transactional
    public void cancel(Long userId, Long id, String reason) {
        Registration registration = getById(id);
        if (registration == null || !Objects.equals(registration.getUserId(), userId)) {
            throw new BusinessException(404, "挂号记录不存在");
        }
        if (!Integer.valueOf(RegistrationStatus.BOOKED).equals(registration.getStatus())) {
            throw new BusinessException("当前状态不可取消");
        }

        Schedule schedule = scheduleService.getById(registration.getScheduleId());
        LocalDateTime start = startAt(registration, schedule);
        if (!LocalDateTime.now().isBefore(start.minusHours(cancelLimitHours))) {
            throw new BusinessException("已超过取消时限（就诊前 " + cancelLimitHours + " 小时）");
        }

        registration.setStatus(RegistrationStatus.CANCELED);
        registration.setCancelReason(isBlank(reason) ? "用户取消" : reason.trim());
        updateById(registration);
        scheduleService.increaseStock(registration.getScheduleId());
    }

    @Override
    public PageResult<RegistrationVO> pageForAdmin(List<Integer> statuses, LocalDate date,
                                                   String keyword, int page, int size) {
        Page<RegistrationVO> request = new Page<>(normalizePage(page), normalizeSize(size));
        String value = keyword == null || keyword.trim().isEmpty() ? null : keyword.trim();
        return PageResult.of(baseMapper.selectPageVo(request, null, statuses, date, value));
    }

    @Override
    @Transactional
    public void changeStatus(Long id, Integer status) {
        Registration registration = getById(id);
        if (registration == null) {
            throw new BusinessException(404, "挂号记录不存在");
        }
        int from = registration.getStatus();
        if (from == status) {
            return;
        }
        if (!isAllowed(from, status)) {
            throw new BusinessException("不支持的状态变更");
        }

        registration.setStatus(status);
        if (status == RegistrationStatus.CANCELED) {
            registration.setCancelReason("管理员取消");
            updateById(registration);
            scheduleService.increaseStock(registration.getScheduleId());
        } else {
            updateById(registration);
        }
    }

    private boolean isAllowed(int from, int to) {
        if (to == RegistrationStatus.CANCELED) {
            return from == RegistrationStatus.BOOKED || from == RegistrationStatus.CHECKED_IN;
        }
        if (to == RegistrationStatus.CHECKED_IN) {
            return from == RegistrationStatus.BOOKED;
        }
        if (to == RegistrationStatus.FINISHED) {
            return from == RegistrationStatus.CHECKED_IN;
        }
        return false;
    }

    private LocalDateTime startAt(Registration registration, Schedule schedule) {
        if (schedule != null) {
            return scheduleService.startAt(schedule);
        }
        return LocalDateTime.of(registration.getWorkDate(), TimeSlots.start(registration.getTimeSlot()));
    }

    private long normalizePage(int page) {
        return Math.max(1, page);
    }

    private long normalizeSize(int size) {
        if (size <= 0) {
            return 10;
        }
        return Math.min(50, size);
    }

    private boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }
}
