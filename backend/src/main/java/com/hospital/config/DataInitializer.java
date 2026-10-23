package com.hospital.config;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.hospital.entity.Admin;
import com.hospital.mapper.AdminMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * 启动时保证管理员可用：
 * - 没有管理员时创建默认账号 admin / 123456；
 * - 历史库里的明文密码自动升级为 BCrypt。
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements ApplicationRunner {

    private static final String DEFAULT_USERNAME = "admin";
    private static final String DEFAULT_PASSWORD = "123456";

    private final AdminMapper adminMapper;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(ApplicationArguments args) {
        Admin admin = adminMapper.selectOne(new LambdaQueryWrapper<Admin>()
                .eq(Admin::getUsername, DEFAULT_USERNAME));

        if (admin == null) {
            Admin created = new Admin();
            created.setUsername(DEFAULT_USERNAME);
            created.setPassword(passwordEncoder.encode(DEFAULT_PASSWORD));
            created.setRealName("系统管理员");
            created.setStatus(1);
            adminMapper.insert(created);
            log.info("已创建默认管理员账号 {}", DEFAULT_USERNAME);
            return;
        }

        if (admin.getPassword() != null && !admin.getPassword().startsWith("$2")) {
            admin.setPassword(passwordEncoder.encode(admin.getPassword()));
            adminMapper.updateById(admin);
            log.info("管理员 {} 的密码已升级为 BCrypt", DEFAULT_USERNAME);
        }
    }
}
