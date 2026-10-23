package com.hospital.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hospital.common.BusinessException;
import com.hospital.entity.Department;
import com.hospital.entity.Doctor;
import com.hospital.mapper.DepartmentMapper;
import com.hospital.mapper.DoctorMapper;
import com.hospital.service.DepartmentService;
import com.hospital.vo.DepartmentVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DepartmentServiceImpl extends ServiceImpl<DepartmentMapper, Department> implements DepartmentService {

    private final DoctorMapper doctorMapper;

    @Override
    public List<DepartmentVO> listActive() {
        return baseMapper.selectAllActive();
    }

    @Override
    public Department detail(Long id) {
        Department department = getById(id);
        if (department == null) {
            throw new BusinessException(404, "科室不存在");
        }
        return department;
    }

    @Override
    @Transactional
    public Department create(Department department) {
        String name = requireName(department.getName());
        ensureNameAvailable(name, null);

        Department entity = new Department();
        entity.setName(name);
        entity.setDescription(department.getDescription());
        entity.setIcon(department.getIcon());
        entity.setLocation(department.getLocation());
        entity.setPhone(department.getPhone());
        entity.setSortOrder(department.getSortOrder() == null ? 0 : department.getSortOrder());
        entity.setStatus(department.getStatus() == null ? 1 : department.getStatus());
        save(entity);
        return entity;
    }

    @Override
    @Transactional
    public Department update(Long id, Department department) {
        Department exist = detail(id);
        String name = requireName(department.getName());
        ensureNameAvailable(name, id);

        exist.setName(name);
        exist.setDescription(department.getDescription());
        exist.setIcon(department.getIcon());
        exist.setLocation(department.getLocation());
        exist.setPhone(department.getPhone());
        if (department.getSortOrder() != null) {
            exist.setSortOrder(department.getSortOrder());
        }
        if (department.getStatus() != null) {
            exist.setStatus(department.getStatus());
        }
        updateById(exist);
        return exist;
    }

    @Override
    @Transactional
    public void delete(Long id) {
        detail(id);
        Long doctors = doctorMapper.selectCount(new LambdaQueryWrapper<Doctor>()
                .eq(Doctor::getDepartmentId, id));
        if (doctors != null && doctors > 0) {
            throw new BusinessException("该科室下还有 " + doctors + " 位医生，请先调整医生所属科室");
        }
        removeById(id);
    }

    private String requireName(String name) {
        String value = name == null ? "" : name.trim();
        if (value.isEmpty()) {
            throw new BusinessException("请输入科室名称");
        }
        if (value.length() > 100) {
            throw new BusinessException("科室名称过长");
        }
        return value;
    }

    private void ensureNameAvailable(String name, Long excludeId) {
        LambdaQueryWrapper<Department> wrapper = new LambdaQueryWrapper<Department>()
                .eq(Department::getName, name);
        if (excludeId != null) {
            wrapper.ne(Department::getId, excludeId);
        }
        Long count = baseMapper.selectCount(wrapper);
        if (count != null && count > 0) {
            throw new BusinessException("已存在同名科室");
        }
    }
}
