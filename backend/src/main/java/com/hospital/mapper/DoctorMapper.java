package com.hospital.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hospital.entity.Doctor;
import com.hospital.vo.DoctorVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface DoctorMapper extends BaseMapper<Doctor> {

    String SELECT_WITH_DEPARTMENT = "SELECT d.id, d.department_id, d.name, d.gender, d.title, d.specialty, " +
            "d.description, d.avatar, d.consultation_fee, d.status, dept.name AS department_name " +
            "FROM doctor d LEFT JOIN department dept ON dept.id = d.department_id ";

    @Select(SELECT_WITH_DEPARTMENT + "WHERE d.status = 1 ORDER BY d.department_id ASC, d.id ASC")
    List<DoctorVO> selectAllActive();

    @Select(SELECT_WITH_DEPARTMENT + "WHERE d.department_id = #{departmentId} AND d.status = 1 ORDER BY d.id ASC")
    List<DoctorVO> selectByDepartmentId(@Param("departmentId") Long departmentId);

    @Select(SELECT_WITH_DEPARTMENT + "WHERE d.status = 1 AND (d.name LIKE CONCAT('%', #{keyword}, '%') " +
            "OR d.specialty LIKE CONCAT('%', #{keyword}, '%') " +
            "OR dept.name LIKE CONCAT('%', #{keyword}, '%')) ORDER BY d.id ASC")
    List<DoctorVO> search(@Param("keyword") String keyword);

    @Select(SELECT_WITH_DEPARTMENT + "WHERE d.id = #{id}")
    DoctorVO selectDetail(@Param("id") Long id);
}
