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

 Date: 26/04/2026 09:43:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO `alembic_version` (`version_num`) VALUES ('b272d52f2f32');
COMMIT;

-- ----------------------------
-- Table structure for feedbacks
-- ----------------------------
DROP TABLE IF EXISTS `feedbacks`;
CREATE TABLE `feedbacks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `type` enum('SUGGESTION','PROBLEM','OTHER') NOT NULL,
  `content` text NOT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `status` enum('PENDING','PROCESSED') DEFAULT NULL,
  `reply` text COMMENT '管理员回复',
  `reply_at` datetime DEFAULT NULL COMMENT '回复时间',
  `is_deleted_by_user` tinyint(1) DEFAULT NULL COMMENT '用户是否删除',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_feedbacks_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of feedbacks
-- ----------------------------
BEGIN;
COMMIT;

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
  KEY `uploader_id` (`uploader_id`),
  KEY `ix_learning_materials_subject` (`subject`),
  KEY `ix_learning_materials_id` (`id`),
  KEY `ix_learning_materials_category_id` (`category_id`),
  KEY `ix_learning_materials_type` (`type`),
  CONSTRAINT `learning_materials_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `material_categories` (`id`),
  CONSTRAINT `learning_materials_ibfk_2` FOREIGN KEY (`uploader_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of learning_materials
-- ----------------------------
BEGIN;
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (1, '考公测试资料', '考公测试资料', 2, 7, '测试', 'uploads/361be862-13ab-49a5-89f1-d467da3f3262.txt', '/uploads/361be862-13ab-49a5-89f1-d467da3f3262.txt', 49, '.txt', '/uploads/f2129d8b-2eed-4286-9877-058287198d50.png', 1, '2026-04-22 13:50:32', 0, 0, 1, '2026-04-22 13:50:32', '2026-04-22 13:50:32');
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (2, '考公测试资料', '考公测试资料', 2, 7, '测试', 'uploads/d809c2c6-df9c-43f3-a34f-d6067bbcd1ec.txt', '/uploads/d809c2c6-df9c-43f3-a34f-d6067bbcd1ec.txt', 49, '.txt', '/uploads/1885a9ca-591e-4e09-bf03-46ace29a71eb.png', 1, '2026-04-22 13:54:37', 0, 0, 1, '2026-04-22 13:54:37', '2026-04-22 13:54:37');
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`) VALUES (3, '考研测试资料', '考研测试资料', 1, 1, '111', 'uploads/b3f710bd-81f1-4a06-af90-788b32c22c7c.txt', '/uploads/b3f710bd-81f1-4a06-af90-788b32c22c7c.txt', 49, '.txt', '/uploads/421ab4ef-55bc-41e9-90e3-75ec013389c6.jpg', 1, '2026-04-22 13:55:55', 0, 0, 1, '2026-04-22 13:55:55', '2026-04-24 17:47:48');
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
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (1, '考研政治', 1, '考研政治相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (2, '考研英语', 1, '考研英语相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (3, '考研数学', 1, '考研数学相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (4, '考研专业课', 1, '考研专业课相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (5, '考研复试', 1, '考研复试相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (6, '行测', 2, '公务员考试行测相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (7, '申论', 2, '公务员考试申论相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (8, '面试', 2, '公务员考试面试相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (9, '公共基础知识', 2, '公共基础知识相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (10, '学习方法', 3, '学习方法相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (11, '时间管理', 3, '时间管理相关资料', '2026-04-22 12:25:21');
INSERT INTO `material_categories` (`id`, `name`, `type`, `description`, `created_at`) VALUES (12, '心理调适', 3, '心理调适相关资料', '2026-04-22 12:25:21');
COMMIT;

-- ----------------------------
-- Table structure for material_comments
-- ----------------------------
DROP TABLE IF EXISTS `material_comments`;
CREATE TABLE `material_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `material_id` int NOT NULL COMMENT '资料ID',
  `parent_comment_id` int DEFAULT NULL COMMENT '父评论ID（回复功能）',
  `comment` text NOT NULL COMMENT '评论内容',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `material_id` (`material_id`),
  KEY `parent_comment_id` (`parent_comment_id`),
  KEY `ix_material_comments_id` (`id`),
  CONSTRAINT `material_comments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `material_comments_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `learning_materials` (`id`),
  CONSTRAINT `material_comments_ibfk_3` FOREIGN KEY (`parent_comment_id`) REFERENCES `material_comments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_comments
-- ----------------------------
BEGIN;
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
  KEY `user_id` (`user_id`),
  KEY `material_id` (`material_id`),
  KEY `ix_material_ratings_id` (`id`),
  CONSTRAINT `material_ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `material_ratings_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `learning_materials` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_ratings
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单编号',
  `user_id` int NOT NULL COMMENT '用户ID',
  `product_id` int NOT NULL COMMENT '产品ID',
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `price` float NOT NULL COMMENT '价格',
  `quantity` int DEFAULT '1' COMMENT '数量',
  `total_amount` float NOT NULL COMMENT '总金额',
  `payment_method` int NOT NULL COMMENT '支付方式: 1-微信支付, 2-支付宝',
  `payment_status` int DEFAULT '0' COMMENT '支付状态: 0-待支付, 1-已支付, 2-已取消, 3-已退款',
  `trade_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付平台交易号',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `refund_time` datetime DEFAULT NULL COMMENT '退款时间',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `user_requirements` json DEFAULT NULL COMMENT '用户需求信息JSON',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of orders
-- ----------------------------
BEGIN;
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (101, 'ORDER202604221840211404', 140, 4, '考公VIP月卡', 49, 1, 49, 1, 1, NULL, '2026-04-22 18:40:26', NULL, NULL, '2026-04-22 18:40:21', '2026-04-22 18:40:26', '{\"email\": \"chongyanghui123@gmail.com\", \"phone\": \"18989898989\", \"gender\": \"男\", \"username\": \"惠重阳\", \"birthdate\": \"2026-04-26\", \"real_name\": \"惠重阳\", \"kaoyan_requirements\": null, \"kaogong_requirements\": {\"majors\": \"推送热带鱼\", \"keywords\": \"人太多衣服\", \"education\": \"不限\", \"provinces\": [\"云南\"], \"position_types\": [\"教师\"], \"is_fresh_graduate\": \"是\"}}');
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (102, 'ORDER202604241804191412', 141, 2, '考研VIP季卡', 99, 1, 99, 1, 1, NULL, '2026-04-24 18:04:24', NULL, NULL, '2026-04-24 18:04:20', '2026-04-24 18:04:24', '{\"email\": \"chongyanghui123@gmail.com\", \"phone\": \"18989898989\", \"gender\": \"男\", \"username\": \"惠重阳\", \"birthdate\": \"2026-04-13\", \"real_name\": \"惠重阳\", \"kaoyan_requirements\": {\"types\": [\"考试大纲\"], \"majors\": \"软件工程\", \"schools\": \"安徽理工大学\", \"keywords\": \"计算机软件\", \"provinces\": [\"安徽\", \"云南\"]}, \"kaogong_requirements\": null}');
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (103, 'ORDER202604242149391422', 142, 2, '考研VIP季卡', 99, 1, 99, 1, 1, NULL, '2026-04-24 21:49:48', NULL, NULL, '2026-04-24 21:49:39', '2026-04-24 21:49:48', '{\"email\": \"1125864796@qq.com\", \"phone\": \"18017243981\", \"gender\": \"男\", \"username\": \"蒲洲泽\", \"birthdate\": \"2026-03-31\", \"real_name\": \"蒲洲泽\", \"kaoyan_requirements\": {\"types\": [\"考试大纲\", \"招生简章\"], \"majors\": \"金融学\", \"schools\": \"复旦大学\", \"keywords\": \"金融\", \"provinces\": [\"上海\"]}, \"kaogong_requirements\": null}');
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (104, 'ORDER202604242152461432', 143, 2, '考研VIP季卡', 99, 1, 99, 1, 1, NULL, '2026-04-24 21:52:52', NULL, NULL, '2026-04-24 21:52:46', '2026-04-24 21:52:52', '{\"email\": \"1322835898@qq.com\", \"phone\": \"18109271096\", \"gender\": \"男\", \"username\": \"惠阳\", \"birthdate\": \"2026-03-30\", \"real_name\": \"惠阳\", \"kaoyan_requirements\": {\"types\": [\"招生简章\"], \"majors\": \"fhgj\", \"schools\": \"云南师范大学\", \"keywords\": \"tfyghjk\", \"provinces\": [\"云南\"]}, \"kaogong_requirements\": null}');
COMMIT;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '产品描述',
  `price` float NOT NULL COMMENT '价格',
  `original_price` float DEFAULT NULL COMMENT '原价',
  `type` int NOT NULL COMMENT '产品类型: 1-考研VIP, 2-考公VIP, 3-双赛道VIP',
  `duration` int NOT NULL COMMENT '有效期(天)',
  `features` json DEFAULT NULL COMMENT '产品特色JSON',
  `status` int DEFAULT '1' COMMENT '状态: 1-上架, 0-下架',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (2, '考研VIP季卡', '考研赛道季度订阅，优惠更多，包含所有月卡功能', 99, 177, 1, 90, '[]', 1, 2, '2026-04-08 20:28:14', '2026-04-16 01:20:14');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (3, '考研VIP年卡', '考研赛道年度订阅，最优惠选择，包含所有月卡功能', 299, 708, 1, 365, '{\"features\": [\"考研全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"年度数据分析\", \"专属客服\"]}', 1, 3, '2026-04-08 20:28:14', '2026-04-16 15:21:03');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (4, '考公VIP月卡', '考公赛道全方位情报监控，包含国考、省考等关键信息推送', 49, 69, 2, 30, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"3天免费试用\"]}', 1, 4, '2026-04-08 20:28:14', '2026-04-15 16:56:52');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (5, '考公VIP季卡', '考公赛道季度订阅，优惠更多，包含所有月卡功能', 119, 207, 2, 90, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"季度数据统计\"]}', 1, 5, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
COMMIT;

-- ----------------------------
-- Table structure for push_logs
-- ----------------------------
DROP TABLE IF EXISTS `push_logs`;
CREATE TABLE `push_logs` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `info_id` int NOT NULL COMMENT '信息ID',
  `category` int NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `push_type` int NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
  `push_status` int NOT NULL COMMENT '推送状态: 1-成功, 0-失败',
  `push_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '推送内容',
  `error_msg` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `push_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '推送时间',
  `is_processed` tinyint(1) DEFAULT '0' COMMENT '是否处理: 1-是, 0-否',
  `read` tinyint(1) DEFAULT NULL COMMENT '是否已读: 1-是, 0-否',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of push_logs
-- ----------------------------
BEGIN;
INSERT INTO `push_logs` (`id`, `user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`, `error_msg`, `push_time`, `is_processed`, `read`) VALUES (79, 141, 102, 3, 3, 1, '【支付成功】您的考研推送服务已开通', NULL, '2026-04-24 18:04:25', 1, 1);
INSERT INTO `push_logs` (`id`, `user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`, `error_msg`, `push_time`, `is_processed`, `read`) VALUES (80, 142, 103, 3, 3, 1, '【系统通知】【支付成功】您的考研推送服务已开通', NULL, '2026-04-24 21:49:48', 1, 0);
INSERT INTO `push_logs` (`id`, `user_id`, `info_id`, `category`, `push_type`, `push_status`, `push_content`, `error_msg`, `push_time`, `is_processed`, `read`) VALUES (81, 143, 104, 3, 3, 1, '【系统通知】【支付成功】您的考研推送服务已开通', NULL, '2026-04-24 21:52:52', 1, 0);
COMMIT;

-- ----------------------------
-- Table structure for push_templates
-- ----------------------------
DROP TABLE IF EXISTS `push_templates`;
CREATE TABLE `push_templates` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '模板ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `type` int NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
  `template_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '第三方模板ID',
  `template_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '模板内容',
  `status` int DEFAULT '1' COMMENT '状态: 1-启用, 0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  `province` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `has_master` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_schools_id` (`id`),
  KEY `ix_schools_name` (`name`),
  KEY `ix_schools_province` (`province`)
) ENGINE=InnoDB AUTO_INCREMENT=218 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of schools
-- ----------------------------
BEGIN;
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (1, '北京', '北京大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (2, '北京', '清华大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (3, '北京', '中国人民大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (4, '北京', '北京师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (5, '北京', '北京航空航天大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (6, '北京', '北京理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (7, '北京', '北京科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (8, '北京', '北京交通大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (9, '北京', '北京邮电大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (10, '北京', '北京林业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (11, '上海', '复旦大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (12, '上海', '上海交通大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (13, '上海', '同济大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (14, '上海', '华东师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (15, '上海', '上海财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (16, '上海', '上海外国语大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (17, '上海', '东华大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (18, '上海', '华东理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (19, '上海', '上海大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (20, '上海', '上海理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (21, '广东', '中山大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (22, '广东', '华南理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (23, '广东', '暨南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (24, '广东', '华南师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (25, '广东', '华南农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (26, '广东', '深圳大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (27, '广东', '广州大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (28, '广东', '南方医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (29, '广东', '广东工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (30, '广东', '汕头大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (31, '浙江', '浙江大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (32, '浙江', '宁波大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (33, '浙江', '浙江工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (34, '浙江', '浙江师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (35, '浙江', '杭州电子科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (36, '浙江', '浙江理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (37, '浙江', '浙江工商大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (38, '浙江', '浙江农林大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (39, '浙江', '温州大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (40, '浙江', '中国计量大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (41, '江苏', '南京大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (42, '江苏', '东南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (43, '江苏', '南京理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (44, '江苏', '南京航空航天大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (45, '江苏', '河海大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (46, '江苏', '南京农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (47, '江苏', '南京师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (48, '江苏', '苏州大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (49, '江苏', '江南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (50, '江苏', '中国矿业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (51, '湖北', '武汉大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (52, '湖北', '华中科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (53, '湖北', '武汉理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (54, '湖北', '华中师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (55, '湖北', '华中农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (56, '湖北', '中南财经政法大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (57, '湖北', '武汉科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (58, '湖北', '长江大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (59, '湖北', '三峡大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (60, '湖北', '湖北大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (61, '四川', '四川大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (62, '四川', '电子科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (63, '四川', '西南交通大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (64, '四川', '西南财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (65, '四川', '四川农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (66, '四川', '西南石油大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (67, '四川', '成都理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (68, '四川', '西南民族大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (69, '四川', '成都信息工程大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (70, '四川', '西华大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (71, '陕西', '西安交通大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (72, '陕西', '西北工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (73, '陕西', '西安电子科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (74, '陕西', '西北农林科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (75, '陕西', '陕西师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (76, '陕西', '长安大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (77, '陕西', '西安理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (78, '陕西', '西安建筑科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (79, '陕西', '西北大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (80, '陕西', '西安科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (81, '山东', '山东大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (82, '山东', '中国海洋大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (83, '山东', '中国石油大学(华东)', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (84, '山东', '山东师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (85, '山东', '山东农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (86, '山东', '青岛大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (87, '山东', '济南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (88, '山东', '青岛科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (89, '山东', '山东科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (90, '山东', '曲阜师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (91, '辽宁', '东北大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (92, '辽宁', '大连理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (93, '辽宁', '大连海事大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (94, '辽宁', '东北财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (95, '辽宁', '辽宁大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (96, '辽宁', '大连大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (97, '辽宁', '沈阳工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (98, '辽宁', '沈阳航空航天大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (99, '辽宁', '沈阳理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (100, '辽宁', '辽宁师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (101, '湖南', '中南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (102, '湖南', '湖南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (103, '湖南', '湖南师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (104, '湖南', '湘潭大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (105, '湖南', '长沙理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (106, '湖南', '湖南农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (107, '湖南', '中南林业科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (108, '湖南', '湖南科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (109, '湖南', '南华大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (110, '湖南', '吉首大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (111, '安徽', '中国科学技术大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (112, '安徽', '合肥工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (113, '安徽', '安徽大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (114, '安徽', '安徽师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (115, '安徽', '安徽农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (116, '安徽', '安徽工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (117, '安徽', '安徽理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (118, '安徽', '安徽财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (119, '安徽', '安徽建筑大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (120, '安徽', '合肥学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (121, '福建', '厦门大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (122, '福建', '福州大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (123, '福建', '福建师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (124, '福建', '华侨大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (125, '福建', '福建农林大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (126, '福建', '集美大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (127, '福建', '福建医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (128, '福建', '福建中医药大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (129, '福建', '闽南师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (130, '福建', '宁德师范学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (131, '河北', '河北大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (132, '河北', '燕山大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (133, '河北', '河北工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (134, '河北', '河北师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (135, '河北', '河北农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (136, '河北', '河北医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (137, '河北', '河北科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (138, '河北', '河北工程大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (139, '河北', '河北经贸大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (140, '河北', '石家庄铁道大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (141, '河南', '郑州大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (142, '河南', '河南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (143, '河南', '河南理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (144, '河南', '河南农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (145, '河南', '河南师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (146, '河南', '河南科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (147, '河南', '河南工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (148, '河南', '华北水利水电大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (149, '河南', '河南财经政法大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (150, '河南', '中原工学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (151, '黑龙江', '哈尔滨工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (152, '黑龙江', '哈尔滨工程大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (153, '黑龙江', '东北农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (154, '黑龙江', '东北林业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (155, '黑龙江', '黑龙江大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (156, '黑龙江', '哈尔滨医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (157, '黑龙江', '哈尔滨师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (158, '黑龙江', '哈尔滨理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (159, '黑龙江', '东北石油大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (160, '黑龙江', '佳木斯大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (161, '吉林', '吉林大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (162, '吉林', '东北师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (163, '吉林', '长春理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (164, '吉林', '延边大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (165, '吉林', '吉林农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (166, '吉林', '长春工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (167, '吉林', '吉林师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (168, '吉林', '东北电力大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (169, '吉林', '长春大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (170, '吉林', '北华大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (171, '重庆', '重庆大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (172, '重庆', '西南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (173, '重庆', '重庆邮电大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (174, '重庆', '重庆交通大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (175, '重庆', '重庆师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (176, '重庆', '重庆医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (177, '重庆', '重庆工商大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (178, '重庆', '西南政法大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (179, '重庆', '重庆理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (180, '重庆', '重庆科技学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (181, '天津', '南开大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (182, '天津', '天津大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (183, '天津', '天津医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (184, '天津', '天津师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (185, '天津', '天津工业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (186, '天津', '天津理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (187, '天津', '天津财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (188, '天津', '中国民航大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (189, '天津', '天津科技大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (190, '天津', '天津城建大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (191, '江西', '南昌大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (192, '江西', '江西师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (193, '江西', '江西财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (194, '江西', '南昌航空大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (195, '江西', '江西理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (196, '江西', '华东交通大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (197, '江西', '南昌工程学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (198, '江西', '井冈山大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (199, '江西', '赣南师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (200, '江西', '九江学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (201, '云南', '云南大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (202, '云南', '昆明理工大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (203, '云南', '云南师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (204, '云南', '云南农业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (205, '云南', '云南财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (206, '云南', '昆明医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (207, '云南', '云南民族大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (208, '云南', '西南林业大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (209, '云南', '大理大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (210, '云南', '曲靖师范学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (211, '贵州', '贵州大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (212, '贵州', '贵州师范大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (213, '贵州', '贵州医科大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (214, '贵州', '贵州财经大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (215, '贵州', '贵州民族大学', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (216, '贵州', '贵州师范学院', 1, '2026-04-23 19:32:49', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (217, '贵州', '遵义医科大学', 1, '2026-04-23 19:32:49', NULL);
COMMIT;

-- ----------------------------
-- Table structure for system_config
-- ----------------------------
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置键',
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '配置值',
  `config_type` int DEFAULT '0' COMMENT '配置类型: 0-字符串, 1-数字, 2-布尔值, 3-JSON',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置描述',
  `is_system` tinyint DEFAULT '0' COMMENT '是否系统配置: 1-是, 0-否',
  `status` int DEFAULT '1' COMMENT '状态: 1-启用, 0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  KEY `ix_user_downloads_material_id` (`material_id`),
  CONSTRAINT `user_downloads_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_downloads_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `learning_materials` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  `id` int NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `info_id` int NOT NULL COMMENT '信息ID',
  `category` int NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  `id` int NOT NULL AUTO_INCREMENT COMMENT '关键词ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `keyword` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关键词',
  `category` int NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用: 1-是, 0-否',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=241 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_keywords
-- ----------------------------
BEGIN;
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (146, 1, '人工智能', 1, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (147, 1, '机器学习', 1, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (148, 1, '公务员', 2, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (149, 1, '国考', 2, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (236, 141, '计算机软件', 1, 1, '2026-04-24 18:04:20', '2026-04-24 18:04:20');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (238, 142, '金融', 1, 1, '2026-04-24 21:49:39', '2026-04-24 21:49:39');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (240, 143, 'tfyghjk', 1, 1, '2026-04-24 21:52:46', '2026-04-24 21:52:46');
COMMIT;

-- ----------------------------
-- Table structure for user_material_favorites
-- ----------------------------
DROP TABLE IF EXISTS `user_material_favorites`;
CREATE TABLE `user_material_favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `material_id` int NOT NULL COMMENT '资料ID',
  `created_at` datetime DEFAULT NULL COMMENT '收藏时间',
  PRIMARY KEY (`id`),
  KEY `ix_user_material_favorites_id` (`id`),
  KEY `ix_user_material_favorites_user_id` (`user_id`),
  KEY `ix_user_material_favorites_material_id` (`material_id`),
  CONSTRAINT `user_material_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_material_favorites_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `learning_materials` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user_material_favorites
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_read_info
-- ----------------------------
DROP TABLE IF EXISTS `user_read_info`;
CREATE TABLE `user_read_info` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '已读ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `info_id` int NOT NULL COMMENT '信息ID',
  `category` int NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `read_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '阅读时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_read_info
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_subscriptions
-- ----------------------------
DROP TABLE IF EXISTS `user_subscriptions`;
CREATE TABLE `user_subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订阅ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `subscribe_type` int NOT NULL COMMENT '订阅类型: 1-考研, 2-考公, 3-双赛道',
  `status` int DEFAULT '1' COMMENT '订阅状态: 1-有效, 0-无效',
  `config_json` json DEFAULT NULL COMMENT '订阅配置JSON',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_subscriptions
-- ----------------------------
BEGIN;
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (71, 1, 1, 1, '{\"kaoyan_requirements\": {\"types\": [\"录取通知\"], \"majors\": [\"计算机科学\"], \"schools\": [\"复旦大学\"], \"keywords\": \"人工智能,机器学习\", \"provinces\": [\"上海\"]}, \"kaogong_requirements\": {\"majors\": [\"不限\"], \"keywords\": \"公务员,国考\", \"education\": [\"本科\"], \"provinces\": [\"北京\"], \"position_types\": [\"综合管理\"], \"is_fresh_graduate\": \"是\"}}', '2026-04-15 03:14:44', '2026-04-15 03:16:17');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (113, 141, 1, 1, '{\"kaoyan\": {\"types\": [\"考试大纲\"], \"majors\": \"软件工程\", \"schools\": \"安徽理工大学\", \"keywords\": \"计算机软件\", \"provinces\": [\"安徽\", \"云南\"]}, \"kaogong\": null}', '2026-04-24 18:04:19', '2026-04-24 18:04:20');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (114, 142, 1, 1, '{\"kaoyan\": {\"types\": [\"考试大纲\", \"招生简章\"], \"majors\": \"金融学\", \"schools\": \"复旦大学\", \"keywords\": \"金融\", \"provinces\": [\"上海\"]}, \"kaogong\": null}', '2026-04-24 21:49:38', '2026-04-24 21:49:39');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (115, 143, 1, 1, '{\"kaoyan\": {\"types\": [\"招生简章\"], \"majors\": \"fhgj\", \"schools\": \"云南师范大学\", \"keywords\": \"tfyghjk\", \"provinces\": [\"云南\"]}, \"kaogong\": null}', '2026-04-24 21:52:46', '2026-04-24 21:52:46');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '密码（仅管理员用户需要）',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像URL',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `id_card` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号',
  `gender` int DEFAULT '0' COMMENT '性别: 0-未知, 1-男, 2-女',
  `birthdate` datetime DEFAULT NULL COMMENT '出生日期',
  `register_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '注册IP',
  `last_login_ip` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `is_active` tinyint DEFAULT '1' COMMENT '是否激活: 1-激活, 0-未激活',
  `is_admin` tinyint DEFAULT '0' COMMENT '是否管理员: 1-是, 0-否',
  `is_vip` tinyint DEFAULT '0' COMMENT '是否VIP: 1-是, 0-否',
  `vip_start_time` datetime DEFAULT NULL COMMENT 'VIP开始时间',
  `vip_end_time` datetime DEFAULT NULL COMMENT 'VIP结束时间',
  `vip_type` int DEFAULT '0' COMMENT 'VIP类型: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP',
  `trial_status` int DEFAULT '0' COMMENT '试用状态: 0-未试用, 1-试用中, 2-已过期',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `need_change_password` tinyint(1) DEFAULT NULL COMMENT '是否需要修改密码: 1-是, 0-否',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`) VALUES (1, 'admin', 'admin@shuangsai.com', '13800138000', '123456789', NULL, '系统管理员', NULL, 0, NULL, NULL, '127.0.0.1', '2026-04-24 14:58:41', 1, 1, 1, '2026-04-16 11:29:54', '2026-07-15 11:29:54', 1, 0, '2026-04-08 20:28:14', '2026-04-24 14:58:41', 1);
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`) VALUES (141, '惠重阳', 'chongyanghui123@gmail.com', '18989898989', '123456789', NULL, '惠重阳', NULL, 1, '2026-04-13 00:00:00', '127.0.0.1', '127.0.0.1', '2026-04-24 22:09:34', 1, 0, 1, '2026-04-25 18:04:24', '2026-07-24 18:04:24', 1, 1, '2026-04-24 18:04:19', '2026-04-24 22:09:34', 0);
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`) VALUES (142, '蒲洲泽', '1125864796@qq.com', '18017243981', 'changeme123', NULL, '蒲洲泽', NULL, 1, '2026-03-31 00:00:00', '127.0.0.1', NULL, NULL, 1, 0, 1, '2026-04-25 21:49:48', '2026-07-24 21:49:48', 1, 1, '2026-04-24 21:49:38', '2026-04-24 21:49:48', 1);
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`) VALUES (143, '惠阳', '1322835898@qq.com', '18109271096', 'changeme123', NULL, '惠阳', NULL, 1, '2026-03-30 00:00:00', '127.0.0.1', NULL, NULL, 1, 0, 1, '2026-04-25 21:52:52', '2026-07-24 21:52:52', 1, 1, '2026-04-24 21:52:46', '2026-04-24 21:52:52', 1);
COMMIT;

-- ----------------------------
-- View structure for order_statistics_view
-- ----------------------------
DROP VIEW IF EXISTS `order_statistics_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `order_statistics_view` AS select cast(`orders`.`created_at` as date) AS `date`,count(0) AS `total_orders`,sum(`orders`.`total_amount`) AS `total_amount`,count((case when (`orders`.`payment_status` = 1) then 1 end)) AS `paid_orders`,sum((case when (`orders`.`payment_status` = 1) then `orders`.`total_amount` else 0 end)) AS `paid_amount`,sum((case when (`orders`.`payment_status` = 3) then `orders`.`total_amount` else 0 end)) AS `refund_amount` from `orders` group by cast(`orders`.`created_at` as date);

SET FOREIGN_KEY_CHECKS = 1;
