-- ============================================================
-- 医院门诊挂号与导诊服务平台 数据库初始化脚本
-- 适用于 MySQL 8.0，执行后即可直接启动后端
--   mysql -u root -p < database/init.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS `hospital`
    DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `hospital`;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `registration`;
DROP TABLE IF EXISTS `schedule`;
DROP TABLE IF EXISTS `doctor`;
DROP TABLE IF EXISTS `department`;
DROP TABLE IF EXISTS `patient`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id`          BIGINT       NOT NULL AUTO_INCREMENT,
  `username`    VARCHAR(50)  NOT NULL,
  `password`    VARCHAR(100) NOT NULL COMMENT 'BCrypt 密文，首次启动时把明文自动升级为密文',
  `real_name`   VARCHAR(50)  DEFAULT NULL,
  `phone`       VARCHAR(20)  DEFAULT NULL,
  `status`      TINYINT      NOT NULL DEFAULT 1 COMMENT '1-启用 0-禁用',
  `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_admin_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员';

CREATE TABLE `user` (
  `id`          BIGINT       NOT NULL AUTO_INCREMENT,
  `openid`      VARCHAR(100) NOT NULL COMMENT '微信 openid，演示环境用设备标识代替',
  `nickname`    VARCHAR(100) DEFAULT NULL,
  `avatar_url`  VARCHAR(500) DEFAULT NULL,
  `phone`       VARCHAR(20)  DEFAULT NULL,
  `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_openid` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='微信用户';

CREATE TABLE `patient` (
  `id`           BIGINT      NOT NULL AUTO_INCREMENT,
  `user_id`      BIGINT      NOT NULL,
  `name`         VARCHAR(50) NOT NULL,
  `id_card`      VARCHAR(18) NOT NULL,
  `phone`        VARCHAR(20) NOT NULL,
  `gender`       TINYINT     NOT NULL DEFAULT 1 COMMENT '1-男 2-女',
  `age`          INT         DEFAULT NULL,
  `relationship` VARCHAR(20) DEFAULT '本人',
  `is_default`   TINYINT     NOT NULL DEFAULT 0,
  `create_time`  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time`  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_patient_user_idcard` (`user_id`, `id_card`),
  KEY `idx_patient_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='就诊人';

CREATE TABLE `department` (
  `id`          BIGINT       NOT NULL AUTO_INCREMENT,
  `name`        VARCHAR(100) NOT NULL,
  `description` VARCHAR(500) DEFAULT NULL,
  `icon`        VARCHAR(255) DEFAULT NULL,
  `location`    VARCHAR(200) DEFAULT NULL,
  `phone`       VARCHAR(20)  DEFAULT NULL,
  `sort_order`  INT          NOT NULL DEFAULT 0,
  `status`      TINYINT      NOT NULL DEFAULT 1 COMMENT '1-启用 0-停用',
  `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_department_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='科室';

CREATE TABLE `doctor` (
  `id`               BIGINT        NOT NULL AUTO_INCREMENT,
  `department_id`    BIGINT        NOT NULL,
  `name`             VARCHAR(50)   NOT NULL,
  `gender`           TINYINT       NOT NULL DEFAULT 1,
  `title`            VARCHAR(50)   DEFAULT NULL,
  `specialty`        VARCHAR(500)  DEFAULT NULL,
  `description`      TEXT,
  `avatar`           VARCHAR(500)  DEFAULT NULL,
  `consultation_fee` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `status`           TINYINT       NOT NULL DEFAULT 1 COMMENT '1-在岗 0-离职',
  `create_time`      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time`      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_doctor_department` (`department_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='医生';

CREATE TABLE `schedule` (
  `id`          BIGINT      NOT NULL AUTO_INCREMENT,
  `doctor_id`   BIGINT      NOT NULL,
  `work_date`   DATE        NOT NULL,
  `time_slot`   VARCHAR(20) NOT NULL COMMENT '上午/下午/晚上',
  `start_time`  TIME        DEFAULT NULL,
  `end_time`    TIME        DEFAULT NULL,
  `total_count` INT         NOT NULL DEFAULT 30,
  `remain_count` INT        NOT NULL DEFAULT 30,
  `status`      TINYINT     NOT NULL DEFAULT 1 COMMENT '1-正常 2-停诊',
  `create_time` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_schedule_doctor_date_slot` (`doctor_id`, `work_date`, `time_slot`),
  KEY `idx_schedule_date` (`work_date`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='排班';

CREATE TABLE `registration` (
  `id`            BIGINT        NOT NULL AUTO_INCREMENT,
  `user_id`       BIGINT        NOT NULL,
  `patient_id`    BIGINT        NOT NULL,
  `schedule_id`   BIGINT        NOT NULL,
  `department_id` BIGINT        NOT NULL,
  `doctor_id`     BIGINT        NOT NULL,
  `work_date`     DATE          NOT NULL,
  `time_slot`     VARCHAR(20)   NOT NULL,
  `fee`           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `status`        TINYINT       NOT NULL DEFAULT 1 COMMENT '1-已预约 2-已签到 3-已完成 4-已取消',
  `cancel_reason` VARCHAR(255)  DEFAULT NULL,
  `create_time`   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time`   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_registration_user` (`user_id`, `status`),
  KEY `idx_registration_schedule` (`schedule_id`),
  KEY `idx_registration_date` (`work_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='挂号记录';

-- ------------------------------------------------------------
-- 初始数据
-- ------------------------------------------------------------

-- 默认管理员 admin / 123456（明文，后端首次启动时会自动替换为 BCrypt 密文）
INSERT INTO `admin` (`username`, `password`, `real_name`, `phone`)
VALUES ('admin', '123456', '系统管理员', '0571-88000000');

INSERT INTO `department` (`name`, `description`, `location`, `phone`, `sort_order`) VALUES
('呼吸内科',  '诊治感冒、流感、肺炎、哮喘、慢阻肺等呼吸系统疾病', '门诊楼 2 层 A 区', '0571-88000101', 1),
('心血管内科', '诊治高血压、冠心病、心律失常、心力衰竭等心血管疾病', '门诊楼 2 层 B 区', '0571-88000102', 2),
('消化内科',  '诊治胃炎、胃溃疡、肝炎、胰腺炎、肠炎等消化系统疾病', '门诊楼 3 层 A 区', '0571-88000103', 3),
('神经内科',  '诊治头痛、脑血管病、帕金森、癫痫、痴呆等神经系统疾病', '门诊楼 3 层 B 区', '0571-88000104', 4),
('骨科',      '诊治骨折、颈椎病、腰椎间盘突出、关节炎、运动损伤', '门诊楼 4 层 A 区', '0571-88000105', 5),
('皮肤科',    '诊治湿疹、荨麻疹、银屑病、痤疮、疱疹、过敏等皮肤病', '门诊楼 4 层 B 区', '0571-88000106', 6),
('眼科',      '诊治近视、白内障、青光眼、结膜炎、眼外伤', '门诊楼 5 层 A 区', '0571-88000107', 7),
('口腔科',    '诊治龋齿、牙周炎、口腔溃疡、拔牙、牙齿矫正', '门诊楼 5 层 B 区', '0571-88000108', 8),
('妇科',      '诊治月经不调、妇科炎症、子宫肌瘤、产前检查', '门诊楼 6 层 A 区', '0571-88000109', 9),
('儿科',      '诊治小儿感冒发热、肺炎、腹泻、生长发育评估', '门诊楼 6 层 B 区', '0571-88000110', 10),
('内分泌科',  '诊治糖尿病、甲亢、甲减、痛风、肥胖等代谢疾病', '门诊楼 7 层 A 区', '0571-88000111', 11),
('泌尿外科',  '诊治肾结石、尿路感染、前列腺疾病、膀胱肿瘤', '门诊楼 7 层 B 区', '0571-88000112', 12),
('急诊科',    '24 小时急诊，处理胸痛、急腹症、外伤、意识障碍等急症', '急诊楼 1 层', '0571-88000120', 0);

INSERT INTO `doctor` (`department_id`, `name`, `gender`, `title`, `specialty`, `description`, `consultation_fee`) VALUES
(1,  '张明远', 1, '主任医师',   '慢阻肺、支气管哮喘、肺部感染', '呼吸内科主任，从事临床工作 30 余年。', 50.00),
(1,  '李芳华', 2, '副主任医师', '支气管哮喘、过敏性鼻炎、慢性咳嗽', '医学博士，擅长呼吸系统过敏性疾病。', 30.00),
(2,  '王建国', 1, '主任医师',   '冠心病介入、高血压、心力衰竭', '心血管内科学科带头人，年介入手术 500 余例。', 50.00),
(2,  '陈晓燕', 2, '主治医师',   '高血压、心律失常、心肌病', '对常见心血管疾病诊疗经验丰富。', 20.00),
(3,  '刘伟强', 1, '主任医师',   '消化内镜、消化道早癌筛查、肝病', '消化内科主任，擅长内镜下微创治疗。', 50.00),
(3,  '赵雪梅', 2, '副主任医师', '功能性胃肠病、炎症性肠病、幽门螺杆菌', '从事消化内科工作 15 年。', 30.00),
(4,  '孙志刚', 1, '主任医师',   '脑血管病、帕金森病、癫痫', '神经内科主任，擅长脑血管病规范化诊疗。', 50.00),
(5,  '周建国', 1, '主任医师',   '脊柱外科、关节置换、运动损伤', '骨科主任，擅长脊柱微创与关节置换。', 50.00),
(5,  '吴小丽', 2, '主治医师',   '骨折复位、骨质疏松、颈肩腰腿痛', '骨科青年骨干。', 20.00),
(6,  '郑明明', 2, '副主任医师', '痤疮、湿疹、银屑病、皮肤美容', '擅长中西医结合治疗皮肤病。', 30.00),
(7,  '冯大宝', 1, '主任医师',   '白内障手术、青光眼、眼底病', '眼科主任，累计完成白内障手术万余例。', 50.00),
(8,  '何丽丽', 2, '主治医师',   '牙体牙髓病、牙周病、儿童牙病', '诊疗细致，擅长儿童牙科。', 20.00),
(9,  '马红霞', 2, '主任医师',   '妇科肿瘤、妇科内分泌、不孕不育', '妇科主任，擅长妇科微创手术。', 50.00),
(10, '黄小明', 1, '副主任医师', '小儿呼吸系统疾病、新生儿疾病', '儿科副主任，对小儿疑难杂症经验丰富。', 30.00),
(10, '林晓芳', 2, '主治医师',   '小儿消化系统疾病、生长发育、预防接种', '擅长儿童常见病与保健。', 20.00),
(11, '钱文博', 1, '主任医师',   '糖尿病及并发症、甲状腺疾病、痛风', '内分泌科主任。', 50.00),
(12, '杨永强', 1, '副主任医师', '泌尿系结石微创、前列腺疾病、男科', '擅长经皮肾镜与输尿管软镜手术。', 30.00),
(13, '陆志远', 1, '副主任医师', '急危重症抢救、多发伤、急性中毒', '急诊科副主任，常年值守一线。', 30.00),
(13, '沈佳',   2, '主治医师',   '急诊内科、急性胸痛、急腹症', '急诊内科骨干医师。', 20.00);

-- 未来 7 天的排班：按医生与星期错开，避免每人都排满
INSERT INTO `schedule` (`doctor_id`, `work_date`, `time_slot`, `start_time`, `end_time`, `total_count`, `remain_count`, `status`)
SELECT d.`id`,
       DATE_ADD(CURDATE(), INTERVAL n.`d` DAY),
       s.`slot`, s.`st`, s.`et`, s.`total`, s.`total`, 1
FROM `doctor` d
CROSS JOIN (
    SELECT 0 AS `d` UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
) n
CROSS JOIN (
    SELECT '上午' AS `slot`, '08:00:00' AS `st`, '12:00:00' AS `et`, 30 AS `total`
    UNION ALL SELECT '下午', '14:00:00', '18:00:00', 24
    UNION ALL SELECT '晚上', '18:00:00', '21:00:00', 16
) s
WHERE d.`status` = 1
  AND MOD(d.`id` * 3 + n.`d` * 7, 4) <> 0;

-- 演示账号：设备登录时使用任意设备标识，即可创建一个新用户；
-- 下面这条用户与就诊人用于在导诊/挂号接口测试时直接引用。
INSERT INTO `user` (`openid`, `nickname`) VALUES ('wx_demo_001', '演示用户');
INSERT INTO `patient` (`user_id`, `name`, `id_card`, `phone`, `gender`, `age`, `relationship`, `is_default`) VALUES
(1, '张伟', '110101199003070011', '13800138000', 1, 36, '本人', 1);
