package com.hospital.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.hospital.entity.Admin;
import com.hospital.vo.LoginVO;

public interface AdminService extends IService<Admin> {

    LoginVO login(String username, String password);
}
