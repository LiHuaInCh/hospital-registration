package com.hospital.controller;

import com.hospital.common.R;
import com.hospital.entity.Schedule;
import com.hospital.service.ScheduleService;
import com.hospital.vo.DateOptionVO;
import com.hospital.vo.ScheduleVO;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.time.format.TextStyle;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@RestController
@RequestMapping("/api/schedule")
@RequiredArgsConstructor
public class ScheduleController {

    private final ScheduleService scheduleService;

    @Value("${app.booking.bookable-days:7}")
    private int bookableDays;

    @GetMapping("/list")
    public R<List<ScheduleVO>> list(@RequestParam Long doctorId) {
        return R.ok(scheduleService.listBookable(doctorId));
    }

    @GetMapping("/detail")
    public R<ScheduleVO> detail(@RequestParam Long id) {
        return R.ok(scheduleService.detail(id));
    }

    @GetMapping("/dates")
    public R<List<DateOptionVO>> dates() {
        List<DateOptionVO> options = new ArrayList<>();
        LocalDate today = LocalDate.now();
        int days = Math.max(1, bookableDays);
        for (int i = 0; i < days; i++) {
            LocalDate date = today.plusDays(i);
            DateOptionVO option = new DateOptionVO();
            option.setDate(date);
            option.setWeekday(date.getDayOfWeek().getDisplayName(TextStyle.SHORT, Locale.CHINA));
            option.setToday(i == 0);
            options.add(option);
        }
        return R.ok(options);
    }

    @PostMapping("/add")
    public R<ScheduleVO> add(@RequestBody Schedule schedule) {
        return R.ok(scheduleService.create(schedule));
    }

    @PutMapping("/update")
    public R<ScheduleVO> update(@RequestBody Schedule schedule) {
        if (schedule.getId() == null) {
            return R.fail("缺少排班标识");
        }
        return R.ok(scheduleService.update(schedule.getId(), schedule));
    }

    @DeleteMapping("/delete")
    public R<Void> delete(@RequestParam Long id) {
        scheduleService.delete(id);
        return R.ok();
    }
}
