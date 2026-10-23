package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.common.PageResult;
import com.hospital.dto.RegistrationCreateDTO;
import com.hospital.entity.Registration;
import com.hospital.vo.RegistrationVO;

import java.time.LocalDate;
import java.util.List;

public interface RegistrationService extends IService<Registration> {

    RegistrationVO create(Long userId, RegistrationCreateDTO dto);

    PageResult<RegistrationVO> pageForUser(Long userId, List<Integer> statuses, int page, int size);

    RegistrationVO detail(Long id, Long userId);

    void cancel(Long userId, Long id, String reason);

    PageResult<RegistrationVO> pageForAdmin(List<Integer> statuses, LocalDate date, String keyword, int page, int size);

    void changeStatus(Long id, Integer status);
}
