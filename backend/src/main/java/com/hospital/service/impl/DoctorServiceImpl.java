package com.hospital.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.BusinessException;
import com.hospital.entity.Department;
import com.hospital.entity.Doctor;
import com.hospital.entity.Schedule;
import com.hospital.mapper.DepartmentMapper;
import com.hospital.mapper.DoctorMapper;
import com.hospital.mapper.RegistrationMapper;
import com.hospital.mapper.ScheduleMapper;
import com.hospital.service.DoctorService;
import com.hospital.vo.DoctorVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
@RequiredArgsConstructor
public class DoctorServiceImpl extends ServiceImpl<DoctorMapper, Doctor> implements DoctorService {

    private final DepartmentMapper departmentMapper;
    private final ScheduleMapper scheduleMapper;
    private final RegistrationMapper registrationMapper;

    @Override
    public List<DoctorVO> list(Long departmentId) {
        if (departmentId == null) {
            return baseMapper.selectAllActive();
        }
        return baseMapper.selectByDepartmentId(departmentId);
    }

    @Override
    public List<DoctorVO> search(String keyword) {
        String value = keyword == null ? "" : keyword.trim();
        if (value.isEmpty()) {
            return baseMapper.selectAllActive();
        }
        return baseMapper.search(value);
    }

    @Override
    public DoctorVO detail(Long id) {
        DoctorVO doctor = baseMapper.selectDetail(id);
        if (doctor == null) {
            throw new BusinessException(404, "医生不存在");
        }
        return doctor;
    }

    @Override
    @Transactional
    public DoctorVO create(Doctor doctor) {
        Doctor entity = new Doctor();
        apply(entity, doctor);
        entity.setStatus(1);
        save(entity);
        return detail(entity.getId());
    }

    @Override
    @Transactional
    public DoctorVO update(Long id, Doctor doctor) {
        Doctor entity = getById(id);
        if (entity == null) {
            throw new BusinessException(404, "医生不存在");
        }
        apply(entity, doctor);
        if (doctor.getStatus() != null) {
            entity.setStatus(doctor.getStatus());
        }
        updateById(entity);
        return detail(id);
    }

    @Override
    @Transactional
    public void delete(Long id) {
        detail(id);
        int registrations = registrationMapper.countByDoctor(id);
        if (registrations > 0) {
            throw new BusinessException("该医生已有挂号记录，无法删除，可将状态改为离职");
        }
        scheduleMapper.delete(new LambdaQueryWrapper<Schedule>().eq(Schedule::getDoctorId, id));
        removeById(id);
    }

    private void apply(Doctor entity, Doctor form) {
        String name = form.getName() == null ? "" : form.getName().trim();
        if (name.isEmpty()) {
            throw new BusinessException("请输入医生姓名");
        }
        if (name.length() > 50) {
            throw new BusinessException("医生姓名过长");
        }
        if (form.getDepartmentId() == null) {
            throw new BusinessException("请选择所属科室");
        }
        Department department = departmentMapper.selectById(form.getDepartmentId());
        if (department == null) {
            throw new BusinessException("所属科室不存在");
        }

        BigDecimal fee = form.getConsultationFee();
        if (fee == null) {
            fee = BigDecimal.ZERO;
        }
        if (fee.signum() < 0 || fee.compareTo(new BigDecimal("9999.99")) > 0) {
            throw new BusinessException("挂号费不合法");
        }

        entity.setName(name);
        entity.setDepartmentId(form.getDepartmentId());
        entity.setGender(form.getGender() == null ? 1 : form.getGender());
        entity.setTitle(form.getTitle());
        entity.setSpecialty(form.getSpecialty());
        entity.setDescription(form.getDescription());
        entity.setAvatar(form.getAvatar());
        entity.setConsultationFee(fee);
    }
}
