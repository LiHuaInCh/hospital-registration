package com.hospital.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hospital.entity.Department;
import com.hospital.vo.DepartmentVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface DepartmentMapper extends BaseMapper<Department> {

    @Select("SELECT d.*, " +
            "(SELECT COUNT(*) FROM doctor dc WHERE dc.department_id = d.id AND dc.status = 1) AS doctor_count " +
            "FROM department d WHERE d.status = 1 ORDER BY d.sort_order ASC, d.id ASC")
    List<DepartmentVO> selectAllActive();
}
