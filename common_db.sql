/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 90600 (9.6.0)
 Source Host           : localhost:3306
 Source Schema         : common_db

 Target Server Type    : MySQL
 Target Server Version : 90600 (9.6.0)
 File Encoding         : 65001

 Date: 20/04/2026 19:43:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for learning_materials
-- ----------------------------
DROP TABLE IF EXISTS `learning_materials`;
CREATE TABLE `learning_materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '资料标题',
  `description` text NOT NULL COMMENT '资料描述',
  `type` int NOT NULL COMMENT '资料类型：1-考研，2-考公',
  `category_id` int NOT NULL COMMENT '资料分类ID',
  `subject` varchar(100) NOT NULL COMMENT '科目：如数学、英语、政治等',
  `file_path` varchar(255) NOT NULL COMMENT '文件存储路径',
  `file_url` varchar(255) NOT NULL COMMENT '文件下载URL',
  `file_size` int NOT NULL COMMENT '文件大小，单位：字节',
  `file_extension` varchar(50) NOT NULL COMMENT '文件扩展名',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图片URL',
  `uploader_id` int NOT NULL COMMENT '上传者ID',
  `upload_time` datetime NOT NULL COMMENT '上传时间',
  `download_count` int DEFAULT NULL COMMENT '下载次数',
  `rating` float DEFAULT NULL COMMENT '评分',
  `is_valid` tinyint(1) DEFAULT NULL COMMENT '是否有效',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_learning_materials_category_id` (`category_id`),
  KEY `ix_learning_materials_id` (`id`),
  KEY `ix_learning_materials_type` (`type`),
  KEY `ix_learning_materials_subject` (`subject`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of learning_materials
-- ----------------------------
BEGIN;
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (2, '测试', '测试', 1, 2, '政治', 'uploads/beb6e33b-40eb-42c6-9869-c1d12f7e4a06.pdf', '/uploads/beb6e33b-40eb-42c6-9869-c1d12f7e4a06.pdf', 514192, '.pdf', '/uploads/d171db14-3828-4049-8053-6885092c2b7e.png', 1, '2026-04-20 12:12:29', 7, 3, 1, '2026-04-20 12:12:29', '2026-04-20 16:52:14');
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (3, '历史', '历史', 1, 2, '1', 'uploads/1643076f-8718-4c69-9273-f8c146d99a4b.txt', '/uploads/1643076f-8718-4c69-9273-f8c146d99a4b.txt', 40, '.txt', '/uploads/8f57d9fc-2b0a-4cbf-ba2a-c4a825dfeea4.png', 1, '2026-04-20 14:03:27', 2, 0, 1, '2026-04-20 14:03:27', '2026-04-20 16:51:57');
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (4, '测试', '1234', 2, 12, 'werty', 'uploads/1361eac3-f411-459a-9cba-ec6f804090ed.txt', '/uploads/1361eac3-f411-459a-9cba-ec6f804090ed.txt', 49, '.txt', '/uploads/e33aadfe-1b94-4d92-aee2-05d6cc22a336.png', 1, '2026-04-20 17:15:20', 1, 0, 1, '2026-04-20 17:15:19', '2026-04-20 18:47:47');
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (5, '考公', '1234', 2, 10, 'rftytgu', 'uploads/97e3dba4-3c60-4cb8-87ae-e9b8f5f9f778.txt', '/uploads/97e3dba4-3c60-4cb8-87ae-e9b8f5f9f778.txt', 49, '.txt', '/uploads/57b393ff-4072-49e4-9a7c-cbf7de62583e.png', 1, '2026-04-20 17:36:02', 0, 0, 1, '2026-04-20 17:36:01', '2026-04-20 17:36:01');
COMMIT;

-- ----------------------------
-- Table structure for material_categories
-- ----------------------------
DROP TABLE IF EXISTS `material_categories`;
CREATE TABLE `material_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `type` int NOT NULL COMMENT '适用类型：1-考研，2-考公，3-通用',
  `description` text COMMENT '分类描述',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_material_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_categories
-- ----------------------------
BEGIN;
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (1, '考研政治', 1, '考研政治相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (2, '考研英语', 1, '考研英语相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (3, '考研数学', 1, '考研数学相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (4, '考研专业课', 1, '考研专业课相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (5, '考研复试', 1, '考研复试相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (6, '行测', 2, '公务员考试行测相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (7, '申论', 2, '公务员考试申论相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (8, '面试', 2, '公务员考试面试相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (9, '公共基础知识', 2, '公共基础知识相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (10, '学习方法', 3, '学习方法相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (11, '时间管理', 3, '时间管理相关资料', '2026-04-20 12:04:52');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (12, '心理调适', 3, '心理调适相关资料', '2026-04-20 12:04:52');
COMMIT;

-- ----------------------------
-- Table structure for material_comments
-- ----------------------------
DROP TABLE IF EXISTS `material_comments`;
CREATE TABLE `material_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `material_id` int NOT NULL COMMENT '资料ID',
  `comment` text NOT NULL COMMENT '评论内容',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_material_comments_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_comments
-- ----------------------------
BEGIN;
INSERT INTO `material_comments` (`id`, `user_id`, `material_id`, `comment`, `created_at`, `updated_at`) VALUES (1, 125, 2, '真不错', '2026-04-20 12:35:31', '2026-04-20 12:35:31');
COMMIT;

-- ----------------------------
-- Table structure for material_ratings
-- ----------------------------
DROP TABLE IF EXISTS `material_ratings`;
CREATE TABLE `material_ratings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `material_id` int NOT NULL COMMENT '资料ID',
  `rating` int NOT NULL COMMENT '评分，1-5星',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_material_ratings_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_ratings
-- ----------------------------
BEGIN;
INSERT INTO `material_ratings` (`id`, `user_id`, `material_id`, `rating`, `created_at`) VALUES (1, 125, 2, 3, '2026-04-20 12:32:24');
INSERT INTO `material_ratings` (`id`, `user_id`, `material_id`, `rating`, `created_at`) VALUES (2, 135, 3, 3, '2026-04-20 15:37:27');
COMMIT;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单编号',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `product_id` bigint unsigned NOT NULL COMMENT '产品ID',
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `quantity` int DEFAULT '1' COMMENT '数量',
  `total_amount` decimal(10,2) NOT NULL COMMENT '总金额',
  `payment_method` tinyint NOT NULL COMMENT '支付方式: 1-微信支付, 2-支付宝',
  `payment_status` tinyint DEFAULT '0' COMMENT '支付状态: 0-待支付, 1-已支付, 2-已取消, 3-已退款',
  `trade_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付平台交易号',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `refund_time` datetime DEFAULT NULL COMMENT '退款时间',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `user_requirements` json DEFAULT NULL COMMENT '用户需求信息JSON',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  UNIQUE KEY `uk_trade_no` (`trade_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_payment_status` (`payment_status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- ----------------------------
-- Records of orders
-- ----------------------------
BEGIN;
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (95, 'ORDER202604161541091252', 125, 2, '考研VIP季卡', 99.00, 1, 99.00, 1, 1, NULL, '2026-04-16 15:41:16', NULL, NULL, '2026-04-16 15:41:10', '2026-04-16 15:41:16', '{\"email\": \"chongyanghui123@gmail.com\", \"phone\": \"18989898989\", \"gender\": \"男\", \"username\": \"惠重阳\", \"birthdate\": \"2026-04-20\", \"real_name\": \"惠重阳\", \"kaoyan_requirements\": {\"types\": [\"考试大纲\"], \"majors\": \"许多富有成果\", \"schools\": \"内蒙古大学\", \"keywords\": \"系统否认曾有过她\", \"provinces\": [\"内蒙古\"]}, \"kaogong_requirements\": null}');
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (96, 'ORDER202604201526151355', 135, 5, '考公VIP季卡', 119.00, 1, 119.00, 1, 1, NULL, '2026-04-20 15:26:21', NULL, NULL, '2026-04-20 15:26:16', '2026-04-20 15:26:21', '{\"email\": \"1125864796@qq.com\", \"phone\": \"18989898989\", \"gender\": \"男\", \"username\": \"蒲周泽\", \"birthdate\": \"2026-03-31\", \"real_name\": \"蒲周泽\", \"kaoyan_requirements\": null, \"kaogong_requirements\": {\"majors\": \"电子商务\", \"keywords\": \"运营\", \"education\": \"本科\", \"provinces\": [\"陕西\"], \"position_types\": [\"公务员\"], \"is_fresh_graduate\": \"否\"}}');
COMMIT;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '产品描述',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
  `type` tinyint NOT NULL COMMENT '产品类型: 1-考研VIP, 2-考公VIP, 3-双赛道VIP',
  `duration` int NOT NULL COMMENT '有效期(天)',
  `features` json DEFAULT NULL COMMENT '产品特色JSON',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1-上架, 0-下架',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_type` (`type`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='产品/套餐表';

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (2, '考研VIP季卡', '考研赛道季度订阅，优惠更多，包含所有月卡功能', 99.00, 177.00, 1, 90, '[]', 1, 2, '2026-04-08 20:28:14', '2026-04-16 01:20:14');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (3, '考研VIP年卡', '考研赛道年度订阅，最优惠选择，包含所有月卡功能', 299.00, 708.00, 1, 365, '{\"features\": [\"考研全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"年度数据分析\", \"专属客服\"]}', 1, 3, '2026-04-08 20:28:14', '2026-04-16 15:21:03');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (4, '考公VIP月卡', '考公赛道全方位情报监控，包含国考、省考等关键信息推送', 49.00, 69.00, 2, 30, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"3天免费试用\"]}', 1, 4, '2026-04-08 20:28:14', '2026-04-15 16:56:52');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (5, '考公VIP季卡', '考公赛道季度订阅，优惠更多，包含所有月卡功能', 119.00, 207.00, 2, 90, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"季度数据统计\"]}', 1, 5, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
COMMIT;

-- ----------------------------
-- Table structure for push_logs
-- ----------------------------
DROP TABLE IF EXISTS `push_logs`;
CREATE TABLE `push_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `info_id` bigint unsigned NOT NULL COMMENT '信息ID',
  `category` tinyint NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `push_type` tinyint NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
  `push_status` tinyint NOT NULL COMMENT '推送状态: 1-成功, 0-失败',
  `push_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '推送内容',
  `error_msg` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `push_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '推送时间',
  `is_processed` tinyint(1) DEFAULT '0' COMMENT '是否处理: 1-是, 0-否',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_info_id` (`info_id`),
  KEY `idx_push_type` (`push_type`),
  KEY `idx_push_status` (`push_status`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推送日志表';

-- ----------------------------
-- Records of push_logs
-- ----------------------------
BEGIN;
INSERT INTO `push_logs` (`id`, `user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`, `error_msg`, `push_time`, `is_processed`) VALUES (58, 125, 354, 1, 3, 1, '【考研情报】内蒙古大学2024年会计专业硕士考试大纲更新\n来源：内蒙古大学研究生院\n发布时间：2026-04-20 10:32\n省份：内蒙古\n学校：内蒙古大学\n专业：会计\n类别：考试大纲\n紧急度：非常紧急\n链接：https://www.imu.edu.cn/kaoyan', NULL, '2026-04-20 10:35:49', 1);
INSERT INTO `push_logs` (`id`, `user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`, `error_msg`, `push_time`, `is_processed`) VALUES (59, 125, 355, 1, 3, 1, '【考研情报】内蒙古大学2024年会计专业考研统计学科目复习指南\n来源：内蒙古大学会计学院\n发布时间：2026-04-20 10:32\n省份：内蒙古\n学校：内蒙古大学\n专业：会计\n类别：成绩查询\n紧急度：紧急\n链接：https://www.imu.edu.cn/accounting/kaoyan', NULL, '2026-04-20 10:35:51', 1);
INSERT INTO `push_logs` (`id`, `user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`, `error_msg`, `push_time`, `is_processed`) VALUES (60, 125, 356, 1, 3, 1, '【考研情报】2024年内蒙古大学会计硕士统计学科目考试大纲解读\n来源：内蒙古大学研究生院\n发布时间：2026-04-20 10:32\n省份：内蒙古\n学校：内蒙古大学\n专业：会计\n类别：复试通知\n紧急度：紧急\n链接：https://www.imu.edu.cn/kaoyan/d解读', NULL, '2026-04-20 10:35:58', 1);
COMMIT;

-- ----------------------------
-- Table structure for push_templates
-- ----------------------------
DROP TABLE IF EXISTS `push_templates`;
CREATE TABLE `push_templates` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '模板ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `type` tinyint NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
  `template_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '第三方模板ID',
  `template_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '模板内容',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1-启用, 0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_type` (`type`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推送模板表';

-- ----------------------------
-- Records of push_templates
-- ----------------------------
BEGIN;
INSERT INTO `push_templates` (`id`, `name`, `type`, `template_id`, `template_content`, `status`, `created_at`, `updated_at`) VALUES (1, '考研情报提醒', 1, '', '您关注的考研信息已更新：{{title}}，来源：{{source}}，发布时间：{{publish_time}}，点击查看详情：{{url}}', 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `push_templates` (`id`, `name`, `type`, `template_id`, `template_content`, `status`, `created_at`, `updated_at`) VALUES (2, '考公情报提醒', 1, '', '您关注的考公信息已更新：{{title}}，来源：{{source}}，发布时间：{{publish_time}}，点击查看详情：{{url}}', 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
COMMIT;

-- ----------------------------
-- Table structure for schools
-- ----------------------------
DROP TABLE IF EXISTS `schools`;
CREATE TABLE `schools` (
  `id` int NOT NULL AUTO_INCREMENT,
  `province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `has_master` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_schools_id` (`id`),
  KEY `ix_schools_name` (`name`),
  KEY `ix_schools_province` (`province`)
) ENGINE=InnoDB AUTO_INCREMENT=1306 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of schools
-- ----------------------------
BEGIN;
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (367, '北京', '北京大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (368, '北京', '中国人民大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (369, '北京', '清华大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (370, '北京', '北京交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (371, '北京', '北京工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (372, '北京', '北京航空航天大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (373, '北京', '北京理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (374, '北京', '北京科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (375, '北京', '北方工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (376, '北京', '北京化工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (377, '北京', '北京工商大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (378, '北京', '北京服装学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (379, '北京', '北京邮电大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (380, '北京', '北京印刷学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (381, '北京', '北京建筑大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (382, '北京', '北京石油化工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (383, '北京', '北京电子科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (384, '北京', '中国农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (385, '北京', '北京农学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (386, '北京', '北京林业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (387, '北京', '北京协和医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (388, '北京', '首都医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (389, '北京', '北京中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (390, '北京', '北京师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (391, '北京', '首都师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (392, '北京', '首都体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (393, '北京', '北京外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (394, '北京', '北京第二外国语学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (395, '北京', '北京语言大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (396, '北京', '中国传媒大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (397, '北京', '中央财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (398, '北京', '对外经济贸易大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (399, '北京', '北京物资学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (400, '北京', '首都经济贸易大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (401, '北京', '外交学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (402, '北京', '中国人民公安大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (403, '北京', '国际关系学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (404, '北京', '北京体育大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (405, '北京', '中央音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (406, '北京', '中国音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (407, '北京', '中央美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (408, '北京', '中央戏剧学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (409, '北京', '中国戏曲学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (410, '北京', '北京电影学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (411, '北京', '北京舞蹈学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (412, '北京', '中央民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (413, '北京', '中国政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (414, '北京', '华北电力大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (415, '北京', '中华女子学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (416, '北京', '北京信息科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (417, '北京', '中国矿业大学(北京)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (418, '北京', '中国石油大学(北京)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (419, '北京', '中国地质大学(北京)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (420, '北京', '北京联合大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (421, '北京', '北京城市学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (422, '北京', '中国青年政治学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (423, '北京', '中国劳动关系学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (424, '北京', '中国科学院大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (425, '北京', '中国社会科学院大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (426, '北京', '中共中央党校(国家行政学院)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (427, '北京', '北京国家会计学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (428, '北京', '中国科学技术信息研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (429, '北京', '中国财政科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (430, '北京', '商务部国际贸易经济合作研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (431, '北京', '中国农业科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (432, '北京', '中国兽医药品监察所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (433, '北京', '中国林业科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (434, '北京', '中国水利水电科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (435, '北京', '中国电力科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (436, '北京', '中国建筑科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (437, '北京', '中国城市规划设计研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (438, '北京', '中国建筑设计研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (439, '北京', '中国环境科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (440, '北京', '中国地质科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (441, '北京', '钢铁研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (442, '北京', '中冶集团建筑研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (443, '北京', '冶金自动化研究设计院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (444, '北京', '机械科学研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (445, '北京', '北京机械工业自动化研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (446, '北京', '北京机电研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (447, '北京', '中国农业机械化科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (448, '北京', '中国原子能科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (449, '北京', '核工业第二研究设计院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (450, '北京', '核工业北京地质研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (451, '北京', '核工业北京化工冶金研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (452, '北京', '中国工程物理研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (453, '北京', '中国航空研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (454, '北京', '中国航空研究院(北京航空精密机械研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (455, '北京', '中国航空研究院(北京航空材料研究院)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (456, '北京', '中国航空研究院(625所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (457, '北京', '中国航空规划设计研究总院有限公司', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (458, '北京', '中国航空研究院(628所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (459, '北京', '中国航空研究院(北京长城计量测试技术研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (460, '北京', '中国电子科技集团有限公司研究生院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (461, '北京', '华北计算机系统工程研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (462, '北京', '中国兵器科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (463, '北京', '中国兵器科学研究院(中国北方车辆研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (464, '北京', '中国运载火箭技术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (465, '北京', '中国航天科工集团第二研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (466, '北京', '中国航天科工集团第二研究院207所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (467, '北京', '中国航天系统科学与工程研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (468, '北京', '中国航天科工集团第三研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (469, '北京', '中国空间技术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (470, '北京', '中国航天空气动力技术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (471, '北京', '煤炭科学研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (472, '北京', '中国石油勘探开发研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (473, '北京', '北京化工研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (474, '北京', '北京橡胶工业研究设计院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (475, '北京', '北京市科学技术研究院资源环境研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (476, '北京', '中国食品发酵工业研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (477, '北京', '中国制浆造纸研究院有限公司', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (478, '北京', '中国铁道科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (479, '北京', '交通运输部公路科学研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (480, '北京', '电信科学技术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (481, '北京', '中国艺术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (482, '北京', '中国电影艺术研究中心', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (483, '北京', '中国疾病预防控制中心', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (484, '北京', '中国中医科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (485, '北京', '中国食品药品检定研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (486, '北京', '北京生物制品研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (487, '北京', '中日友好临床医学研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (488, '北京', '国家老年医学中心', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (489, '北京', '国家体育总局体育科学研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (490, '北京', '中国建筑材料科学研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (491, '北京', '中国气象科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (492, '北京', '国家海洋环境预报中心', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (493, '北京', '中国地震局地球物理研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (494, '北京', '中国地震局地质研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (495, '北京', '中国地震局地震预测研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (496, '北京', '应急管理部国家自然灾害防治研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (497, '北京', '中国计量科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (498, '北京', '中国测绘科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (499, '北京', '中国舰船研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (500, '北京', '中国石油化工股份有限公司石油化工科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (501, '北京', '北京矿冶研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (502, '北京', '北京有色金属研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (503, '北京', '北京市科学技术研究院城市安全与环境科学研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (504, '北京', '北京市生态环境保护科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (505, '北京', '北京市心肺血管疾病研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (506, '北京', '北京市市政工程研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (507, '北京', '北京市结核病胸部肿瘤研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (508, '北京', '北京市创伤骨科研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (509, '北京', '首都儿科研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (510, '北京', '中共北京市委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (511, '北京', '长江商学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (512, '北京', '中央社会主义学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (513, '北京', '国防大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (514, '北京', '陆军航空兵学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (515, '北京', '陆军防化学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (516, '北京', '空军指挥学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (517, '北京', '军事航天部队航天工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (518, '北京', '军事科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (519, '北京', '解放军医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (520, '天津', '南开大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (521, '天津', '天津大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (522, '天津', '天津科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (523, '天津', '天津工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (524, '天津', '中国民航大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (525, '天津', '天津理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (526, '天津', '天津农学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (527, '天津', '天津医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (528, '天津', '天津中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (529, '天津', '天津师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (530, '天津', '天津职业技术师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (531, '天津', '天津外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (532, '天津', '天津商业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (533, '天津', '天津财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (534, '天津', '天津体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (535, '天津', '天津音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (536, '天津', '天津美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (537, '天津', '天津城建大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (538, '天津', '天津中德应用技术大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (539, '天津', '中钢集团天津地质研究院有限公司', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (540, '天津', '核工业理化工程研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (541, '天津', '中国航天科工集团公司第三研究院(8357所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (542, '天津', '中国航天科工集团第三研究院第八三五八研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (543, '天津', '国家海洋技术中心', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (544, '天津', '中国舰船研究院(天津航海仪器研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (545, '天津', '海军勤务学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (546, '天津', '武警指挥学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (547, '天津', '武警后勤学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (548, '河北', '河北大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (549, '河北', '河北工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (550, '河北', '河北地质大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (551, '河北', '华北电力大学(保定)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (552, '河北', '河北工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (553, '河北', '华北理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (554, '河北', '河北科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (555, '河北', '河北建筑工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (556, '河北', '河北农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (557, '河北', '河北医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (558, '河北', '河北北方学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (559, '河北', '承德医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (560, '河北', '河北师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (561, '河北', '唐山师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (562, '河北', '石家庄铁道大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (563, '河北', '燕山大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (564, '河北', '河北科技师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (565, '河北', '华北科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (566, '河北', '中国人民警察大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (567, '河北', '河北金融学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (568, '河北', '北华航天工业学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (569, '河北', '防灾科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (570, '河北', '河北经贸大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (571, '河北', '中央司法警官学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (572, '河北', '河北传媒学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (573, '河北', '河北中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (574, '河北', '中国舰船研究院(邯郸净化设备研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (575, '山西', '山西大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (576, '山西', '太原科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (577, '山西', '中北大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (578, '山西', '太原理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (579, '山西', '山西农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (580, '山西', '山西医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (581, '山西', '长治医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (582, '山西', '山西师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (583, '山西', '太原师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (584, '山西', '山西大同大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (585, '山西', '运城学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (586, '山西', '山西财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (587, '山西', '山西中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (588, '山西', '中国辐射防护研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (589, '山西', '中国兵器科学研究院(北方自动控制技术研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (590, '山西', '中国日用化学工业研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (591, '山西', '山西省中医药研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (592, '内蒙古', '内蒙古大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (593, '内蒙古', '内蒙古科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (594, '内蒙古', '内蒙古工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (595, '内蒙古', '内蒙古农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (596, '内蒙古', '内蒙古医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (597, '内蒙古', '内蒙古师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (598, '内蒙古', '内蒙古民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (599, '内蒙古', '赤峰学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (600, '内蒙古', '内蒙古财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (601, '内蒙古', '呼伦贝尔学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (602, '内蒙古', '呼和浩特民族学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (603, '内蒙古', '内蒙古艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (604, '内蒙古', '中国兵器科学研究院(内蒙金属材料研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (605, '辽宁', '辽宁大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (606, '辽宁', '大连理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (607, '辽宁', '沈阳工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (608, '辽宁', '沈阳航空航天大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (609, '辽宁', '沈阳理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (610, '辽宁', '东北大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (611, '辽宁', '辽宁科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (612, '辽宁', '辽宁工程技术大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (613, '辽宁', '辽宁石油化工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (614, '辽宁', '沈阳化工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (615, '辽宁', '大连交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (616, '辽宁', '大连海事大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (617, '辽宁', '大连工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (618, '辽宁', '沈阳建筑大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (619, '辽宁', '辽宁工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (620, '辽宁', '沈阳农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (621, '辽宁', '大连海洋大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (622, '辽宁', '中国医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (623, '辽宁', '锦州医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (624, '辽宁', '大连医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (625, '辽宁', '辽宁中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (626, '辽宁', '沈阳药科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (627, '辽宁', '沈阳医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (628, '辽宁', '辽宁师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (629, '辽宁', '沈阳师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (630, '辽宁', '渤海大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (631, '辽宁', '鞍山师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (632, '辽宁', '大连外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (633, '辽宁', '东北财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (634, '辽宁', '中国刑事警察学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (635, '辽宁', '沈阳体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (636, '辽宁', '沈阳音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (637, '辽宁', '鲁迅美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (638, '辽宁', '沈阳大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (639, '辽宁', '大连大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (640, '辽宁', '沈阳工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (641, '辽宁', '大连民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (642, '辽宁', '机械科学研究总院(沈阳铸造研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (643, '辽宁', '中国航空研究院(601所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (644, '辽宁', '中国航空研究院(606所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (645, '辽宁', '中国航空研究院(626所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (646, '辽宁', '沈阳化工研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (647, '辽宁', '中国舰船研究院(大连测控技术研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (648, '辽宁', '中共辽宁省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (649, '辽宁', '海军大连舰艇学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (650, '吉林', '吉林大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (651, '吉林', '延边大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (652, '吉林', '长春理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (653, '吉林', '东北电力大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (654, '吉林', '长春工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (655, '吉林', '吉林建筑大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (656, '吉林', '吉林化工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (657, '吉林', '吉林农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (658, '吉林', '长春中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (659, '吉林', '东北师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (660, '吉林', '北华大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (661, '吉林', '吉林师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (662, '吉林', '吉林工程技术师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (663, '吉林', '长春师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (664, '吉林', '吉林财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (665, '吉林', '吉林体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (666, '吉林', '吉林艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (667, '吉林', '吉林外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (668, '吉林', '长春工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (669, '吉林', '长春大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (670, '吉林', '中共吉林省委党校(吉林省行政学院)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (671, '吉林', '空军航空大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (672, '黑龙江', '黑龙江大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (673, '黑龙江', '哈尔滨工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (674, '黑龙江', '哈尔滨理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (675, '黑龙江', '哈尔滨工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (676, '黑龙江', '黑龙江科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (677, '黑龙江', '东北石油大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (678, '黑龙江', '佳木斯大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (679, '黑龙江', '黑龙江八一农垦大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (680, '黑龙江', '东北农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (681, '黑龙江', '东北林业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (682, '黑龙江', '哈尔滨医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (683, '黑龙江', '黑龙江中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (684, '黑龙江', '牡丹江医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (685, '黑龙江', '哈尔滨师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (686, '黑龙江', '齐齐哈尔大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (687, '黑龙江', '牡丹江师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (688, '黑龙江', '哈尔滨学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (689, '黑龙江', '哈尔滨商业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (690, '黑龙江', '哈尔滨体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (691, '黑龙江', '齐齐哈尔医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (692, '黑龙江', '黑龙江东方学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (693, '黑龙江', '黑龙江工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (694, '黑龙江', '哈尔滨音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (695, '黑龙江', '机械科学研究院哈尔滨焊接研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (696, '黑龙江', '中国航空研究院(627所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (697, '黑龙江', '中国地震局工程力学研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (698, '黑龙江', '中国舰船研究院(哈尔滨船舶锅炉涡轮机研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (699, '黑龙江', '黑龙江省中医药科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (700, '黑龙江', '黑龙江省社会科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (701, '黑龙江', '黑龙江省科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (702, '黑龙江', '中共黑龙江省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (703, '上海', '复旦大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (704, '上海', '同济大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (705, '上海', '上海交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (706, '上海', '华东理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (707, '上海', '上海理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (708, '上海', '上海海事大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (709, '上海', '东华大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (710, '上海', '上海电力大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (711, '上海', '上海应用技术大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (712, '上海', '上海海洋大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (713, '上海', '上海中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (714, '上海', '华东师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (715, '上海', '上海师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (716, '上海', '上海外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (717, '上海', '上海财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (718, '上海', '上海对外经贸大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (719, '上海', '上海海关学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (720, '上海', '华东政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (721, '上海', '上海体育大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (722, '上海', '上海音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (723, '上海', '上海戏剧学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (724, '上海', '上海大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (725, '上海', '上海工程技术大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (726, '上海', '上海立信会计金融学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (727, '上海', '上海电机学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (728, '上海', '上海杉达学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (729, '上海', '上海政法学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (730, '上海', '上海第二工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (731, '上海', '上海商学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (732, '上海', '上海科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (733, '上海', '上海国家会计学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (734, '上海', '上海材料研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (735, '上海', '上海发电设备成套设计研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (736, '上海', '上海核工程研究设计院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (737, '上海', '中国航空研究院(640所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (738, '上海', '上海航天技术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (739, '上海', '上海化工研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (740, '上海', '上海船舶运输科学研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (741, '上海', '电信科学技术第一研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (742, '上海', '上海生物制品研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (743, '上海', '中国医药工业研究总院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (744, '上海', '中国舰船研究院(中国船舶及海洋工程设计研究院)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (745, '上海', '中国舰船研究院(上海船舶设备研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (746, '上海', '中国舰船研究院(上海船用柴油机研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (747, '上海', '中国舰船研究院(上海船舶电子设备研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (748, '上海', '上海国际问题研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (749, '上海', '上海社会科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (750, '上海', '中共上海市委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (751, '上海', '海军军医大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (752, '江苏', '南京大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (753, '江苏', '苏州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (754, '江苏', '东南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (755, '江苏', '南京航空航天大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (756, '江苏', '南京理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (757, '江苏', '江苏科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (758, '江苏', '中国矿业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (759, '江苏', '南京工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (760, '江苏', '常州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (761, '江苏', '南京邮电大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (762, '江苏', '河海大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (763, '江苏', '江南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (764, '江苏', '南京林业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (765, '江苏', '江苏大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (766, '江苏', '南京信息工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (767, '江苏', '南通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (768, '江苏', '盐城工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (769, '江苏', '南京农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (770, '江苏', '南京医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (771, '江苏', '徐州医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (772, '江苏', '南京中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (773, '江苏', '中国药科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (774, '江苏', '南京师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (775, '江苏', '江苏师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (776, '江苏', '淮阴师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (777, '江苏', '盐城师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (778, '江苏', '南京财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (779, '江苏', '江苏警官学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (780, '江苏', '南京体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (781, '江苏', '南京艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (782, '江苏', '苏州科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (783, '江苏', '苏州工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (784, '江苏', '淮阴工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (785, '江苏', '常州工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (786, '江苏', '扬州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (787, '江苏', '南京工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (788, '江苏', '南京审计大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (789, '江苏', '南京晓庄学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (790, '江苏', '江苏理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (791, '江苏', '江苏海洋大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (792, '江苏', '徐州工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (793, '江苏', '南京警察学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (794, '江苏', '金陵科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (795, '江苏', '国网电力科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (796, '江苏', '南京水利科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (797, '江苏', '中国航空研究院(609所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (798, '江苏', '中国舰船研究院(中国船舶科学研究中心)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (799, '江苏', '中国舰船研究院(江苏自动化研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (800, '江苏', '江苏省中国科学院植物研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (801, '江苏', '江苏省血吸虫病防治研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (802, '江苏', '中共江苏省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (803, '江苏', '陆军指挥学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (804, '江苏', '陆军工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (805, '江苏', '海军指挥学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (806, '江苏', '空军勤务学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (807, '江苏', '网络空间部队第五十六研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (808, '浙江', '浙江大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (809, '浙江', '杭州电子科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (810, '浙江', '浙江工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (811, '浙江', '浙江理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (812, '浙江', '浙江海洋大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (813, '浙江', '浙江农林大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (814, '浙江', '温州医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (815, '浙江', '浙江中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (816, '浙江', '浙江师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (817, '浙江', '杭州师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (818, '浙江', '湖州师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (819, '浙江', '绍兴文理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (820, '浙江', '台州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (821, '浙江', '温州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (822, '浙江', '丽水学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (823, '浙江', '浙江工商大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (824, '浙江', '嘉兴大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (825, '浙江', '中国美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (826, '浙江', '中国计量大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (827, '浙江', '浙江万里学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (828, '浙江', '浙江科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (829, '浙江', '宁波工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (830, '浙江', '浙江财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (831, '浙江', '浙江警察学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (832, '浙江', '衢州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (833, '浙江', '宁波大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (834, '浙江', '浙江传媒学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (835, '浙江', '浙江树人学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (836, '浙江', '浙大城市学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (837, '浙江', '浙大宁波理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (838, '浙江', '杭州医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (839, '浙江', '浙江外国语学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (840, '浙江', '浙江音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (841, '浙江', '西湖大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (842, '浙江', '自然资源部第二海洋研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (843, '浙江', '中国舰船研究院(杭州应用声学研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (844, '浙江', '中共浙江省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (845, '安徽', '安徽大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (846, '安徽', '中国科学技术大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (847, '安徽', '合肥工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (848, '安徽', '安徽工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (849, '安徽', '安徽理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (850, '安徽', '安徽工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (851, '安徽', '安徽农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (852, '安徽', '安徽医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (853, '安徽', '蚌埠医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (854, '安徽', '皖南医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (855, '安徽', '安徽中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (856, '安徽', '安徽师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (857, '安徽', '阜阳师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (858, '安徽', '安庆师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (859, '安徽', '淮北师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (860, '安徽', '皖西学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (861, '安徽', '滁州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (862, '安徽', '安徽财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (863, '安徽', '宿州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (864, '安徽', '安徽建筑大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (865, '安徽', '安徽科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (866, '安徽', '合肥大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (867, '安徽', '合肥师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (868, '安徽', '马鞍山矿山研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (869, '安徽', '陆军兵种大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (870, '福建', '厦门大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (871, '福建', '华侨大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (872, '福建', '福州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (873, '福建', '福建理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (874, '福建', '福建农林大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (875, '福建', '集美大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (876, '福建', '福建医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (877, '福建', '福建中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (878, '福建', '福建师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (879, '福建', '闽江学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (880, '福建', '武夷学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (881, '福建', '宁德师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (882, '福建', '泉州师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (883, '福建', '闽南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (884, '福建', '厦门理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (885, '福建', '三明学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (886, '福建', '龙岩学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (887, '福建', '莆田学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (888, '福建', '福建江夏学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (889, '福建', '厦门国家会计学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (890, '福建', '自然资源部第三海洋研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (891, '江西', '南昌大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (892, '江西', '华东交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (893, '江西', '东华理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (894, '江西', '南昌航空大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (895, '江西', '江西理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (896, '江西', '景德镇陶瓷大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (897, '江西', '江西农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (898, '江西', '江西中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (899, '江西', '赣南医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (900, '江西', '江西师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (901, '江西', '上饶师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (902, '江西', '宜春学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (903, '江西', '赣南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (904, '江西', '井冈山大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (905, '江西', '江西财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (906, '江西', '江西科技师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (907, '江西', '江西水利电力大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (908, '江西', '九江学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (909, '江西', '中国航空研究院(602所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (910, '江西', '陆军步兵学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (911, '山东', '山东大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (912, '山东', '中国海洋大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (913, '山东', '山东科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (914, '山东', '中国石油大学(华东)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (915, '山东', '青岛科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (916, '山东', '济南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (917, '山东', '青岛理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (918, '山东', '山东建筑大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (919, '山东', '齐鲁工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (920, '山东', '山东理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (921, '山东', '山东农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (922, '山东', '青岛农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (923, '山东', '山东第二医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (924, '山东', '山东第一医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (925, '山东', '滨州医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (926, '山东', '山东中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (927, '山东', '济宁医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (928, '山东', '山东师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (929, '山东', '曲阜师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (930, '山东', '聊城大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (931, '山东', '德州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (932, '山东', '山东航空学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (933, '山东', '鲁东大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (934, '山东', '临沂大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (935, '山东', '泰山学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (936, '山东', '山东财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (937, '山东', '山东体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (938, '山东', '山东艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (939, '山东', '枣庄学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (940, '山东', '山东工艺美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (941, '山东', '青岛大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (942, '山东', '烟台大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (943, '山东', '潍坊学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (944, '山东', '山东交通学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (945, '山东', '山东工商学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (946, '山东', '山东政法学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (947, '山东', '中国兵器科学研究院(山东非金属材料研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (948, '山东', '自然资源部第一海洋研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (949, '山东', '中共山东省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (950, '山东', '海军潜艇学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (951, '山东', '海军航空大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (952, '河南', '华北水利水电大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (953, '河南', '郑州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (954, '河南', '河南理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (955, '河南', '郑州轻工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (956, '河南', '河南工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (957, '河南', '河南科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (958, '河南', '中原工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (959, '河南', '河南农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (960, '河南', '河南科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (961, '河南', '河南中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (962, '河南', '河南医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (963, '河南', '河南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (964, '河南', '河南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (965, '河南', '信阳师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (966, '河南', '安阳师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (967, '河南', '南阳师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (968, '河南', '洛阳师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (969, '河南', '河南财经政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (970, '河南', '郑州航空工业管理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (971, '河南', '平顶山学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (972, '河南', '河南城建学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (973, '河南', '中钢集团洛阳耐火材料研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (974, '河南', '机械科学研究总院(郑州机械研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (975, '河南', '中国航空研究院(014中心)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (976, '河南', '中国航空研究院(613所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (977, '河南', '中国烟草总公司郑州烟草研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (978, '河南', '中国舰船研究院(郑州机电工程研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (979, '河南', '中国舰船研究院(洛阳船舶材料研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (980, '河南', '网络空间部队信息工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (981, '湖北', '武汉大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (982, '湖北', '华中科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (983, '湖北', '武汉科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (984, '湖北', '长江大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (985, '湖北', '武汉工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (986, '湖北', '中国地质大学(武汉)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (987, '湖北', '武汉纺织大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (988, '湖北', '武汉轻工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (989, '湖北', '武汉理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (990, '湖北', '湖北工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (991, '湖北', '华中农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (992, '湖北', '湖北中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (993, '湖北', '华中师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (994, '湖北', '湖北大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (995, '湖北', '湖北师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (996, '湖北', '黄冈师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (997, '湖北', '湖北民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (998, '湖北', '湖北文理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (999, '湖北', '中南财经政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1000, '湖北', '武汉体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1001, '湖北', '湖北美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1002, '湖北', '中南民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1003, '湖北', '湖北汽车工业学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1004, '湖北', '湖北工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1005, '湖北', '湖北理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1006, '湖北', '湖北科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1007, '湖北', '湖北医药学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1008, '湖北', '江汉大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1009, '湖北', '三峡大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1010, '湖北', '武汉音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1011, '湖北', '湖北经济学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1012, '湖北', '长江科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1013, '湖北', '中钢集团武汉安全环保研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1014, '湖北', '机械科学研究总院(武汉材料保护研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1015, '湖北', '中国航空研究院(610所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1016, '湖北', '航天动力技术研究院(42所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1017, '湖北', '武汉邮电科学研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1018, '湖北', '武汉生物制品研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1019, '湖北', '中国地震局地震研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1020, '湖北', '中国舰船研究院(武汉数字工程研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1021, '湖北', '中国舰船研究院(中国舰船研究设计中心)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1022, '湖北', '中国舰船研究院(武汉船用电力推进装置研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1023, '湖北', '中国舰船研究院(华中光电技术研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1024, '湖北', '中国舰船研究院(武汉船舶通信研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1025, '湖北', '中国舰船研究院(武汉第二船舶设计研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1026, '湖北', '湖北省社会科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1027, '湖北', '中共湖北省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1028, '湖北', '海军工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1029, '湖北', '空军预警学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1030, '湖北', '火箭军指挥学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1031, '湖北', '信息支援部队工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1032, '湖南', '湘潭大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1033, '湖南', '吉首大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1034, '湖南', '湖南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1035, '湖南', '中南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1036, '湖南', '湖南科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1037, '湖南', '长沙理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1038, '湖南', '湖南农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1039, '湖南', '中南林业科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1040, '湖南', '湖南中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1041, '湖南', '湖南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1042, '湖南', '湖南理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1043, '湖南', '衡阳师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1044, '湖南', '邵阳学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1045, '湖南', '湖南文理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1046, '湖南', '湖南科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1047, '湖南', '湖南人文科技学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1048, '湖南', '湖南工商大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1049, '湖南', '南华大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1050, '湖南', '长沙学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1051, '湖南', '湖南工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1052, '湖南', '湖南城市学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1053, '湖南', '湖南工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1054, '湖南', '湖南第一师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1055, '湖南', '长沙矿冶研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1056, '湖南', '中国航空研究院(608所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1057, '湖南', '长沙矿山研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1058, '湖南', '湖南省中医药研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1059, '湖南', '中共湖南省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1060, '湖南', '国防科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1061, '广东', '中山大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1062, '广东', '暨南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1063, '广东', '汕头大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1064, '广东', '华南理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1065, '广东', '华南农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1066, '广东', '广东海洋大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1067, '广东', '广州医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1068, '广东', '广东医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1069, '广东', '广州中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1070, '广东', '广东药科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1071, '广东', '华南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1072, '广东', '韶关学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1073, '广东', '惠州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1074, '广东', '韩山师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1075, '广东', '岭南师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1076, '广东', '肇庆学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1077, '广东', '嘉应学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1078, '广东', '广州体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1079, '广东', '广州美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1080, '广东', '星海音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1081, '广东', '广东技术师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1082, '广东', '深圳大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1083, '广东', '广东财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1084, '广东', '广州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1085, '广东', '仲恺农业工程学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1086, '广东', '五邑大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1087, '广东', '广东金融学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1088, '广东', '广东石油化工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1089, '广东', '东莞理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1090, '广东', '广东工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1091, '广东', '广东外语外贸大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1092, '广东', '佛山大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1093, '广东', '南方医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1094, '广东', '南方科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1095, '广东', '中共广东省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1096, '广东', '广东省社会科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1097, '广东', '广东省心血管病研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1098, '广西', '广西大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1099, '广西', '广西科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1100, '广西', '桂林电子科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1101, '广西', '桂林理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1102, '广西', '广西医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1103, '广西', '右江民族医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1104, '广西', '广西中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1105, '广西', '桂林医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1106, '广西', '广西师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1107, '广西', '南宁师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1108, '广西', '玉林师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1109, '广西', '广西艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1110, '广西', '广西民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1111, '广西', '广西财经学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1112, '广西', '北部湾大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1113, '广西', '贺州学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1114, '广西', '陆军特种作战学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1115, '海南', '海南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1116, '海南', '海南热带海洋学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1117, '海南', '海南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1118, '海南', '海南医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1119, '海南', '三亚学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1120, '重庆', '重庆大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1121, '重庆', '重庆邮电大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1122, '重庆', '重庆交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1123, '重庆', '重庆医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1124, '重庆', '西南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1125, '重庆', '重庆师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1126, '重庆', '重庆文理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1127, '重庆', '重庆三峡学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1128, '重庆', '长江师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1129, '重庆', '四川外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1130, '重庆', '西南政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1131, '重庆', '四川美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1132, '重庆', '重庆科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1133, '重庆', '重庆理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1134, '重庆', '重庆工商大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1135, '重庆', '重庆中医药学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1136, '重庆', '中共重庆市委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1137, '重庆', '陆军军医大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1138, '重庆', '联勤保障部队工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1139, '四川', '四川大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1140, '四川', '西南交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1141, '四川', '电子科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1142, '四川', '西南石油大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1143, '四川', '成都理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1144, '四川', '西南科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1145, '四川', '成都信息工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1146, '四川', '四川轻化工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1147, '四川', '西华大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1148, '四川', '中国民用航空飞行学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1149, '四川', '四川农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1150, '四川', '西昌学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1151, '四川', '西南医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1152, '四川', '成都中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1153, '四川', '川北医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1154, '四川', '四川师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1155, '四川', '西华师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1156, '四川', '绵阳师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1157, '四川', '内江师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1158, '四川', '宜宾学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1159, '四川', '乐山师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1160, '四川', '西南财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1161, '四川', '成都体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1162, '四川', '四川音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1163, '四川', '西南民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1164, '四川', '成都大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1165, '四川', '攀枝花学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1166, '四川', '四川警察学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1167, '四川', '成都医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1168, '四川', '中国核动力研究设计院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1169, '四川', '核工业西南物理研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1170, '四川', '中国航空研究院(611所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1171, '四川', '中国航空研究院(624所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1172, '四川', '中国兵器科学研究院(西南技术物理研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1173, '四川', '中国兵器科学研究院(西南自动化研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1174, '四川', '电信科学技术研究院(第五研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1175, '四川', '四川省社会科学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1176, '四川', '中共四川省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1177, '贵州', '贵州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1178, '贵州', '贵州医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1179, '贵州', '遵义医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1180, '贵州', '贵州中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1181, '贵州', '贵州师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1182, '贵州', '遵义师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1183, '贵州', '铜仁学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1184, '贵州', '黔南民族师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1185, '贵州', '贵州财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1186, '贵州', '贵州民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1187, '贵州', '贵阳学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1188, '贵州', '贵州师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1189, '贵州', '中国航天科工集团第十研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1190, '云南', '云南大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1191, '云南', '昆明理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1192, '云南', '云南农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1193, '云南', '西南林业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1194, '云南', '昆明医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1195, '云南', '大理大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1196, '云南', '云南中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1197, '云南', '云南师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1198, '云南', '曲靖师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1199, '云南', '红河学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1200, '云南', '云南财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1201, '云南', '云南艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1202, '云南', '云南民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1203, '云南', '玉溪师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1204, '云南', '云南警官学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1205, '云南', '昆明学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1206, '云南', '中国兵器科学研究院(昆明物理研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1207, '云南', '昆明贵金属研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1208, '西藏', '西藏农牧大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1209, '西藏', '西藏大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1210, '西藏', '西藏民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1211, '西藏', '西藏藏医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1212, '陕西', '西北大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1213, '陕西', '西安交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1214, '陕西', '西北工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1215, '陕西', '西安理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1216, '陕西', '西安电子科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1217, '陕西', '西安工业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1218, '陕西', '西安建筑科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1219, '陕西', '西安科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1220, '陕西', '西安石油大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1221, '陕西', '陕西科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1222, '陕西', '西安工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1223, '陕西', '长安大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1224, '陕西', '西北农林科技大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1225, '陕西', '陕西中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1226, '陕西', '陕西师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1227, '陕西', '延安大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1228, '陕西', '陕西理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1229, '陕西', '宝鸡文理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1230, '陕西', '咸阳师范学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1231, '陕西', '西安外国语大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1232, '陕西', '西北政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1233, '陕西', '西安体育学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1234, '陕西', '西安音乐学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1235, '陕西', '西安美术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1236, '陕西', '西安文理学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1237, '陕西', '榆林学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1238, '陕西', '商洛学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1239, '陕西', '安康学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1240, '陕西', '西安财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1241, '陕西', '西安邮电大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1242, '陕西', '西安医学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1243, '陕西', '西京学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1244, '陕西', '西安热工研究院有限公司', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1245, '陕西', '中国航空研究院(603所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1246, '陕西', '中国航空研究院(623所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1247, '陕西', '中国航空研究院(630所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1248, '陕西', '中国航空研究院(631所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1249, '陕西', '中国航空研究院(618所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1250, '陕西', '中国兵器科学研究院(西安近代化学研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1251, '陕西', '中国兵器科学研究院(西安应用光学研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1252, '陕西', '中国兵器科学研究院(西安机电信息技术研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1253, '陕西', '中国兵器科学研究院(陕西应用物理化学研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1254, '陕西', '中国兵器科学研究院(西北机电工程研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1255, '陕西', '中国兵器科学研究院(西安现代控制技术研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1256, '陕西', '中国兵器科学研究院(西安电子工程研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1257, '陕西', '中国航天科工集团第二研究院(16所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1258, '陕西', '航天动力技术研究院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1259, '陕西', '中国空间技术研究院(西安分院)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1260, '陕西', '西安微电子技术研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1261, '陕西', '中国航天科技集团有限公司第六研究院第十一研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1262, '陕西', '电信科学技术第四研究所(西安)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1263, '陕西', '中国舰船研究院(西安精密机械研究所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1264, '陕西', '中共陕西省委党校', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1265, '陕西', '空军工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1266, '陕西', '空军军医大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1267, '陕西', '火箭军工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1268, '陕西', '武警工程大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1269, '陕西', '西北核技术研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1270, '甘肃', '兰州大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1271, '甘肃', '兰州理工大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1272, '甘肃', '兰州交通大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1273, '甘肃', '甘肃农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1274, '甘肃', '甘肃中医药大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1275, '甘肃', '西北师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1276, '甘肃', '兰州城市学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1277, '甘肃', '陇东学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1278, '甘肃', '天水师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1279, '甘肃', '河西学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1280, '甘肃', '兰州财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1281, '甘肃', '西北民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1282, '甘肃', '甘肃政法大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1283, '甘肃', '中国空间技术研究院(510所)', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1284, '甘肃', '天华化工机械及自动化研究设计院有限公司', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1285, '甘肃', '兰州生物制品研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1286, '甘肃', '中国地震局兰州地震研究所', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1287, '青海', '青海大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1288, '青海', '青海师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1289, '青海', '青海民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1290, '宁夏', '宁夏大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1291, '宁夏', '宁夏医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1292, '宁夏', '宁夏师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1293, '宁夏', '北方民族大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1294, '宁夏', '宁夏理工学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1295, '新疆', '新疆大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1296, '新疆', '塔里木大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1297, '新疆', '新疆农业大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1298, '新疆', '石河子大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1299, '新疆', '新疆医科大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1300, '新疆', '新疆师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1301, '新疆', '喀什大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1302, '新疆', '伊犁师范大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1303, '新疆', '新疆财经大学', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1304, '新疆', '新疆艺术学院', 1, '2026-04-14 23:04:51', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1305, '新疆', '昌吉学院', 1, '2026-04-14 23:04:51', NULL);
COMMIT;

-- ----------------------------
-- Table structure for system_config
-- ----------------------------
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置键',
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '配置值',
  `config_type` tinyint DEFAULT '0' COMMENT '配置类型: 0-字符串, 1-数字, 2-布尔值, 3-JSON',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置描述',
  `is_system` tinyint DEFAULT '0' COMMENT '是否系统配置: 1-是, 0-否',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1-启用, 0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- ----------------------------
-- Records of system_config
-- ----------------------------
BEGIN;
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (1, 'crawler_interval', '10（更新后）', 1, '爬虫默认抓取间隔(分钟) - 更新于 2026-04-16', 1, 1, '2026-04-08 20:28:14', '2026-04-16 18:10:40');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (2, 'max_concurrent_crawlers', '5', 1, '最大并发爬虫数', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (3, 'push_enabled', '1', 2, '是否启用推送功能', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (4, 'trial_days', '3', 1, '免费试用天数', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (5, 'wechat_app_id', '', 0, '微信公众号AppID', 0, 1, '2026-04-08 20:28:14', '2026-04-16 18:11:06');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (6, 'wechat_app_secret', '', 0, '微信公众号AppSecret', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (7, 'alipay_app_id', '', 0, '支付宝AppID', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (8, 'alipay_private_key', '', 0, '支付宝私钥', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (9, 'push_settings', '{\'frequency\': \'weekly\', \'time\': \'10:30\'}', 3, '推送设置', 1, 1, '2026-04-20 17:12:40', '2026-04-20 17:12:40');
COMMIT;

-- ----------------------------
-- Table structure for user_crawler_configs
-- ----------------------------
DROP TABLE IF EXISTS `user_crawler_configs`;
CREATE TABLE `user_crawler_configs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `crawler_type` tinyint NOT NULL COMMENT '爬虫类型: 1=考研, 2=考公',
  `crawler_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '爬虫名称',
  `base_crawler_id` bigint unsigned DEFAULT NULL COMMENT '基础爬虫ID',
  `config_json` json NOT NULL COMMENT '爬虫配置JSON',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态: 1=激活, 0=暂停',
  `priority` tinyint NOT NULL DEFAULT '2' COMMENT '优先级: 1=高, 2=中, 3=低',
  `last_crawl_time` datetime DEFAULT NULL COMMENT '最后爬取时间',
  `crawl_interval` int NOT NULL DEFAULT '3600' COMMENT '爬取间隔(秒)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_crawler` (`user_id`,`crawler_name`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_crawler_type` (`crawler_type`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户爬虫配置表';

-- ----------------------------
-- Records of user_crawler_configs
-- ----------------------------
BEGIN;
INSERT INTO `user_crawler_configs` (`id`, `user_id`, `crawler_type`, `crawler_name`, `base_crawler_id`, `config_json`, `status`, `priority`, `last_crawl_time`, `crawl_interval`, `created_at`, `updated_at`) VALUES (1, 22, 1, '惠重阳_考研监控', NULL, '{\"targets\": [\"华东师范大学\", \"上海\"], \"user_id\": 22, \"keywords\": [\"软件工程\", \"录取通知\", \"复试通知\"], \"ai_enabled\": true, \"user_config\": {\"types\": [\"录取通知\", \"复试通知\"], \"majors\": [\"软件工程\"], \"schools\": [\"华东师范大学\"], \"provinces\": [\"上海\"], \"study_type\": [], \"degree_type\": []}, \"crawler_name\": \"惠重阳_考研监控\", \"crawler_type\": 1, \"push_enabled\": true}', 1, 2, NULL, 3600, '2026-04-09 23:22:42', '2026-04-09 23:22:42');
COMMIT;

-- ----------------------------
-- Table structure for user_crawler_keywords
-- ----------------------------
DROP TABLE IF EXISTS `user_crawler_keywords`;
CREATE TABLE `user_crawler_keywords` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_crawler_id` bigint unsigned NOT NULL COMMENT '用户爬虫配置ID',
  `keyword` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关键词',
  `keyword_type` tinyint NOT NULL COMMENT '关键词类型: 1=专业, 2=学校, 3=地区, 4=其他',
  `weight` decimal(3,2) DEFAULT '1.00' COMMENT '权重',
  `is_active` tinyint NOT NULL DEFAULT '1' COMMENT '是否激活',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_crawler_keyword` (`user_crawler_id`,`keyword`,`keyword_type`),
  KEY `idx_user_crawler_id` (`user_crawler_id`),
  KEY `idx_keyword` (`keyword`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户爬虫关键词关联表';

-- ----------------------------
-- Records of user_crawler_keywords
-- ----------------------------
BEGIN;
INSERT INTO `user_crawler_keywords` (`id`, `user_crawler_id`, `keyword`, `keyword_type`, `weight`, `is_active`, `created_at`) VALUES (1, 1, '软件工程', 1, 1.00, 1, '2026-04-09 23:22:42');
COMMIT;

-- ----------------------------
-- Table structure for user_crawler_logs
-- ----------------------------
DROP TABLE IF EXISTS `user_crawler_logs`;
CREATE TABLE `user_crawler_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_crawler_id` bigint unsigned NOT NULL COMMENT '用户爬虫配置ID',
  `crawl_status` tinyint NOT NULL COMMENT '爬取状态: 1=成功, 2=失败, 3=部分成功',
  `items_count` int DEFAULT '0' COMMENT '爬取到的项目数',
  `new_items_count` int DEFAULT '0' COMMENT '新增项目数',
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `crawl_duration` int DEFAULT NULL COMMENT '爬取耗时(秒)',
  `crawl_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_crawler_id` (`user_crawler_id`),
  KEY `idx_crawl_time` (`crawl_time`),
  KEY `idx_crawl_status` (`crawl_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户爬虫日志表';

-- ----------------------------
-- Records of user_crawler_logs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_crawler_results
-- ----------------------------
DROP TABLE IF EXISTS `user_crawler_results`;
CREATE TABLE `user_crawler_results` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_crawler_id` bigint unsigned NOT NULL COMMENT '用户爬虫配置ID',
  `info_id` bigint unsigned NOT NULL COMMENT '信息ID(对应考研或考公信息表)',
  `info_type` tinyint NOT NULL COMMENT '信息类型: 1=考研, 2=考公',
  `match_score` decimal(5,2) DEFAULT '0.00' COMMENT '匹配分数',
  `is_read` tinyint NOT NULL DEFAULT '0' COMMENT '是否已读: 0=未读, 1=已读',
  `is_notified` tinyint NOT NULL DEFAULT '0' COMMENT '是否已通知: 0=未通知, 1=已通知',
  `is_favorite` tinyint NOT NULL DEFAULT '0' COMMENT '是否收藏: 0=未收藏, 1=已收藏',
  `crawl_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_info` (`user_crawler_id`,`info_id`),
  KEY `idx_user_crawler_id` (`user_crawler_id`),
  KEY `idx_info_type` (`info_type`),
  KEY `idx_match_score` (`match_score`),
  KEY `idx_crawl_time` (`crawl_time`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_is_notified` (`is_notified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户爬虫结果表';

-- ----------------------------
-- Records of user_crawler_results
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_downloads
-- ----------------------------
DROP TABLE IF EXISTS `user_downloads`;
CREATE TABLE `user_downloads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `material_id` int NOT NULL COMMENT '资料ID',
  `download_time` datetime NOT NULL COMMENT '下载时间',
  `ip_address` varchar(50) DEFAULT NULL COMMENT '下载IP地址',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `ix_user_downloads_user_id` (`user_id`),
  KEY `ix_user_downloads_id` (`id`),
  KEY `ix_user_downloads_material_id` (`material_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user_downloads
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_favorites
-- ----------------------------
DROP TABLE IF EXISTS `user_favorites`;
CREATE TABLE `user_favorites` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `info_id` bigint unsigned NOT NULL COMMENT '信息ID',
  `category` tinyint NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_info` (`user_id`,`info_id`,`category`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_info_id` (`info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏信息表';

-- ----------------------------
-- Records of user_favorites
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_keywords
-- ----------------------------
DROP TABLE IF EXISTS `user_keywords`;
CREATE TABLE `user_keywords` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '关键词ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `keyword` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关键词',
  `category` tinyint NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用: 1-是, 0-否',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_keyword` (`user_id`,`keyword`,`category`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=223 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户关键词表';

-- ----------------------------
-- Records of user_keywords
-- ----------------------------
BEGIN;
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (146, 1, '人工智能', 1, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (147, 1, '机器学习', 1, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (148, 1, '公务员', 2, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (149, 1, '国考', 2, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (219, 125, '统计', 1, 1, '2026-04-20 10:29:17', '2026-04-20 10:29:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (222, 135, '运营', 2, 1, '2026-04-20 16:43:03', '2026-04-20 16:43:03');
COMMIT;

-- ----------------------------
-- Table structure for user_material_favorites
-- ----------------------------
DROP TABLE IF EXISTS `user_material_favorites`;
CREATE TABLE `user_material_favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `material_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `user_material_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_material_favorites_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `learning_materials` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user_material_favorites
-- ----------------------------
BEGIN;
INSERT INTO `user_material_favorites` (`id`, `user_id`, `material_id`, `created_at`) VALUES (7, 1, 2, '2026-04-20 18:11:27');
INSERT INTO `user_material_favorites` (`id`, `user_id`, `material_id`, `created_at`) VALUES (16, 135, 4, '2026-04-20 18:48:00');
INSERT INTO `user_material_favorites` (`id`, `user_id`, `material_id`, `created_at`) VALUES (17, 135, 5, '2026-04-20 18:54:04');
COMMIT;

-- ----------------------------
-- Table structure for user_read_info
-- ----------------------------
DROP TABLE IF EXISTS `user_read_info`;
CREATE TABLE `user_read_info` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '已读ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `info_id` bigint unsigned NOT NULL COMMENT '信息ID',
  `category` tinyint NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `read_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '阅读时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_info` (`user_id`,`info_id`,`category`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_info_id` (`info_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户已读信息表';

-- ----------------------------
-- Records of user_read_info
-- ----------------------------
BEGIN;
INSERT INTO `user_read_info` (`id`, `user_id`, `info_id`, `category`, `read_time`) VALUES (1, 125, 354, 1, '2026-04-20 10:35:51');
INSERT INTO `user_read_info` (`id`, `user_id`, `info_id`, `category`, `read_time`) VALUES (2, 125, 355, 1, '2026-04-20 10:35:58');
INSERT INTO `user_read_info` (`id`, `user_id`, `info_id`, `category`, `read_time`) VALUES (3, 125, 356, 1, '2026-04-20 10:36:00');
COMMIT;

-- ----------------------------
-- Table structure for user_subscriptions
-- ----------------------------
DROP TABLE IF EXISTS `user_subscriptions`;
CREATE TABLE `user_subscriptions` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '订阅ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `subscribe_type` tinyint NOT NULL COMMENT '订阅类型: 1-考研, 2-考公, 3-双赛道',
  `status` tinyint DEFAULT '1' COMMENT '订阅状态: 1-有效, 0-无效',
  `config_json` json DEFAULT NULL COMMENT '订阅配置JSON',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_type` (`user_id`,`subscribe_type`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_subscribe_type` (`subscribe_type`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户订阅配置表';

-- ----------------------------
-- Records of user_subscriptions
-- ----------------------------
BEGIN;
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (71, 1, 1, 1, '{\"kaoyan_requirements\": {\"types\": [\"录取通知\"], \"majors\": [\"计算机科学\"], \"schools\": [\"复旦大学\"], \"keywords\": \"人工智能,机器学习\", \"provinces\": [\"上海\"]}, \"kaogong_requirements\": {\"majors\": [\"不限\"], \"keywords\": \"公务员,国考\", \"education\": [\"本科\"], \"provinces\": [\"北京\"], \"position_types\": [\"综合管理\"], \"is_fresh_graduate\": \"是\"}}', '2026-04-15 03:14:44', '2026-04-15 03:16:17');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (99, 125, 1, 1, '{\"push\": {\"time\": \"10:35\", \"frequency\": \"daily\"}, \"kaoyan\": {\"types\": [\"考试大纲\"], \"majors\": \"会计\", \"schools\": \"内蒙古大学\", \"keywords\": \"统计\", \"provinces\": [\"内蒙古\"]}, \"kaogong\": {}}', '2026-04-16 15:41:10', '2026-04-20 15:38:02');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (108, 135, 2, 1, '{\"push\": {\"time\": \"\"}, \"kaoyan\": {\"types\": [], \"majors\": \"\", \"schools\": \"\", \"keywords\": \"\", \"provinces\": []}, \"kaogong\": {\"types\": [\"公务员\"], \"majors\": \"电子商务\", \"keywords\": \"运营\", \"education\": \"本科\", \"provinces\": [\"四川\"], \"position_types\": [\"公务员\"]}}', '2026-04-20 15:26:16', '2026-04-20 16:43:03');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像URL',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `id_card` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号',
  `gender` tinyint DEFAULT '0' COMMENT '性别: 0-未知, 1-男, 2-女',
  `birthdate` date DEFAULT NULL COMMENT '出生日期',
  `register_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '注册IP',
  `last_login_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `is_active` tinyint DEFAULT '1' COMMENT '是否激活: 1-激活, 0-未激活',
  `is_admin` tinyint DEFAULT '0' COMMENT '是否管理员: 1-是, 0-否',
  `is_vip` tinyint DEFAULT '0' COMMENT '是否VIP: 1-是, 0-否',
  `vip_start_time` datetime DEFAULT NULL COMMENT 'VIP开始时间',
  `vip_end_time` datetime DEFAULT NULL COMMENT 'VIP结束时间',
  `vip_type` tinyint DEFAULT '0' COMMENT 'VIP类型: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP',
  `trial_status` tinyint DEFAULT '0' COMMENT '试用状态: 0-未试用, 1-试用中, 2-已过期',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_phone` (`phone`),
  KEY `idx_vip_type` (`vip_type`),
  KEY `idx_vip_end_time` (`vip_end_time`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`) VALUES (1, 'admin', 'admin@shuangsai.com', '13800138000', '123456789', NULL, '系统管理员', NULL, 0, NULL, NULL, '127.0.0.1', '2026-04-20 17:37:24', 1, 1, 1, '2026-04-16 11:29:54', '2026-07-15 11:29:54', 1, 0, '2026-04-08 20:28:14', '2026-04-20 17:37:24');
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`) VALUES (125, '惠重阳', 'chongyanghui123@gmail.com', '18109271096', '123456789', NULL, '惠重阳', NULL, 1, '2026-04-20', '127.0.0.1', '192.168.1.154', '2026-04-20 09:32:48', 1, 0, 1, '2026-04-17 15:41:16', '2026-07-16 15:41:16', 2, 1, '2026-04-16 15:41:10', '2026-04-20 15:29:22');
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`) VALUES (135, '蒲周泽', '1125864796@qq.com', '18989898989', '123456789', NULL, '蒲周泽', NULL, 1, '2026-03-31', '127.0.0.1', '192.168.1.168', '2026-04-20 16:51:01', 1, 0, 1, '2026-04-21 15:26:21', '2026-07-20 15:26:21', 2, 1, '2026-04-20 15:26:16', '2026-04-20 16:51:01');
COMMIT;

-- ----------------------------
-- View structure for order_statistics_view
-- ----------------------------
DROP VIEW IF EXISTS `order_statistics_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `order_statistics_view` AS select cast(`orders`.`created_at` as date) AS `date`,count(0) AS `total_orders`,sum(`orders`.`total_amount`) AS `total_amount`,count((case when (`orders`.`payment_status` = 1) then 1 end)) AS `paid_orders`,sum((case when (`orders`.`payment_status` = 1) then `orders`.`total_amount` else 0 end)) AS `paid_amount`,sum((case when (`orders`.`payment_status` = 3) then `orders`.`total_amount` else 0 end)) AS `refund_amount` from `orders` group by cast(`orders`.`created_at` as date);

SET FOREIGN_KEY_CHECKS = 1;
