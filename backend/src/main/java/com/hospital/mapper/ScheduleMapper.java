package com.hospital.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hospital.entity.Schedule;
import com.hospital.vo.ScheduleVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.time.LocalDate;
import java.util.List;

@Mapper
public interface ScheduleMapper extends BaseMapper<Schedule> {

    String SELECT_WITH_DOCTOR = "SELECT s.id, s.doctor_id, s.work_date, s.time_slot, s.start_time, s.end_time, " +
            "s.total_count, s.remain_count, s.status, d.name AS doctor_name, d.title, " +
            "d.consultation_fee, dept.id AS department_id, dept.name AS department_name " +
            "FROM schedule s JOIN doctor d ON d.id = s.doctor_id " +
            "LEFT JOIN department dept ON dept.id = d.department_id ";

    @Select(SELECT_WITH_DOCTOR + "WHERE s.doctor_id = #{doctorId} AND s.work_date BETWEEN #{from} AND #{to} " +
            "AND s.status = 1 AND s.remain_count > 0 " +
            "AND (s.work_date > CURDATE() OR s.start_time IS NULL OR s.start_time > CURTIME()) " +
            "ORDER BY s.work_date ASC, s.start_time ASC")
    List<ScheduleVO> selectBookable(@Param("doctorId") Long doctorId,
                                    @Param("from") LocalDate from,
                                    @Param("to") LocalDate to);

    @Select("<script>" + SELECT_WITH_DOCTOR +
            "<where>" +
            "<if test='date != null'>AND s.work_date = #{date}</if>" +
            "<if test='departmentId != null'>AND dept.id = #{departmentId}</if>" +
            "<if test='status != null'>AND s.status = #{status}</if>" +
            "</where> ORDER BY s.work_date DESC, s.start_time ASC, d.name ASC" +
            "</script>")
    List<ScheduleVO> selectForAdmin(@Param("date") LocalDate date,
                                    @Param("departmentId") Long departmentId,
                                    @Param("status") Integer status);

    @Select(SELECT_WITH_DOCTOR + "WHERE s.id = #{id}")
    ScheduleVO selectDetail(@Param("id") Long id);

    /**
     * 原子扣减，避免并发下超卖。
     */
    @Update("UPDATE schedule SET remain_count = remain_count - 1 " +
            "WHERE id = #{id} AND status = 1 AND remain_count > 0")
    int decreaseStock(@Param("id") Long id);

    @Update("UPDATE schedule SET remain_count = remain_count + 1 " +
            "WHERE id = #{id} AND remain_count < total_count")
    int increaseStock(@Param("id") Long id);
}
