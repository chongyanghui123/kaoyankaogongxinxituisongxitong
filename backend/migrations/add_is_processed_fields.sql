-- 为 common_db 数据库中的 push_logs 表添加 is_processed 字段
USE common_db;
ALTER TABLE push_logs ADD COLUMN IF NOT EXISTS is_processed TINYINT(1) DEFAULT 0 COMMENT "是否处理: 1-是, 0-否";

-- 为 kaoyan_db 数据库中的 kaoyan_info 表添加 is_processed 字段
USE kaoyan_db;
ALTER TABLE kaoyan_info ADD COLUMN IF NOT EXISTS is_processed TINYINT(1) DEFAULT 0 COMMENT "是否处理: 1-是, 0-否";

-- 为 kaogong_db 数据库中的 kaogong_info 表添加 is_processed 字段
USE kaogong_db;
ALTER TABLE kaogong_info ADD COLUMN IF NOT EXISTS is_processed TINYINT(1) DEFAULT 0 COMMENT "是否处理: 1-是, 0-否";
