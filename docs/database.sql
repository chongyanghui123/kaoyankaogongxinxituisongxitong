-- 双赛道情报通数据库设计
-- 数据库版本: MySQL 8.0+
-- 创建时间: 2026-04-08
-- 作者: 双赛道情报通开发团队

/* ==========================================
   公共库 (common_db) - 用户、订单、系统配置
   ========================================== */
CREATE DATABASE IF NOT EXISTS `common_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `common_db`;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `email` VARCHAR(100) NOT NULL COMMENT '邮箱',
    `phone` VARCHAR(20) NOT NULL COMMENT '手机号',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `avatar` VARCHAR(255) NULL COMMENT '头像URL',
    `real_name` VARCHAR(50) NULL COMMENT '真实姓名',
    `id_card` VARCHAR(20) NULL COMMENT '身份证号',
    `gender` TINYINT DEFAULT 0 COMMENT '性别: 0-未知, 1-男, 2-女',
    `birthdate` DATE NULL COMMENT '出生日期',
    `register_ip` VARCHAR(45) NULL COMMENT '注册IP',
    `last_login_ip` VARCHAR(45) NULL COMMENT '最后登录IP',
    `last_login_time` DATETIME NULL COMMENT '最后登录时间',
    `is_active` TINYINT DEFAULT 1 COMMENT '是否激活: 1-激活, 0-未激活',
    `is_admin` TINYINT DEFAULT 0 COMMENT '是否管理员: 1-是, 0-否',
    `is_vip` TINYINT DEFAULT 0 COMMENT '是否VIP: 1-是, 0-否',
    `vip_start_time` DATETIME NULL COMMENT 'VIP开始时间',
    `vip_end_time` DATETIME NULL COMMENT 'VIP结束时间',
    `vip_type` TINYINT DEFAULT 0 COMMENT 'VIP类型: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP',
    `trial_status` TINYINT DEFAULT 0 COMMENT '试用状态: 0-未试用, 1-试用中, 2-已过期',
    `trial_start_time` DATETIME NULL COMMENT '试用开始时间',
    `trial_end_time` DATETIME NULL COMMENT '试用结束时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_email` (`email`),
    UNIQUE KEY `uk_phone` (`phone`),
    KEY `idx_vip_type` (`vip_type`),
    KEY `idx_vip_end_time` (`vip_end_time`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 2. 用户订阅配置表
CREATE TABLE IF NOT EXISTS `user_subscriptions` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订阅ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `subscribe_type` TINYINT NOT NULL COMMENT '订阅类型: 1-考研, 2-考公, 3-双赛道',
    `status` TINYINT DEFAULT 1 COMMENT '订阅状态: 1-有效, 0-无效',
    `config_json` JSON NULL COMMENT '订阅配置JSON',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_type` (`user_id`, `subscribe_type`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_subscribe_type` (`subscribe_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户订阅配置表';

-- 3. 用户关键词表
CREATE TABLE IF NOT EXISTS `user_keywords` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '关键词ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `keyword` VARCHAR(100) NOT NULL COMMENT '关键词',
    `category` TINYINT NOT NULL COMMENT '分类: 1-考研, 2-考公',
    `is_active` TINYINT DEFAULT 1 COMMENT '是否启用: 1-是, 0-否',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_keyword` (`user_id`, `keyword`, `category`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户关键词表';

-- 4. 用户已读信息表
CREATE TABLE IF NOT EXISTS `user_read_info` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '已读ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `info_id` BIGINT UNSIGNED NOT NULL COMMENT '信息ID',
    `category` TINYINT NOT NULL COMMENT '分类: 1-考研, 2-考公',
    `read_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '阅读时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_info` (`user_id`, `info_id`, `category`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_info_id` (`info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户已读信息表';

-- 5. 用户收藏信息表
CREATE TABLE IF NOT EXISTS `user_favorites` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `info_id` BIGINT UNSIGNED NOT NULL COMMENT '信息ID',
    `category` TINYINT NOT NULL COMMENT '分类: 1-考研, 2-考公',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_info` (`user_id`, `info_id`, `category`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_info_id` (`info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏信息表';

-- 6. 订单表
CREATE TABLE IF NOT EXISTS `orders` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单ID',
    `order_no` VARCHAR(32) NOT NULL COMMENT '订单编号',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `product_id` BIGINT UNSIGNED NOT NULL COMMENT '产品ID',
    `product_name` VARCHAR(100) NOT NULL COMMENT '产品名称',
    `price` DECIMAL(10,2) NOT NULL COMMENT '价格',
    `quantity` INT DEFAULT 1 COMMENT '数量',
    `total_amount` DECIMAL(10,2) NOT NULL COMMENT '总金额',
    `payment_method` TINYINT NOT NULL COMMENT '支付方式: 1-微信支付, 2-支付宝',
    `payment_status` TINYINT DEFAULT 0 COMMENT '支付状态: 0-待支付, 1-已支付, 2-已取消, 3-已退款',
    `trade_no` VARCHAR(100) NULL COMMENT '支付平台交易号',
    `payment_time` DATETIME NULL COMMENT '支付时间',
    `refund_time` DATETIME NULL COMMENT '退款时间',
    `expire_time` DATETIME NULL COMMENT '过期时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_order_no` (`order_no`),
    UNIQUE KEY `uk_trade_no` (`trade_no`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_payment_status` (`payment_status`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- 7. 产品/套餐表
CREATE TABLE IF NOT EXISTS `products` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '产品ID',
    `name` VARCHAR(100) NOT NULL COMMENT '产品名称',
    `description` TEXT NULL COMMENT '产品描述',
    `price` DECIMAL(10,2) NOT NULL COMMENT '价格',
    `original_price` DECIMAL(10,2) NULL COMMENT '原价',
    `type` TINYINT NOT NULL COMMENT '产品类型: 1-考研VIP, 2-考公VIP, 3-双赛道VIP',
    `duration` INT NOT NULL COMMENT '有效期(天)',
    `features` JSON NULL COMMENT '产品特色JSON',
    `status` TINYINT DEFAULT 1 COMMENT '状态: 1-上架, 0-下架',
    `sort_order` INT DEFAULT 0 COMMENT '排序',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_type` (`type`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='产品/套餐表';

-- 8. 系统配置表
CREATE TABLE IF NOT EXISTS `system_config` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '配置ID',
    `config_key` VARCHAR(100) NOT NULL COMMENT '配置键',
    `config_value` TEXT NULL COMMENT '配置值',
    `config_type` TINYINT DEFAULT 0 COMMENT '配置类型: 0-字符串, 1-数字, 2-布尔值, 3-JSON',
    `description` VARCHAR(255) NULL COMMENT '配置描述',
    `is_system` TINYINT DEFAULT 0 COMMENT '是否系统配置: 1-是, 0-否',
    `status` TINYINT DEFAULT 1 COMMENT '状态: 1-启用, 0-禁用',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 9. 推送模板表
CREATE TABLE IF NOT EXISTS `push_templates` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '模板ID',
    `name` VARCHAR(100) NOT NULL COMMENT '模板名称',
    `type` TINYINT NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
    `template_id` VARCHAR(100) NOT NULL COMMENT '第三方模板ID',
    `template_content` TEXT NULL COMMENT '模板内容',
    `status` TINYINT DEFAULT 1 COMMENT '状态: 1-启用, 0-禁用',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_type` (`type`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推送模板表';

-- 10. 推送日志表
CREATE TABLE IF NOT EXISTS `push_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
    `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `info_id` BIGINT UNSIGNED NOT NULL COMMENT '信息ID',
    `category` TINYINT NOT NULL COMMENT '分类: 1-考研, 2-考公',
    `push_type` TINYINT NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
    `push_status` TINYINT NOT NULL COMMENT '推送状态: 1-成功, 0-失败',
    `push_content` TEXT NULL COMMENT '推送内容',
    `error_msg` TEXT NULL COMMENT '错误信息',
    `push_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '推送时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_info_id` (`info_id`),
    KEY `idx_push_type` (`push_type`),
    KEY `idx_push_status` (`push_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推送日志表';

/* ==========================================
   考研库 (kaoyan_db) - 考研相关数据
   ========================================== */
CREATE DATABASE IF NOT EXISTS `kaoyan_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `kaoyan_db`;

-- 1. 考研信息表
CREATE TABLE IF NOT EXISTS `kaoyan_info` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '信息ID',
    `title` VARCHAR(500) NOT NULL COMMENT '标题',
    `source` VARCHAR(100) NOT NULL COMMENT '来源',
    `source_url` VARCHAR(500) NULL COMMENT '来源链接',
    `publish_time` DATETIME NOT NULL COMMENT '发布时间',
    `content` LONGTEXT NULL COMMENT '内容',
    `url` VARCHAR(500) NOT NULL COMMENT '原文链接',
    `tags` VARCHAR(255) NULL COMMENT '标签(逗号分隔)',
    `urgency_level` TINYINT DEFAULT 0 COMMENT '紧急度: 0-普通, 1-重要, 2-紧急, 3-非常紧急',
    `category` TINYINT DEFAULT 0 COMMENT '分类: 0-普通通知, 1-调剂, 2-扩招, 3-复试线, 4-招生简章, 5-时间节点',
    `province` VARCHAR(50) NULL COMMENT '省份',
    `school` VARCHAR(100) NULL COMMENT '院校',
    `major` VARCHAR(100) NULL COMMENT '专业',
    `degree_type` TINYINT NULL COMMENT '学位类型: 1-学硕, 2-专硕',
    `study_type` TINYINT NULL COMMENT '学习方式: 1-全日制, 2-非全日制',
    `is_valid` TINYINT DEFAULT 1 COMMENT '是否有效: 1-有效, 0-无效',
    `is_top` TINYINT DEFAULT 0 COMMENT '是否置顶: 1-是, 0-否',
    `is_excellent` TINYINT DEFAULT 0 COMMENT '是否加精: 1-是, 0-否',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `like_count` INT DEFAULT 0 COMMENT '点赞次数',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_url` (`url`),
    KEY `idx_publish_time` (`publish_time`),
    KEY `idx_category` (`category`),
    KEY `idx_urgency_level` (`urgency_level`),
    KEY `idx_province` (`province`),
    KEY `idx_school` (`school`),
    KEY `idx_major` (`major`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研信息表';

-- 2. 考研爬虫配置表
CREATE TABLE IF NOT EXISTS `kaoyan_crawler_config` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '配置ID',
    `name` VARCHAR(100) NOT NULL COMMENT '配置名称',
    `url` VARCHAR(500) NOT NULL COMMENT '监控网址',
    `selector` TEXT NULL COMMENT '页面选择器',
    `parse_rules` JSON NULL COMMENT '解析规则',
    `interval` INT DEFAULT 10 COMMENT '抓取间隔(分钟)',
    `status` TINYINT DEFAULT 1 COMMENT '状态: 1-启用, 0-禁用',
    `priority` TINYINT DEFAULT 0 COMMENT '优先级: 0-普通, 1-高, 2-非常高',
    `last_crawl_time` DATETIME NULL COMMENT '最后抓取时间',
    `next_crawl_time` DATETIME NULL COMMENT '下次抓取时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_url` (`url`),
    KEY `idx_status` (`status`),
    KEY `idx_priority` (`priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研爬虫配置表';

-- 3. 考研爬虫日志表
CREATE TABLE IF NOT EXISTS `kaoyan_crawler_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
    `config_id` BIGINT UNSIGNED NOT NULL COMMENT '配置ID',
    `url` VARCHAR(500) NOT NULL COMMENT '抓取网址',
    `status` TINYINT NOT NULL COMMENT '状态: 1-成功, 0-失败',
    `info_count` INT DEFAULT 0 COMMENT '抓取信息数量',
    `error_msg` TEXT NULL COMMENT '错误信息',
    `crawl_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '抓取时间',
    PRIMARY KEY (`id`),
    KEY `idx_config_id` (`config_id`),
    KEY `idx_status` (`status`),
    KEY `idx_crawl_time` (`crawl_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研爬虫日志表';

/* ==========================================
   考公库 (kaogong_db) - 考公相关数据
   ========================================== */
CREATE DATABASE IF NOT EXISTS `kaogong_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `kaogong_db`;

-- 1. 考公信息表
CREATE TABLE IF NOT EXISTS `kaogong_info` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '信息ID',
    `title` VARCHAR(500) NOT NULL COMMENT '标题',
    `source` VARCHAR(100) NOT NULL COMMENT '来源',
    `source_url` VARCHAR(500) NULL COMMENT '来源链接',
    `publish_time` DATETIME NOT NULL COMMENT '发布时间',
    `content` LONGTEXT NULL COMMENT '内容',
    `url` VARCHAR(500) NOT NULL COMMENT '原文链接',
    `tags` VARCHAR(255) NULL COMMENT '标签(逗号分隔)',
    `urgency_level` TINYINT DEFAULT 0 COMMENT '紧急度: 0-普通, 1-重要, 2-紧急, 3-非常紧急',
    `category` TINYINT DEFAULT 0 COMMENT '分类: 0-普通通知, 1-公告, 2-职位表, 3-报名, 4-缴费, 5-三不限, 6-应届生, 7-竞争比',
    `province` VARCHAR(50) NULL COMMENT '省份',
    `position_type` VARCHAR(100) NULL COMMENT '岗位类别',
    `major` VARCHAR(100) NULL COMMENT '专业',
    `education` VARCHAR(50) NULL COMMENT '学历要求',
    `is_fresh_graduate` TINYINT NULL COMMENT '是否应届生岗: 1-是, 0-否',
    `is_unlimited` TINYINT NULL COMMENT '是否三不限: 1-是, 0-否',
    `competition_ratio` DECIMAL(10,2) NULL COMMENT '竞争比',
    `is_valid` TINYINT DEFAULT 1 COMMENT '是否有效: 1-有效, 0-无效',
    `is_top` TINYINT DEFAULT 0 COMMENT '是否置顶: 1-是, 0-否',
    `is_excellent` TINYINT DEFAULT 0 COMMENT '是否加精: 1-是, 0-否',
    `view_count` INT DEFAULT 0 COMMENT '浏览次数',
    `like_count` INT DEFAULT 0 COMMENT '点赞次数',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_url` (`url`),
    KEY `idx_publish_time` (`publish_time`),
    KEY `idx_category` (`category`),
    KEY `idx_urgency_level` (`urgency_level`),
    KEY `idx_province` (`province`),
    KEY `idx_position_type` (`position_type`),
    KEY `idx_major` (`major`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考公信息表';

-- 2. 考公爬虫配置表
CREATE TABLE IF NOT EXISTS `kaogong_crawler_config` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '配置ID',
    `name` VARCHAR(100) NOT NULL COMMENT '配置名称',
    `url` VARCHAR(500) NOT NULL COMMENT '监控网址',
    `selector` TEXT NULL COMMENT '页面选择器',
    `parse_rules` JSON NULL COMMENT '解析规则',
    `interval` INT DEFAULT 10 COMMENT '抓取间隔(分钟)',
    `status` TINYINT DEFAULT 1 COMMENT '状态: 1-启用, 0-禁用',
    `priority` TINYINT DEFAULT 0 COMMENT '优先级: 0-普通, 1-高, 2-非常高',
    `last_crawl_time` DATETIME NULL COMMENT '最后抓取时间',
    `next_crawl_time` DATETIME NULL COMMENT '下次抓取时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_url` (`url`),
    KEY `idx_status` (`status`),
    KEY `idx_priority` (`priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考公爬虫配置表';

-- 3. 考公爬虫日志表
CREATE TABLE IF NOT EXISTS `kaogong_crawler_logs` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
    `config_id` BIGINT UNSIGNED NOT NULL COMMENT '配置ID',
    `url` VARCHAR(500) NOT NULL COMMENT '抓取网址',
    `status` TINYINT NOT NULL COMMENT '状态: 1-成功, 0-失败',
    `info_count` INT DEFAULT 0 COMMENT '抓取信息数量',
    `error_msg` TEXT NULL COMMENT '错误信息',
    `crawl_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '抓取时间',
    PRIMARY KEY (`id`),
    KEY `idx_config_id` (`config_id`),
    KEY `idx_status` (`status`),
    KEY `idx_crawl_time` (`crawl_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考公爬虫日志表';

/* ==========================================
   初始化数据
   ========================================== */
-- 初始化系统配置
USE `common_db`;

-- 插入系统配置
INSERT INTO `system_config` (`config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`) VALUES
('crawler_interval', '10', 1, '爬虫默认抓取间隔(分钟)', 1, 1),
('max_concurrent_crawlers', '5', 1, '最大并发爬虫数', 1, 1),
('push_enabled', '1', 2, '是否启用推送功能', 1, 1),
('trial_days', '3', 1, '免费试用天数', 1, 1),
('wechat_app_id', '', 0, '微信公众号AppID', 0, 0),
('wechat_app_secret', '', 0, '微信公众号AppSecret', 0, 0),
('alipay_app_id', '', 0, '支付宝AppID', 0, 0),
('alipay_private_key', '', 0, '支付宝私钥', 0, 0);

-- 插入默认产品套餐
INSERT INTO `products` (`name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`) VALUES
('考研VIP月卡', '考研赛道全方位情报监控，包含研招网、目标院校等关键信息推送', 39.00, 59.00, 1, 30, '{"features":["考研全赛道监控","实时推送","智能分类","优先级提醒","3天免费试用"]}', 1, 1),
('考研VIP季卡', '考研赛道季度订阅，优惠更多，包含所有月卡功能', 99.00, 177.00, 1, 90, '{"features":["考研全赛道监控","实时推送","智能分类","优先级提醒","季度数据统计"]}', 1, 2),
('考研VIP年卡', '考研赛道年度订阅，最优惠选择，包含所有月卡功能', 299.00, 708.00, 1, 365, '{"features":["考研全赛道监控","实时推送","智能分类","优先级提醒","年度数据分析","专属客服"]}', 1, 3),
('考公VIP月卡', '考公赛道全方位情报监控，包含国考、省考等关键信息推送', 49.00, 69.00, 2, 30, '{"features":["考公全赛道监控","实时推送","智能分类","优先级提醒","3天免费试用"]}', 1, 4),
('考公VIP季卡', '考公赛道季度订阅，优惠更多，包含所有月卡功能', 119.00, 207.00, 2, 90, '{"features":["考公全赛道监控","实时推送","智能分类","优先级提醒","季度数据统计"]}', 1, 5),
('考公VIP年卡', '考公赛道年度订阅，最优惠选择，包含所有月卡功能', 359.00, 828.00, 2, 365, '{"features":["考公全赛道监控","实时推送","智能分类","优先级提醒","年度数据分析","专属客服"]}', 1, 6),
('双赛道VIP年卡', '考研+考公双赛道全方位情报监控，性价比最高', 499.00, 658.00, 3, 365, '{"features":["双赛道全监控","实时推送","智能分类","优先级提醒","年度数据分析","专属客服","双赛道对比"]}', 1, 0);

-- 插入默认推送模板
INSERT INTO `push_templates` (`name`, `type`, `template_id`, `template_content`, `status`) VALUES
('考研情报提醒', 1, '', '您关注的考研信息已更新：{{title}}，来源：{{source}}，发布时间：{{publish_time}}，点击查看详情：{{url}}', 1),
('考公情报提醒', 1, '', '您关注的考公信息已更新：{{title}}，来源：{{source}}，发布时间：{{publish_time}}，点击查看详情：{{url}}', 1);

-- 创建管理员用户(密码: 123456)
INSERT INTO `users` (`username`, `email`, `phone`, `password_hash`, `real_name`, `is_active`, `is_admin`) VALUES
('admin', 'admin@shuangsai.com', '13800138000', '$2b$12$9tW3eWf5Z6xQ7cV8bN9mK0lJ1kH2jG3fD4sA5dF6gH7jK8lJ9kL0', '系统管理员', 1, 1);

-- 插入默认爬虫配置
USE `kaoyan_db`;
INSERT INTO `kaoyan_crawler_config` (`name`, `url`, `selector`, `parse_rules`, `interval`, `status`, `priority`) VALUES
('研招网-考研政策', 'https://yz.chsi.com.cn/', 'div.news-list', '{"title":"h3 a","time":".time","content":".summary","link":"h3 a@href"}', 10, 1, 2),
('中国教育考试网-考研', 'https://www.neea.edu.cn/', '.exam-news', '{"title":".news-title","time":".publish-time","content":".news-content","link":".news-link"}', 15, 1, 1);

USE `kaogong_db`;
INSERT INTO `kaogong_crawler_config` (`name`, `url`, `selector`, `parse_rules`, `interval`, `status`, `priority`) VALUES
('国家公务员局-国考公告', 'http://www.scs.gov.cn/', '.notice-list', '{"title":"a.title","time":".publish-date","content":".summary","link":"a@href"}', 10, 1, 2),
('中国人事考试网-公务员', 'https://www.cpta.com.cn/', '.news-list', '{"title":".news-title","time":".publish-time","content":".news-content","link":".news-link"}', 15, 1, 1);

/* ==========================================
   创建视图和存储过程
   ========================================== */
-- 创建用户订阅视图
USE `common_db`;
CREATE OR REPLACE VIEW `user_subscription_view` AS
SELECT 
    u.`id` AS `user_id`,
    u.`username`,
    u.`email`,
    u.`phone`,
    u.`vip_type`,
    u.`vip_start_time`,
    u.`vip_end_time`,
    u.`trial_status`,
    u.`trial_start_time`,
    u.`trial_end_time`,
    us.`subscribe_type`,
    us.`status` AS `subscribe_status`,
    us.`config_json`
FROM `users` u
LEFT JOIN `user_subscriptions` us ON u.`id` = us.`user_id`;

-- 创建订单统计视图
CREATE OR REPLACE VIEW `order_statistics_view` AS
SELECT 
    DATE(`created_at`) AS `date`,
    COUNT(*) AS `total_orders`,
    SUM(`total_amount`) AS `total_amount`,
    COUNT(CASE WHEN `payment_status` = 1 THEN 1 END) AS `paid_orders`,
    SUM(CASE WHEN `payment_status` = 1 THEN `total_amount` ELSE 0 END) AS `paid_amount`,
    SUM(CASE WHEN `payment_status` = 3 THEN `total_amount` ELSE 0 END) AS `refund_amount`
FROM `orders`
GROUP BY DATE(`created_at`);

-- 创建存储过程：检查VIP状态
DELIMITER //
CREATE PROCEDURE `check_vip_status`()
BEGIN
    UPDATE `users` 
    SET `is_vip` = CASE 
        WHEN `vip_end_time` > NOW() THEN 1 
        ELSE 0 
    END;
END //
DELIMITER ;

-- 创建存储过程：发送过期提醒
DELIMITER //
CREATE PROCEDURE `send_vip_expiration_reminders`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_user_id BIGINT;
    DECLARE v_email VARCHAR(100);
    DECLARE v_phone VARCHAR(20);
    DECLARE v_vip_end_time DATETIME;
    
    -- 定义游标
    DECLARE cur CURSOR FOR 
        SELECT `id`, `email`, `phone`, `vip_end_time` 
        FROM `users` 
        WHERE `vip_end_time` BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 3 DAY) 
        AND `is_vip` = 1;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_user_id, v_email, v_phone, v_vip_end_time;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- 这里可以添加发送提醒的逻辑
        -- 暂时只记录到日志表
        INSERT INTO `push_logs` (`user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`)
        VALUES (v_user_id, 0, 0, 1, 0, CONCAT('您的VIP将于', DATE_FORMAT(v_vip_end_time, '%Y-%m-%d'), '过期，请及时续费'));
    END LOOP;
    
    CLOSE cur;
END //
DELIMITER ;

/* ==========================================
   创建事件调度器
   ========================================== */
-- 启用事件调度器
SET GLOBAL event_scheduler = ON;

-- 创建每天检查VIP状态的事件
CREATE EVENT IF NOT EXISTS `check_vip_status_daily`
ON SCHEDULE EVERY 1 DAY STARTS '2026-04-08 00:00:00'
ON COMPLETION PRESERVE
DO
    CALL `check_vip_status`();

-- 创建每天发送过期提醒的事件
CREATE EVENT IF NOT EXISTS `send_vip_expiration_reminders_daily`
ON SCHEDULE EVERY 1 DAY STARTS '2026-04-08 09:00:00'
ON COMPLETION PRESERVE
DO
    CALL `send_vip_expiration_reminders`();

-- 创建每小时统计爬虫数据的事件
CREATE EVENT IF NOT EXISTS `statistic_crawler_data_hourly`
ON SCHEDULE EVERY 1 HOUR STARTS '2026-04-08 00:00:00'
ON COMPLETION PRESERVE
DO
    BEGIN
        -- 这里可以添加爬虫数据统计逻辑
    END;

/* ==========================================
   权限配置
   ========================================== */
-- 创建数据库用户
CREATE USER IF NOT EXISTS 'shuangsai_user'@'%' IDENTIFIED BY 'ShuangSai@2024';

-- 授权
GRANT ALL PRIVILEGES ON `common_db`.* TO 'shuangsai_user'@'%';
GRANT ALL PRIVILEGES ON `kaoyan_db`.* TO 'shuangsai_user'@'%';
GRANT ALL PRIVILEGES ON `kaogong_db`.* TO 'shuangsai_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 优化表结构
OPTIMIZE TABLE `common_db`.`users`;
OPTIMIZE TABLE `common_db`.`orders`;
OPTIMIZE TABLE `kaoyan_db`.`kaoyan_info`;
OPTIMIZE TABLE `kaogong_db`.`kaogong_info`;