package com.hospital.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.hospital.entity.Registration;
import com.hospital.vo.RegistrationVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.time.LocalDate;
import java.util.List;

@Mapper
public interface RegistrationMapper extends BaseMapper<Registration> {

    IPage<RegistrationVO> selectPageVo(IPage<RegistrationVO> page,
                                       @Param("userId") Long userId,
                                       @Param("statuses") List<Integer> statuses,
                                       @Param("date") LocalDate date,
                                       @Param("keyword") String keyword);

    RegistrationVO selectDetail(@Param("id") Long id);

    @Select("SELECT COUNT(*) FROM registration WHERE patient_id = #{patientId} AND schedule_id = #{scheduleId} " +
            "AND status IN (1, 2)")
    int countActive(@Param("patientId") Long patientId, @Param("scheduleId") Long scheduleId);

    @Select("SELECT COUNT(*) FROM registration WHERE schedule_id = #{scheduleId} AND status IN (1, 2)")
    int countActiveBySchedule(@Param("scheduleId") Long scheduleId);

    @Select("SELECT COUNT(*) FROM registration WHERE doctor_id = #{doctorId}")
    int countByDoctor(@Param("doctorId") Long doctorId);

    @Select("SELECT COUNT(*) FROM registration WHERE patient_id = #{patientId}")
    int countByPatient(@Param("patientId") Long patientId);
}
