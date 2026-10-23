package com.hospital.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hospital.entity.Patient;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface PatientMapper extends BaseMapper<Patient> {

    @Select("SELECT * FROM patient WHERE user_id = #{userId} ORDER BY is_default DESC, id ASC")
    List<Patient> selectByUserId(@Param("userId") Long userId);
}
