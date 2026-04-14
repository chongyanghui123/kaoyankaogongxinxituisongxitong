/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 90600 (9.6.0)
 Source Host           : localhost:3306
 Source Schema         : kaoyan_db

 Target Server Type    : MySQL
 Target Server Version : 90600 (9.6.0)
 File Encoding         : 65001

 Date: 12/04/2026 23:29:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for kaoyan_crawler_config
-- ----------------------------
DROP TABLE IF EXISTS `kaoyan_crawler_config`;
CREATE TABLE `kaoyan_crawler_config` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置名称',
  `url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '监控网址',
  `selector` text COLLATE utf8mb4_unicode_ci COMMENT '页面选择器',
  `parse_rules` json DEFAULT NULL COMMENT '解析规则',
  `interval` int DEFAULT '10' COMMENT '抓取间隔(分钟)',
  `status` tinyint DEFAULT '1' COMMENT '状态: 1-启用, 0-禁用',
  `priority` tinyint DEFAULT '0' COMMENT '优先级: 0-普通, 1-高, 2-非常高',
  `user_id` int DEFAULT NULL COMMENT '用户ID',
  `last_crawl_time` datetime DEFAULT NULL COMMENT '最后抓取时间',
  `next_crawl_time` datetime DEFAULT NULL COMMENT '下次抓取时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_url` (`url`),
  KEY `idx_status` (`status`),
  KEY `idx_priority` (`priority`)
) ENGINE=InnoDB AUTO_INCREMENT=532 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研爬虫配置表';

-- ----------------------------
-- Records of kaoyan_crawler_config
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for kaoyan_crawler_logs
-- ----------------------------
DROP TABLE IF EXISTS `kaoyan_crawler_logs`;
CREATE TABLE `kaoyan_crawler_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `config_id` bigint unsigned NOT NULL COMMENT '配置ID',
  `url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '抓取网址',
  `status` tinyint NOT NULL COMMENT '状态: 1-成功, 0-失败',
  `info_count` int DEFAULT '0' COMMENT '抓取信息数量',
  `error_msg` text COLLATE utf8mb4_unicode_ci COMMENT '错误信息',
  `crawl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '抓取时间',
  PRIMARY KEY (`id`),
  KEY `idx_config_id` (`config_id`),
  KEY `idx_status` (`status`),
  KEY `idx_crawl_time` (`crawl_time`)
) ENGINE=InnoDB AUTO_INCREMENT=509 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研爬虫日志表';

-- ----------------------------
-- Records of kaoyan_crawler_logs
-- ----------------------------
BEGIN;
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (1, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:54:24');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (2, 2, 'https://www.neea.edu.cn/', 1, 0, NULL, '2026-04-08 22:54:27');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (3, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:54:34');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (4, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:54:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (5, 2, 'https://www.neea.edu.cn/', 1, 0, NULL, '2026-04-08 22:54:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (6, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:54:54');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (7, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:55:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (8, 2, 'https://www.neea.edu.cn/', 1, 0, NULL, '2026-04-08 22:55:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (9, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:55:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (10, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:55:40');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (11, 2, 'https://www.neea.edu.cn/', 1, 0, NULL, '2026-04-08 22:55:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (12, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:55:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (13, 2, 'https://www.neea.edu.cn/', 1, 0, NULL, '2026-04-08 22:56:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (14, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:56:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (15, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:56:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (16, 2, 'https://www.neea.edu.cn/', 1, 0, NULL, '2026-04-08 22:56:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (17, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:56:20');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (18, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:56:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (19, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:56:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (20, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:56:54');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (21, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:57:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (22, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:57:14');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (23, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:57:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (24, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:57:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (25, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:57:44');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (26, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:57:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (27, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:58:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (28, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:58:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (29, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:58:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (30, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:58:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (31, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:58:44');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (32, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:58:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (33, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:59:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (34, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:59:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (35, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:59:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (36, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:59:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (37, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:59:44');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (38, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 22:59:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (39, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:00:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (40, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:00:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (41, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:00:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (42, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:00:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (43, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:00:44');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (44, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:00:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (45, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:01:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (46, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:01:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (47, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:01:28');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (48, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:01:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (49, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:01:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (50, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:02:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (51, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:02:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (52, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:02:29');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (53, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:02:39');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (54, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:02:49');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (55, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:02:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (56, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:03:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (57, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:03:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (58, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:03:28');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (59, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:03:38');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (60, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:03:48');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (61, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:03:58');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (62, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:04:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (63, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:04:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (64, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:04:29');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (65, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:04:38');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (66, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:04:49');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (67, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:04:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (68, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:05:08');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (69, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:05:18');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (70, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:05:29');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (71, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:05:39');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (72, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:05:49');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (73, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:05:58');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (74, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:06:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (75, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:06:18');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (76, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:06:29');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (77, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:06:39');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (78, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:06:50');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (79, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:06:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (80, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:07:08');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (81, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:07:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (82, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:07:29');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (83, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:07:38');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (84, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:07:49');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (85, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:07:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (86, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:08:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (87, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:08:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (88, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:08:28');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (89, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:08:38');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (90, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:08:57');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (91, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:09:07');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (92, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:09:18');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (93, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:09:27');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (94, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:09:37');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (95, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:09:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (96, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:10:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (97, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:10:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (98, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:10:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (99, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:10:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (100, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:10:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (101, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:10:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (102, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:11:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (103, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:11:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (104, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:11:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (105, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:11:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (106, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:11:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (107, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:11:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (108, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:12:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (109, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:12:17');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (110, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:12:27');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (111, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:12:37');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (112, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:12:47');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (113, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:12:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (114, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:13:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (115, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:13:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (116, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:13:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (117, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:13:37');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (118, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:13:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (119, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:13:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (120, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:14:07');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (121, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:14:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (122, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:14:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (123, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:14:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (124, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:14:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (125, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:14:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (126, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:15:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (127, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:15:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (128, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:15:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (129, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:15:37');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (130, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:15:54');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (131, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:16:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (132, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:16:14');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (133, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:16:24');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (134, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:16:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (135, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:16:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (136, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:16:54');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (137, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:17:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (138, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:17:14');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (139, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:17:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (140, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:17:34');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (141, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:17:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (142, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:17:54');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (143, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:18:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (144, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:18:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (145, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:18:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (146, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:18:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (147, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:19:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (148, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:19:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (149, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:19:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (150, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:19:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (151, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:19:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (152, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:20:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (153, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:20:20');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (154, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:20:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (155, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:20:40');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (156, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:20:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (157, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (158, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (159, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (160, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (161, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:30');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (162, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (163, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (164, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (165, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (166, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:21:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (167, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (168, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (169, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (170, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (171, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:20');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (172, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (173, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:30');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (174, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (175, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (176, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (177, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:50');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (178, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:22:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (179, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (180, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (181, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (182, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (183, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:20');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (184, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (185, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:30');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (186, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (187, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (188, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:23:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (189, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (190, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (191, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (192, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (193, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (194, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (195, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:24:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (196, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:25:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (197, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:25:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (198, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:25:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (199, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:25:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (200, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:25:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (201, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:25:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (202, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:26:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (203, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:26:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (204, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:26:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (205, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:26:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (206, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:26:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (207, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:26:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (208, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:27:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (209, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:27:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (210, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:27:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (211, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:27:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (212, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:27:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (213, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:27:56');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (214, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:28:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (215, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:28:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (216, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:28:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (217, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:28:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (218, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:28:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (219, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:28:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (220, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:29:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (221, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:29:16');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (222, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:29:26');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (223, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:29:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (224, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:29:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (225, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:29:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (226, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:30:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (227, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:30:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (228, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:30:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (229, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:30:36');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (230, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:30:46');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (231, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:30:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (232, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:31:06');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (233, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:31:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (234, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:31:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (235, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:31:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (236, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:32:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (237, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:32:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (238, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:32:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (239, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:32:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (240, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:32:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (241, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:32:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (242, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:33:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (243, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:33:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (244, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:33:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (245, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:33:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (246, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:33:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (247, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:34:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (248, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:34:10');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (249, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:34:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (250, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:34:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (251, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:34:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (252, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:34:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (253, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:35:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (254, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:35:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (255, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:35:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (256, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:35:57');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (257, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:36:07');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (258, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:36:17');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (259, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:36:57');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (260, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:37:10');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (261, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:41:48');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (262, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:41:57');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (263, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:42:08');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (264, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:42:34');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (265, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:42:44');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (266, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:42:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (267, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:43:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (268, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:43:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (269, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:43:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (270, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:43:34');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (271, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:43:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (272, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:43:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (273, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:44:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (274, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:44:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (275, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:44:24');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (276, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:44:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (277, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:44:44');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (278, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:44:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (279, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:45:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (280, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:45:34');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (281, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:45:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (282, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:45:54');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (283, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:46:14');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (284, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:46:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (285, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:46:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (286, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:46:49');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (287, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:47:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (288, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:47:09');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (289, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:47:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (290, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:47:29');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (291, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:47:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (292, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:48:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (293, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:48:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (294, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:48:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (295, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:48:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (296, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:48:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (297, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:48:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (298, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:49:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (299, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:49:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (300, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:49:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (301, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:49:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (302, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:49:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (303, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:49:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (304, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:50:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (305, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:50:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (306, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:50:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (307, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:50:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (308, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:50:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (309, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:50:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (310, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:51:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (311, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:51:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (312, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:51:25');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (313, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:51:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (314, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:51:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (315, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:51:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (316, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:52:04');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (317, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:52:14');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (318, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:52:24');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (319, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:52:35');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (320, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:52:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (321, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:52:55');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (322, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:53:05');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (323, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:53:37');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (324, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:53:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (325, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:54:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (326, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:54:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (327, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:54:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (328, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:54:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (329, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:54:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (330, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:54:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (331, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:55:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (332, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:55:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (333, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:55:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (334, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:55:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (335, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:55:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (336, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:55:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (337, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:56:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (338, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:56:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (339, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:56:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (340, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:56:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (341, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:56:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (342, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:56:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (343, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:57:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (344, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:57:14');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (345, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:57:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (346, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:57:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (347, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:57:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (348, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:57:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (349, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:58:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (350, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:58:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (351, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:58:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (352, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:58:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (353, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:58:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (354, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:58:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (355, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:59:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (356, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:59:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (357, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:59:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (358, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:59:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (359, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:59:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (360, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-08 23:59:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (361, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:00:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (362, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:00:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (363, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:00:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (364, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:00:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (365, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:00:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (366, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:00:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (367, 2, 'https://www.neea.edu.cn/', 0, 0, '\'publish_date\' is an invalid keyword argument for KaoyanInfo', '2026-04-09 00:01:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (368, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:01:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (369, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:01:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (370, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:01:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (371, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:01:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (372, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:01:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (373, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:01:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (374, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:02:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (375, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:02:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (376, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:02:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (377, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:02:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (378, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:02:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (379, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:02:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (380, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:03:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (381, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:03:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (382, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:03:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (383, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:03:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (384, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:03:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (385, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:03:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (386, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:04:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (387, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:04:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (388, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:04:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (389, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:04:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (390, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:04:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (391, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:04:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (392, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:05:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (393, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:05:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (394, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:05:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (395, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:05:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (396, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:05:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (397, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:05:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (398, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:06:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (399, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:06:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (400, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:06:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (401, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:06:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (402, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:06:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (403, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:06:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (404, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:07:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (405, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:07:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (406, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:07:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (407, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:07:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (408, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:07:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (409, 2, 'https://www.neea.edu.cn/', 0, 0, '\'publish_date\' is an invalid keyword argument for KaoyanInfo', '2026-04-09 00:07:45');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (410, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:07:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (411, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:08:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (412, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:08:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (413, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:08:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (414, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:08:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (415, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:08:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (416, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:08:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (417, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:09:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (418, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:09:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (419, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:09:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (420, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:09:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (421, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:09:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (422, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:09:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (423, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:10:03');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (424, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:10:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (425, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:10:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (426, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:10:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (427, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:10:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (428, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:10:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (429, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:11:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (430, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:11:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (431, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:11:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (432, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:11:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (433, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:11:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (434, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:11:53');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (435, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:12:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (436, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:12:13');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (437, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:12:23');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (438, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:12:33');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (439, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:12:43');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (440, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:13:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (441, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:13:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (442, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:14:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (443, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:14:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (444, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:14:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (445, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:14:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (446, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:14:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (447, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:14:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (448, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:15:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (449, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:15:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (450, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:15:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (451, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:15:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (452, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:15:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (453, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:15:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (454, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:16:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (455, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:16:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (456, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:16:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (457, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:16:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (458, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:16:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (459, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:16:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (460, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:17:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (461, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:17:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (462, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:17:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (463, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:17:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (464, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:17:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (465, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:17:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (466, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:18:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (467, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:18:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (468, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:18:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (469, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:18:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (470, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:18:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (471, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:18:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (472, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:19:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (473, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:19:11');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (474, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:19:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (475, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:19:31');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (476, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:19:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (477, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:19:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (478, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:20:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (479, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:20:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (480, 2, 'https://www.neea.edu.cn/', 0, 0, '\'publish_date\' is an invalid keyword argument for KaoyanInfo', '2026-04-09 00:20:19');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (481, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:20:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (482, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:20:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (483, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:20:41');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (484, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:20:52');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (485, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:21:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (486, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:21:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (487, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:21:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (488, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:21:32');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (489, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:21:42');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (490, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:21:51');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (491, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:22:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (492, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:22:12');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (493, 1, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:22:22');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (494, 12, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 00:36:02');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (495, 194, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 01:06:15');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (496, 454, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 11:55:21');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (497, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:13:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (498, 475, 'https://yz.chsi.com.cn/sch/北京大学', 1, 0, NULL, '2026-04-09 18:17:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (499, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:18:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (500, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:23:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (501, 476, 'https://yz.chsi.com.cn/zyk/?major=1&school=北京大学', 1, 0, NULL, '2026-04-09 18:23:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (502, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:28:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (503, 475, 'https://yz.chsi.com.cn/sch/北京大学', 1, 0, NULL, '2026-04-09 18:28:01');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (504, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:33:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (505, 476, 'https://yz.chsi.com.cn/zyk/?major=1&school=北京大学', 1, 0, NULL, '2026-04-09 18:37:59');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (506, 475, 'https://yz.chsi.com.cn/sch/北京大学', 1, 0, NULL, '2026-04-09 18:38:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (507, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:38:00');
INSERT INTO `kaoyan_crawler_logs` (`id`, `config_id`, `url`, `status`, `info_count`, `error_msg`, `crawl_time`) VALUES (508, 474, 'https://yz.chsi.com.cn/', 1, 0, NULL, '2026-04-09 18:43:01');
COMMIT;

-- ----------------------------
-- Table structure for kaoyan_info
-- ----------------------------
DROP TABLE IF EXISTS `kaoyan_info`;
CREATE TABLE `kaoyan_info` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '信息ID',
  `title` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标题',
  `source` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '来源',
  `source_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '来源链接',
  `publish_time` datetime NOT NULL COMMENT '发布时间',
  `content` longtext COLLATE utf8mb4_unicode_ci COMMENT '内容',
  `url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '原文链接',
  `tags` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标签(逗号分隔)',
  `urgency_level` tinyint DEFAULT '0' COMMENT '紧急度: 0-普通, 1-重要, 2-紧急, 3-非常紧急',
  `category` tinyint DEFAULT '0' COMMENT '分类: 0-普通通知, 1-调剂, 2-扩招, 3-复试线, 4-招生简章, 5-时间节点',
  `province` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '省份',
  `school` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '院校',
  `major` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '专业',
  `degree_type` tinyint DEFAULT NULL COMMENT '学位类型: 1-学硕, 2-专硕',
  `study_type` tinyint DEFAULT NULL COMMENT '学习方式: 1-全日制, 2-非全日制',
  `is_valid` tinyint DEFAULT '1' COMMENT '是否有效: 1-有效, 0-无效',
  `is_top` tinyint DEFAULT '0' COMMENT '是否置顶: 1-是, 0-否',
  `is_excellent` tinyint DEFAULT '0' COMMENT '是否加精: 1-是, 0-否',
  `view_count` int DEFAULT '0' COMMENT '浏览次数',
  `like_count` int DEFAULT '0' COMMENT '点赞次数',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_url` (`url`),
  KEY `idx_publish_time` (`publish_time`),
  KEY `idx_category` (`category`),
  KEY `idx_urgency_level` (`urgency_level`),
  KEY `idx_province` (`province`),
  KEY `idx_school` (`school`),
  KEY `idx_major` (`major`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研信息表';

-- ----------------------------
-- Records of kaoyan_info
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
