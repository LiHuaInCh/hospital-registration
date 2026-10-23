package com.hospital.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("patient")
public class Patient {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    private String name;
    private String idCard;
    private String phone;
    private Integer gender;
    private Integer age;
    private String relationship;
    private Integer isDefault;

    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
