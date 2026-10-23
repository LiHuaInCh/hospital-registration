package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.dto.WxLoginDTO;
import com.hospital.entity.User;
import com.hospital.vo.LoginVO;

public interface UserService extends IService<User> {

    LoginVO login(WxLoginDTO dto);
}
