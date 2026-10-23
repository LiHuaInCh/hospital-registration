package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.entity.Department;
import com.hospital.vo.DepartmentVO;

import java.util.List;

public interface DepartmentService extends IService<Department> {

    List<DepartmentVO> listActive();

    Department detail(Long id);

    Department create(Department department);

    Department update(Long id, Department department);

    void delete(Long id);
}
