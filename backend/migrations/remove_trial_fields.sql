-- 删除users表中的trial_start_time和trial_end_time字段
USE common_db;

ALTER TABLE users DROP COLUMN IF EXISTS trial_start_time;
ALTER TABLE users DROP COLUMN IF EXISTS trial_end_time;

SELECT 'trial_start_time和trial_end_time字段删除成功' AS message;
