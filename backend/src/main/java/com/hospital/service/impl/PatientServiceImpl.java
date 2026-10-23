package com.hospital.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.BusinessException;
import com.hospital.dto.PatientDTO;
import com.hospital.entity.Patient;
import com.hospital.mapper.PatientMapper;
import com.hospital.mapper.RegistrationMapper;
import com.hospital.service.PatientService;
import com.hospital.util.Ids;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Objects;

@Service
@RequiredArgsConstructor
public class PatientServiceImpl extends ServiceImpl<PatientMapper, Patient> implements PatientService {

    private final RegistrationMapper registrationMapper;

    @Override
    public List<Patient> list(Long userId) {
        return baseMapper.selectByUserId(userId);
    }

    @Override
    public Patient detail(Long id, Long userId) {
        Patient patient = getById(id);
        if (patient == null || !Objects.equals(patient.getUserId(), userId)) {
            throw new BusinessException(404, "就诊人不存在");
        }
        return patient;
    }

    @Override
    @Transactional
    public Patient create(Long userId, PatientDTO dto) {
        Ids.checkIdCard(dto.getIdCard());
        Ids.checkPhone(dto.getPhone());
        String idCard = dto.getIdCard().trim().toUpperCase();
        ensureIdCardAvailable(userId, idCard, null);

        boolean first = baseMapper.selectCount(new LambdaQueryWrapper<Patient>()
                .eq(Patient::getUserId, userId)) == 0;
        boolean asDefault = first || Integer.valueOf(1).equals(dto.getIsDefault());
        if (asDefault) {
            clearDefault(userId);
        }

        Patient patient = new Patient();
        patient.setUserId(userId);
        apply(patient, dto, idCard);
        patient.setIsDefault(asDefault ? 1 : 0);
        save(patient);
        return patient;
    }

    @Override
    @Transactional
    public Patient update(Long userId, PatientDTO dto) {
        if (dto.getId() == null) {
            throw new BusinessException("缺少就诊人标识");
        }
        Patient patient = detail(dto.getId(), userId);

        Ids.checkIdCard(dto.getIdCard());
        Ids.checkPhone(dto.getPhone());
        String idCard = dto.getIdCard().trim().toUpperCase();
        ensureIdCardAvailable(userId, idCard, patient.getId());

        if (Integer.valueOf(1).equals(dto.getIsDefault())) {
            clearDefault(userId);
            patient.setIsDefault(1);
        } else if (dto.getIsDefault() != null) {
            patient.setIsDefault(0);
        }

        apply(patient, dto, idCard);
        updateById(patient);
        return patient;
    }

    @Override
    @Transactional
    public void delete(Long id, Long userId) {
        detail(id, userId);
        int registrations = registrationMapper.countByPatient(id);
        if (registrations > 0) {
            throw new BusinessException("该就诊人存在挂号记录，无法删除");
        }
        removeById(id);
    }

    private void apply(Patient patient, PatientDTO dto, String idCard) {
        patient.setName(dto.getName().trim());
        patient.setIdCard(idCard);
        patient.setPhone(dto.getPhone().trim());
        patient.setGender(dto.getGender());
        patient.setAge(dto.getAge());
        patient.setRelationship(dto.getRelationship());
    }

    private void ensureIdCardAvailable(Long userId, String idCard, Long excludeId) {
        LambdaQueryWrapper<Patient> wrapper = new LambdaQueryWrapper<Patient>()
                .eq(Patient::getUserId, userId)
                .eq(Patient::getIdCard, idCard);
        if (excludeId != null) {
            wrapper.ne(Patient::getId, excludeId);
        }
        Long count = baseMapper.selectCount(wrapper);
        if (count != null && count > 0) {
            throw new BusinessException("该身份证号的就诊人已存在");
        }
    }

    private void clearDefault(Long userId) {
        Patient patch = new Patient();
        patch.setIsDefault(0);
        update(patch, new LambdaQueryWrapper<Patient>()
                .eq(Patient::getUserId, userId)
                .eq(Patient::getIsDefault, 1));
    }
}
