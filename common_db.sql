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

 Date: 12/04/2026 23:29:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单编号',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `product_id` bigint unsigned NOT NULL COMMENT '产品ID',
  `product_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `quantity` int DEFAULT '1' COMMENT '数量',
  `total_amount` decimal(10,2) NOT NULL COMMENT '总金额',
  `payment_method` tinyint NOT NULL COMMENT '支付方式: 1-微信支付, 2-支付宝',
  `payment_status` tinyint DEFAULT '0' COMMENT '支付状态: 0-待支付, 1-已支付, 2-已取消, 3-已退款',
  `trade_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '支付平台交易号',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `refund_time` datetime DEFAULT NULL COMMENT '退款时间',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  UNIQUE KEY `uk_trade_no` (`trade_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_payment_status` (`payment_status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- ----------------------------
-- Records of orders
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '产品名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '产品描述',
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='产品/套餐表';

-- ----------------------------
-- Records of products
-- ----------------------------
BEGIN;
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (2, '考研VIP季卡1', '考研赛道季度订阅，优惠更多，包含所有月卡功能', 99.00, 177.00, 1, 90, '[]', 1, 2, '2026-04-08 20:28:14', '2026-04-12 18:39:30');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (3, '考研VIP年卡', '考研赛道年度订阅，最优惠选择，包含所有月卡功能', 299.00, 708.00, 1, 365, '{\"features\": [\"考研全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"年度数据分析\", \"专属客服\"]}', 1, 3, '2026-04-08 20:28:14', '2026-04-12 18:39:32');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (4, '考公VIP月卡', '考公赛道全方位情报监控，包含国考、省考等关键信息推送', 49.00, 69.00, 2, 30, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"3天免费试用\"]}', 1, 4, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (5, '考公VIP季卡', '考公赛道季度订阅，优惠更多，包含所有月卡功能', 119.00, 207.00, 2, 90, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"季度数据统计\"]}', 1, 5, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (6, '考公VIP年卡', '考公赛道年度订阅，最优惠选择，包含所有月卡功能', 359.00, 828.00, 2, 365, '{\"features\": [\"考公全赛道监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"年度数据分析\", \"专属客服\"]}', 1, 6, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `products` (`id`, `name`, `description`, `price`, `original_price`, `type`, `duration`, `features`, `status`, `sort_order`, `created_at`, `updated_at`) VALUES (7, '双赛道VIP年卡', '考研+考公双赛道全方位情报监控，性价比最高', 499.00, 658.00, 3, 365, '{\"features\": [\"双赛道全监控\", \"实时推送\", \"智能分类\", \"优先级提醒\", \"年度数据分析\", \"专属客服\", \"双赛道对比\"]}', 1, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
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
  `push_content` text COLLATE utf8mb4_unicode_ci COMMENT '推送内容',
  `error_msg` text COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `push_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '推送时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_info_id` (`info_id`),
  KEY `idx_push_type` (`push_type`),
  KEY `idx_push_status` (`push_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推送日志表';

-- ----------------------------
-- Records of push_logs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for push_templates
-- ----------------------------
DROP TABLE IF EXISTS `push_templates`;
CREATE TABLE `push_templates` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '模板ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `type` tinyint NOT NULL COMMENT '推送类型: 1-微信模板消息, 2-企业微信, 3-短信',
  `template_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '第三方模板ID',
  `template_content` text COLLATE utf8mb4_unicode_ci COMMENT '模板内容',
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
  `province` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `has_master` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_schools_id` (`id`),
  KEY `ix_schools_name` (`name`),
  KEY `ix_schools_province` (`province`)
) ENGINE=InnoDB AUTO_INCREMENT=367 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of schools
-- ----------------------------
BEGIN;
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (23, '天津', '天津工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (24, '天津', '天津理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (25, '天津', '天津医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (26, '天津', '天津中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (27, '天津', '天津师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (28, '天津', '天津财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (29, '天津', '天津科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (30, '天津', '天津职业技术师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (31, '河北', '河北大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (32, '河北', '河北工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (33, '河北', '燕山大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (34, '河北', '河北师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (35, '河北', '河北农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (36, '河北', '河北医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (37, '河北', '河北科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (38, '河北', '华北电力大学（保定）', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (39, '河北', '石家庄铁道大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (40, '河北', '河北经贸大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (41, '山西', '山西大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (42, '山西', '太原理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (46, '山西', '中北大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (47, '山西', '山西财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (48, '山西', '太原科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (49, '山西', '山西大同大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (50, '山西', '太原师范学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (51, '内蒙古', '内蒙古大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (52, '内蒙古', '内蒙古工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (53, '内蒙古', '内蒙古农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (54, '内蒙古', '内蒙古师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (55, '内蒙古', '内蒙古科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (56, '内蒙古', '内蒙古民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (57, '内蒙古', '内蒙古财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (58, '辽宁', '大连理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (59, '辽宁', '东北大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (60, '辽宁', '辽宁大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (61, '辽宁', '大连海事大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (62, '辽宁', '沈阳工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (63, '辽宁', '沈阳农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (64, '辽宁', '中国医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (65, '辽宁', '辽宁师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (66, '辽宁', '东北财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (67, '辽宁', '沈阳药科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (68, '吉林', '吉林大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (69, '吉林', '东北师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (70, '吉林', '延边大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (71, '吉林', '长春理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (72, '吉林', '长春工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (73, '吉林', '吉林农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (74, '吉林', '吉林师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (75, '吉林', '东北电力大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (76, '吉林', '吉林财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (77, '吉林', '北华大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (78, '黑龙江', '哈尔滨工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (79, '黑龙江', '哈尔滨工程大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (80, '黑龙江', '东北农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (81, '黑龙江', '东北林业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (82, '黑龙江', '哈尔滨医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (83, '黑龙江', '黑龙江大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (84, '黑龙江', '哈尔滨师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (85, '黑龙江', '哈尔滨理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (86, '黑龙江', '东北石油大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (87, '黑龙江', '佳木斯大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (88, '上海', '复旦大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (89, '上海', '上海交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (90, '上海', '同济大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (91, '上海', '华东师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (92, '上海', '上海大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (93, '上海', '华东理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (94, '上海', '东华大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (95, '上海', '上海财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (96, '上海', '上海外国语大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (97, '上海', '上海师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (98, '上海', '华东政法大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (99, '上海', '上海海事大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (100, '上海', '上海理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (101, '上海', '上海中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (102, '上海', '上海海洋大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (103, '江苏', '南京大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (104, '江苏', '东南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (105, '江苏', '苏州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (106, '江苏', '南京航空航天大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (107, '江苏', '南京理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (108, '江苏', '河海大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (109, '江苏', '江南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (110, '江苏', '南京农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (111, '江苏', '中国药科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (112, '江苏', '南京师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (113, '江苏', '扬州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (114, '江苏', '江苏大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (115, '江苏', '南京工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (116, '江苏', '南京邮电大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (117, '江苏', '南京林业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (118, '江苏', '南京医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (119, '江苏', '南京中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (120, '江苏', '江苏师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (121, '江苏', '南通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (122, '江苏', '常州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (123, '浙江', '浙江大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (124, '浙江', '宁波大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (125, '浙江', '浙江工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (126, '浙江', '浙江师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (127, '浙江', '杭州电子科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (128, '浙江', '浙江理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (129, '浙江', '温州医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (130, '浙江', '浙江工商大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (131, '浙江', '杭州师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (132, '浙江', '温州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (133, '浙江', '浙江农林大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (134, '浙江', '中国计量大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (135, '浙江', '浙江中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (136, '浙江', '浙江财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (137, '安徽', '中国科学技术大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (138, '安徽', '合肥工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (139, '安徽', '安徽大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (140, '安徽', '安徽师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (141, '安徽', '安徽农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (142, '安徽', '安徽医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (143, '安徽', '安徽理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (144, '安徽', '安徽财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (145, '安徽', '合肥学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (146, '安徽', '淮北师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (147, '福建', '厦门大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (148, '福建', '福州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (149, '福建', '福建师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (150, '福建', '福建农林大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (151, '福建', '福建医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (152, '福建', '华侨大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (153, '福建', '集美大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (154, '福建', '福建中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (155, '福建', '闽南师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (156, '福建', '福州师范学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (157, '江西', '南昌大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (158, '江西', '江西师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (159, '江西', '江西财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (160, '江西', '江西农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (161, '江西', '南昌航空大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (162, '江西', '华东交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (163, '江西', '东华理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (164, '江西', '江西理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (165, '江西', '井冈山大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (166, '江西', '江西中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (167, '山东', '山东大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (168, '山东', '中国海洋大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (169, '山东', '中国石油大学（华东）', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (170, '山东', '山东师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (171, '山东', '山东科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (172, '山东', '青岛大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (173, '山东', '济南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (174, '山东', '山东农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (175, '山东', '青岛科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (176, '山东', '山东理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (177, '山东', '曲阜师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (178, '山东', '烟台大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (179, '山东', '鲁东大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (180, '山东', '山东财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (181, '山东', '青岛理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (182, '山东', '山东建筑大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (183, '山东', '山东中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (184, '河南', '郑州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (185, '河南', '河南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (186, '河南', '河南师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (187, '河南', '河南农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (188, '河南', '河南科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (189, '河南', '河南理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (190, '河南', '河南工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (191, '河南', '河南财经政法大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (192, '河南', '华北水利水电大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (193, '河南', '新乡医学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (194, '湖北', '武汉大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (195, '湖北', '华中科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (196, '湖北', '华中师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (197, '湖北', '武汉理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (198, '湖北', '中国地质大学（武汉）', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (199, '湖北', '华中农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (200, '湖北', '中南财经政法大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (201, '湖北', '湖北大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (202, '湖北', '武汉科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (203, '湖北', '长江大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (204, '湖北', '三峡大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (205, '湖北', '湖北工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (206, '湖北', '武汉工程大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (207, '湖北', '武汉纺织大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (208, '湖北', '武汉轻工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (209, '湖北', '湖北中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (210, '湖北', '江汉大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (211, '湖南', '中南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (212, '湖南', '湖南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (213, '湖南', '湖南师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (214, '湖南', '湘潭大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (215, '湖南', '长沙理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (216, '湖南', '湖南科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (217, '湖南', '湖南农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (218, '湖南', '中南林业科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (219, '湖南', '湖南中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (220, '湖南', '南华大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (221, '湖南', '湖南工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (222, '湖南', '吉首大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (223, '广东', '中山大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (224, '广东', '华南理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (225, '广东', '暨南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (226, '广东', '华南师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (227, '广东', '深圳大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (228, '广东', '华南农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (229, '广东', '广州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (230, '广东', '广东工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (231, '广东', '汕头大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (232, '广东', '广东外语外贸大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (233, '广东', '南方医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (234, '广东', '广州中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (235, '广西', '广西大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (236, '广西', '广西师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (237, '广西', '广西医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (238, '广西', '桂林电子科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (239, '广西', '桂林理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (240, '广西', '广西民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (241, '广西', '广西中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (242, '广西', '南宁师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (243, '广西', '广西科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (244, '广西', '桂林医学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (245, '海南', '海南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (246, '海南', '海南师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (247, '海南', '海南医学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (248, '海南', '海南热带海洋学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (249, '海南', '琼州学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (250, '重庆', '重庆大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (251, '重庆', '西南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (252, '重庆', '重庆邮电大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (253, '重庆', '重庆交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (254, '重庆', '重庆医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (255, '重庆', '重庆师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (256, '重庆', '重庆理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (257, '重庆', '重庆工商大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (258, '重庆', '西南政法大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (259, '重庆', '四川外国语大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (260, '四川', '四川大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (261, '四川', '电子科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (262, '四川', '西南交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (263, '四川', '西南财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (264, '四川', '四川农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (265, '四川', '成都理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (266, '四川', '西南石油大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (267, '四川', '成都中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (268, '四川', '四川师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (269, '四川', '西华大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (270, '四川', '西南科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (271, '四川', '成都信息工程大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (272, '四川', '成都大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (273, '四川', '四川轻化工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (274, '四川', '西华师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (275, '贵州', '贵州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (276, '贵州', '贵州师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (277, '贵州', '贵州医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (278, '贵州', '贵州民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (279, '贵州', '贵州财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (280, '贵州', '遵义医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (281, '贵州', '贵州师范学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (282, '贵州', '贵阳学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (283, '贵州', '黔南民族师范学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (284, '贵州', '贵州工程应用技术学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (285, '云南', '云南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (286, '云南', '昆明理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (287, '云南', '云南师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (288, '云南', '云南农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (289, '云南', '昆明医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (290, '云南', '云南民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (291, '云南', '西南林业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (292, '云南', '云南财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (293, '云南', '大理大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (294, '云南', '云南中医学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (295, '西藏', '西藏大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (296, '西藏', '西藏民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (297, '西藏', '西藏藏医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (298, '陕西', '西安交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (299, '陕西', '西北工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (300, '陕西', '西安电子科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (301, '陕西', '西北农林科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (302, '陕西', '陕西师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (303, '陕西', '长安大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (304, '陕西', '西北大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (305, '陕西', '西安理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (306, '陕西', '西安建筑科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (307, '陕西', '陕西科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (308, '陕西', '西安科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (309, '陕西', '西安石油大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (310, '陕西', '延安大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (311, '陕西', '西安工业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (312, '陕西', '西安工程大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (313, '陕西', '西安外国语大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (314, '陕西', '西北政法大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (315, '陕西', '西安邮电大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (316, '陕西', '西安财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (317, '陕西', '陕西理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (318, '甘肃', '兰州大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (319, '甘肃', '西北师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (320, '甘肃', '兰州理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (321, '甘肃', '兰州交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (322, '甘肃', '甘肃农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (323, '甘肃', '兰州财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (324, '甘肃', '甘肃中医药大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (325, '甘肃', '河西学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (326, '甘肃', '陇东学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (327, '甘肃', '天水师范学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (328, '青海', '青海大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (329, '青海', '青海师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (330, '青海', '青海民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (331, '宁夏', '宁夏大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (332, '宁夏', '宁夏医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (333, '宁夏', '北方民族大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (334, '宁夏', '宁夏师范学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (335, '新疆', '新疆大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (336, '新疆', '石河子大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (337, '新疆', '新疆师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (338, '新疆', '新疆农业大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (339, '新疆', '新疆医科大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (340, '新疆', '新疆财经大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (341, '新疆', '塔里木大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (342, '新疆', '喀什大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (343, '新疆', '伊犁师范大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (344, '新疆', '新疆工程学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (345, '香港', '香港大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (346, '香港', '香港中文大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (347, '香港', '香港科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (348, '香港', '香港理工大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (349, '香港', '香港城市大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (350, '香港', '香港浸会大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (351, '香港', '岭南大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (352, '香港', '香港教育大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (353, '澳门', '澳门大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (354, '澳门', '澳门科技大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (355, '澳门', '澳门理工学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (356, '澳门', '澳门旅游学院', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (357, '台湾', '台湾大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (358, '台湾', '清华大学（台湾）', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (359, '台湾', '交通大学（台湾）', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (360, '台湾', '成功大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (361, '台湾', '政治大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (362, '台湾', '阳明交通大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (363, '台湾', '中央大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (364, '台湾', '中山大学（台湾）', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (365, '台湾', '中兴大学', 1, '2026-04-08 23:40:43', NULL);
INSERT INTO `schools` (`id`, `province`, `name`, `has_master`, `created_at`, `updated_at`) VALUES (366, '台湾', '中正大学', 1, '2026-04-08 23:40:43', NULL);
COMMIT;

-- ----------------------------
-- Table structure for system_config
-- ----------------------------
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `config_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置键',
  `config_value` text COLLATE utf8mb4_unicode_ci COMMENT '配置值',
  `config_type` tinyint DEFAULT '0' COMMENT '配置类型: 0-字符串, 1-数字, 2-布尔值, 3-JSON',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '配置描述',
  `is_system` tinyint DEFAULT '0' COMMENT '是否系统配置: 1-是, 0-否',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1-启用, 0-禁用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- ----------------------------
-- Records of system_config
-- ----------------------------
BEGIN;
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (1, 'crawler_interval', '10', 1, '爬虫默认抓取间隔(分钟)', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (2, 'max_concurrent_crawlers', '5', 1, '最大并发爬虫数', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (3, 'push_enabled', '1', 2, '是否启用推送功能', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (4, 'trial_days', '3', 1, '免费试用天数', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (5, 'wechat_app_id', '', 0, '微信公众号AppID', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (6, 'wechat_app_secret', '', 0, '微信公众号AppSecret', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (7, 'alipay_app_id', '', 0, '支付宝AppID', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (8, 'alipay_private_key', '', 0, '支付宝私钥', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
COMMIT;

-- ----------------------------
-- Table structure for user_crawler_configs
-- ----------------------------
DROP TABLE IF EXISTS `user_crawler_configs`;
CREATE TABLE `user_crawler_configs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `crawler_type` tinyint NOT NULL COMMENT '爬虫类型: 1=考研, 2=考公',
  `crawler_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '爬虫名称',
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
  `keyword` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关键词',
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
  `error_message` text COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
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
  `keyword` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关键词',
  `category` tinyint NOT NULL COMMENT '分类: 1-考研, 2-考公',
  `is_active` tinyint DEFAULT '1' COMMENT '是否启用: 1-是, 0-否',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_keyword` (`user_id`,`keyword`,`category`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户关键词表';

-- ----------------------------
-- Records of user_keywords
-- ----------------------------
BEGIN;
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (109, 44, '计算机软件', 1, 1, '2026-04-12 22:17:47', '2026-04-12 22:17:47');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (112, 43, '软件', 1, 1, '2026-04-12 23:25:31', '2026-04-12 23:25:31');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (113, 43, '计算机', 2, 1, '2026-04-12 23:25:31', '2026-04-12 23:25:31');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户已读信息表';

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
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户订阅配置表';

-- ----------------------------
-- Records of user_subscriptions
-- ----------------------------
BEGIN;
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (42, 43, 3, 1, '{\"kaoyan\": {\"types\": [\"考试大纲\", \"成绩查询\"], \"majors\": \"软件\", \"schools\": \"西南石油\", \"keywords\": \"软件\", \"provinces\": [\"四川\"], \"study_type\": [], \"degree_type\": []}, \"kaogong\": {\"majors\": \"软件工程\", \"keywords\": [\"计算机\", \"计算机\"], \"education\": \"硕士\", \"provinces\": [\"北京\"], \"is_unlimited\": null, \"position_types\": [\"事业单位\"], \"is_fresh_graduate\": \"不限\"}}', '2026-04-12 19:11:56', '2026-04-12 23:25:31');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (43, 44, 2, 1, '{\"kaoyan\": {\"types\": [\"录取通知\", \"复试通知\"], \"majors\": \"器械工程\", \"schools\": \"东华\", \"keywords\": [\"计算机软件\"], \"provinces\": [\"上海\"], \"study_type\": [], \"degree_type\": []}, \"kaogong\": {\"majors\": [], \"education\": [\"不限\"], \"provinces\": [], \"is_unlimited\": null, \"position_types\": [], \"is_fresh_graduate\": \"不限\"}}', '2026-04-12 21:35:54', '2026-04-12 22:19:28');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像URL',
  `real_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `id_card` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '身份证号',
  `gender` tinyint DEFAULT '0' COMMENT '性别: 0-未知, 1-男, 2-女',
  `birthdate` date DEFAULT NULL COMMENT '出生日期',
  `register_ip` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '注册IP',
  `last_login_ip` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`) VALUES (1, 'admin', 'admin@shuangsai.com', '13800138000', '123456789', NULL, '系统管理员', NULL, 0, NULL, NULL, '127.0.0.1', '2026-04-12 19:10:43', 1, 1, 0, NULL, NULL, 0, 0, '2026-04-08 20:28:14', '2026-04-12 19:10:43');
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`) VALUES (43, '惠yang', 'chongyanghui123@gmail.com', '18109271097', '123456a', NULL, '惠重阳', NULL, 1, '2026-04-15', '127.0.0.1', NULL, NULL, 1, 0, 0, NULL, NULL, 0, 1, '2026-04-12 19:11:56', '2026-04-12 22:19:38');
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`) VALUES (44, '惠重阳', 'chongyanghui12@gmail.com', '18109271096', '123456a', NULL, '惠重阳', NULL, 1, '2026-04-15', '127.0.0.1', NULL, NULL, 1, 0, 0, NULL, NULL, 0, 1, '2026-04-12 21:35:54', '2026-04-12 21:35:54');
COMMIT;

-- ----------------------------
-- View structure for order_statistics_view
-- ----------------------------
DROP VIEW IF EXISTS `order_statistics_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `order_statistics_view` AS select cast(`orders`.`created_at` as date) AS `date`,count(0) AS `total_orders`,sum(`orders`.`total_amount`) AS `total_amount`,count((case when (`orders`.`payment_status` = 1) then 1 end)) AS `paid_orders`,sum((case when (`orders`.`payment_status` = 1) then `orders`.`total_amount` else 0 end)) AS `paid_amount`,sum((case when (`orders`.`payment_status` = 3) then `orders`.`total_amount` else 0 end)) AS `refund_amount` from `orders` group by cast(`orders`.`created_at` as date);

-- ----------------------------
-- View structure for user_subscription_view
-- ----------------------------
DROP VIEW IF EXISTS `user_subscription_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `user_subscription_view` AS select `u`.`id` AS `user_id`,`u`.`username` AS `username`,`u`.`email` AS `email`,`u`.`phone` AS `phone`,`u`.`vip_type` AS `vip_type`,`u`.`vip_start_time` AS `vip_start_time`,`u`.`vip_end_time` AS `vip_end_time`,`u`.`trial_status` AS `trial_status`,`u`.`trial_start_time` AS `trial_start_time`,`u`.`trial_end_time` AS `trial_end_time`,`us`.`subscribe_type` AS `subscribe_type`,`us`.`status` AS `subscribe_status`,`us`.`config_json` AS `config_json` from (`users` `u` left join `user_subscriptions` `us` on((`u`.`id` = `us`.`user_id`)));

-- ----------------------------
-- Procedure structure for check_vip_status
-- ----------------------------
DROP PROCEDURE IF EXISTS `check_vip_status`;
delimiter ;;
CREATE PROCEDURE `check_vip_status`()
BEGIN
    UPDATE `users` 
    SET `is_vip` = CASE 
        WHEN `vip_end_time` > NOW() THEN 1 
        ELSE 0 
    END;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for send_vip_expiration_reminders
-- ----------------------------
DROP PROCEDURE IF EXISTS `send_vip_expiration_reminders`;
delimiter ;;
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
END
;;
delimiter ;

-- ----------------------------
-- Event structure for check_vip_status_daily
-- ----------------------------
DROP EVENT IF EXISTS `check_vip_status_daily`;
delimiter ;;
CREATE EVENT `check_vip_status_daily`
ON SCHEDULE
EVERY '1' DAY STARTS '2026-04-08 00:00:00'
ON COMPLETION PRESERVE
DO CALL `check_vip_status`()
;;
delimiter ;

-- ----------------------------
-- Event structure for send_vip_expiration_reminders_daily
-- ----------------------------
DROP EVENT IF EXISTS `send_vip_expiration_reminders_daily`;
delimiter ;;
CREATE EVENT `send_vip_expiration_reminders_daily`
ON SCHEDULE
EVERY '1' DAY STARTS '2026-04-08 09:00:00'
ON COMPLETION PRESERVE
DO CALL `send_vip_expiration_reminders`()
;;
delimiter ;

-- ----------------------------
-- Event structure for statistic_crawler_data_hourly
-- ----------------------------
DROP EVENT IF EXISTS `statistic_crawler_data_hourly`;
delimiter ;;
CREATE EVENT `statistic_crawler_data_hourly`
ON SCHEDULE
EVERY '1' HOUR STARTS '2026-04-08 00:00:00'
ON COMPLETION PRESERVE
DO BEGIN
        -- 这里可以添加爬虫数据统计逻辑
    END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
