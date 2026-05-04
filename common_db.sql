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

 Date: 04/05/2026 19:39:28
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
-- Table structure for carousels
-- ----------------------------
DROP TABLE IF EXISTS `carousels`;
CREATE TABLE `carousels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '轮播图标题',
  `subtitle` varchar(500) DEFAULT NULL COMMENT '轮播图副标题',
  `image_url` varchar(500) DEFAULT NULL COMMENT '轮播图图片URL',
  `link_url` varchar(500) DEFAULT NULL COMMENT '跳转链接URL',
  `sort_order` int DEFAULT NULL COMMENT '排序顺序',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_carousels_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of carousels
-- ----------------------------
BEGIN;
INSERT INTO `carousels` (`id`, `title`, `subtitle`, `image_url`, `link_url`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (1, '考研备考攻略', '2026年考研全程备考指南', '/uploads/carousels/carousel_20260427180549.jpg', '/kaoyan-guides', 1, 1, '2026-04-26 17:46:38', '2026-04-27 18:05:50');
INSERT INTO `carousels` (`id`, `title`, `subtitle`, `image_url`, `link_url`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (2, '公务员考试技巧', '公务员考试高分答题技巧', '/uploads/carousels/carousel_20260426225045.jpg', '/gongwuyuan-tips', 2, 1, '2026-04-26 17:46:38', '2026-04-27 11:50:28');
INSERT INTO `carousels` (`id`, `title`, `subtitle`, `image_url`, `link_url`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES (3, 'VIP会员权益', '开通VIP享受更多权益', '/uploads/carousels/carousel_20260426225050.jpg', '/vip-plans', 3, 1, '2026-04-26 17:46:38', '2026-04-27 11:50:48');
COMMIT;

-- ----------------------------
-- Table structure for community_answer_comments
-- ----------------------------
DROP TABLE IF EXISTS `community_answer_comments`;
CREATE TABLE `community_answer_comments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `answer_id` int NOT NULL COMMENT '回答ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `content` text NOT NULL COMMENT '评论内容',
  `parent_id` int DEFAULT NULL COMMENT '父评论ID，用于回复',
  `like_count` int DEFAULT NULL COMMENT '点赞数',
  `status` int DEFAULT NULL COMMENT '状态: 1-活跃, 0-已删除',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_answer_comments
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for community_answers
-- ----------------------------
DROP TABLE IF EXISTS `community_answers`;
CREATE TABLE `community_answers` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '回答ID',
  `question_id` int NOT NULL COMMENT '问题ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `content` text NOT NULL COMMENT '回答内容',
  `image_urls` varchar(500) DEFAULT NULL COMMENT '图片URL，逗号分隔',
  `like_count` int DEFAULT NULL COMMENT '点赞数',
  `is_accepted` tinyint(1) DEFAULT NULL COMMENT '是否被采纳',
  `status` int DEFAULT NULL COMMENT '状态: 1-活跃, 0-已删除',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_answers
-- ----------------------------
BEGIN;
INSERT INTO `community_answers` (`id`, `question_id`, `user_id`, `content`, `image_urls`, `like_count`, `is_accepted`, `status`, `created_at`, `updated_at`) VALUES (9, 1, 2, '数学一确实比较难，建议先打好基础，高数部分重点复习极限、积分、微分方程。', NULL, 0, NULL, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_answers` (`id`, `question_id`, `user_id`, `content`, `image_urls`, `like_count`, `is_accepted`, `status`, `created_at`, `updated_at`) VALUES (10, 1, 3, '真题很重要，建议至少做三遍，总结错题。', NULL, 0, NULL, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_answers` (`id`, `question_id`, `user_id`, `content`, `image_urls`, `like_count`, `is_accepted`, `status`, `created_at`, `updated_at`) VALUES (11, 2, 1, '申论要多写多练，注意结构清晰，论点明确。', NULL, 0, NULL, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_answers` (`id`, `question_id`, `user_id`, `content`, `image_urls`, `like_count`, `is_accepted`, `status`, `created_at`, `updated_at`) VALUES (12, 3, 4, '阅读技巧在于定位关键词，先看题目再读文章。', NULL, 0, NULL, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_answers` (`id`, `question_id`, `user_id`, `content`, `image_urls`, `like_count`, `is_accepted`, `status`, `created_at`, `updated_at`) VALUES (13, 4, 5, '政治选择题要关注时政热点，多做模拟题。', NULL, 0, NULL, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
COMMIT;

-- ----------------------------
-- Table structure for community_group_members
-- ----------------------------
DROP TABLE IF EXISTS `community_group_members`;
CREATE TABLE `community_group_members` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '成员ID',
  `group_id` int NOT NULL COMMENT '小组ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `role` int DEFAULT NULL COMMENT '角色: 0-普通成员, 1-管理员, 2-创建者',
  `status` int DEFAULT NULL COMMENT '状态: 1-已加入, 0-待审核, 2-已拒绝',
  `join_time` datetime DEFAULT NULL COMMENT '加入时间',
  `last_active_time` datetime DEFAULT NULL COMMENT '最后活跃时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_group_members
-- ----------------------------
BEGIN;
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (45, 19, 1, 2, 1, '2026-04-29 19:52:22', NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (46, 1, 1, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (47, 1, 2, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (48, 1, 3, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (49, 1, 4, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (50, 1, 5, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (51, 2, 1, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (52, 2, 2, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (53, 2, 3, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (54, 2, 4, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (55, 2, 5, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (56, 3, 1, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (57, 3, 2, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (58, 3, 3, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (59, 3, 4, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (60, 3, 5, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (61, 4, 1, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (62, 4, 2, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (63, 4, 3, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (64, 4, 4, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (65, 4, 5, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (66, 5, 1, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (67, 5, 2, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (68, 5, 3, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (69, 5, 4, NULL, 1, NULL, NULL);
INSERT INTO `community_group_members` (`id`, `group_id`, `user_id`, `role`, `status`, `join_time`, `last_active_time`) VALUES (70, 5, 5, NULL, 1, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for community_group_messages
-- ----------------------------
DROP TABLE IF EXISTS `community_group_messages`;
CREATE TABLE `community_group_messages` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '消息ID',
  `group_id` int NOT NULL COMMENT '小组ID',
  `user_id` int NOT NULL COMMENT '发送者ID',
  `message_type` int DEFAULT NULL COMMENT '消息类型: 1-文字, 2-图片, 3-系统消息',
  `content` text COMMENT '消息内容',
  `image_url` varchar(255) DEFAULT NULL COMMENT '图片URL',
  `status` int DEFAULT NULL COMMENT '状态: 1-正常, 0-已撤回',
  `created_at` datetime DEFAULT NULL COMMENT '发送时间',
  `mentioned_users` varchar(500) DEFAULT NULL COMMENT '被@的用户ID列表，逗号分隔',
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `community_group_messages_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `community_groups` (`id`),
  CONSTRAINT `community_group_messages_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_group_messages
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for community_group_post_comments
-- ----------------------------
DROP TABLE IF EXISTS `community_group_post_comments`;
CREATE TABLE `community_group_post_comments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `post_id` int NOT NULL COMMENT '帖子ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `content` text NOT NULL COMMENT '评论内容',
  `parent_id` int DEFAULT NULL COMMENT '父评论ID，用于回复',
  `like_count` int DEFAULT NULL COMMENT '点赞数',
  `status` int DEFAULT NULL COMMENT '状态: 1-活跃, 0-已删除',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_group_post_comments
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for community_group_posts
-- ----------------------------
DROP TABLE IF EXISTS `community_group_posts`;
CREATE TABLE `community_group_posts` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
  `group_id` int NOT NULL COMMENT '小组ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `title` varchar(200) NOT NULL COMMENT '帖子标题',
  `content` text NOT NULL COMMENT '帖子内容',
  `image_urls` varchar(500) DEFAULT NULL COMMENT '图片URL，逗号分隔',
  `view_count` int DEFAULT NULL COMMENT '浏览量',
  `comment_count` int DEFAULT NULL COMMENT '评论数',
  `like_count` int DEFAULT NULL COMMENT '点赞数',
  `status` int DEFAULT NULL COMMENT '状态: 1-活跃, 0-已删除',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_group_posts
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for community_groups
-- ----------------------------
DROP TABLE IF EXISTS `community_groups`;
CREATE TABLE `community_groups` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '小组ID',
  `name` varchar(100) NOT NULL COMMENT '小组名称',
  `description` text COMMENT '小组描述',
  `avatar` varchar(255) DEFAULT NULL COMMENT '小组头像URL',
  `cover` varchar(255) DEFAULT NULL COMMENT '小组封面URL',
  `creator_id` int NOT NULL COMMENT '创建者ID',
  `status` int DEFAULT NULL COMMENT '状态: 1-活跃, 0-不活跃',
  `member_count` int DEFAULT NULL COMMENT '成员数量',
  `join_type` int DEFAULT NULL COMMENT '加入类型: 1-自由加入, 2-审核加入, 3-邀请加入',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签，逗号分隔',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_groups
-- ----------------------------
BEGIN;
INSERT INTO `community_groups` (`id`, `name`, `description`, `avatar`, `cover`, `creator_id`, `status`, `member_count`, `join_type`, `tags`, `created_at`, `updated_at`) VALUES (19, '测试学习小组', '这是一个测试小组', NULL, NULL, 1, 1, 1, 1, NULL, '2026-04-29 19:52:22', '2026-04-29 19:52:22');
INSERT INTO `community_groups` (`id`, `name`, `description`, `avatar`, `cover`, `creator_id`, `status`, `member_count`, `join_type`, `tags`, `created_at`, `updated_at`) VALUES (20, '考研数学交流群', '为考研数学学习者提供交流平台，分享学习心得和解题技巧', NULL, NULL, 1, 1, NULL, 0, NULL, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_groups` (`id`, `name`, `description`, `avatar`, `cover`, `creator_id`, `status`, `member_count`, `join_type`, `tags`, `created_at`, `updated_at`) VALUES (21, '公务员考试交流群', '公务员考试备考交流，分享真题解析和备考经验', NULL, NULL, 1, 1, NULL, 0, NULL, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_groups` (`id`, `name`, `description`, `avatar`, `cover`, `creator_id`, `status`, `member_count`, `join_type`, `tags`, `created_at`, `updated_at`) VALUES (22, '考研英语学习群', '英语学习交流，分享阅读、写作、翻译技巧', NULL, NULL, 1, 1, NULL, 0, NULL, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_groups` (`id`, `name`, `description`, `avatar`, `cover`, `creator_id`, `status`, `member_count`, `join_type`, `tags`, `created_at`, `updated_at`) VALUES (23, '考研政治学习群', '政治备考交流，分享时政热点和答题技巧', NULL, NULL, 1, 1, NULL, 0, NULL, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_groups` (`id`, `name`, `description`, `avatar`, `cover`, `creator_id`, `status`, `member_count`, `join_type`, `tags`, `created_at`, `updated_at`) VALUES (24, '公务员申论群', '申论写作技巧交流，分享范文和写作思路', NULL, NULL, 1, 1, NULL, 0, NULL, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
COMMIT;

-- ----------------------------
-- Table structure for community_likes
-- ----------------------------
DROP TABLE IF EXISTS `community_likes`;
CREATE TABLE `community_likes` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `target_type` int NOT NULL COMMENT '目标类型: 1-问题, 2-回答, 3-评论, 4-帖子',
  `target_id` int NOT NULL COMMENT '目标ID',
  `created_at` datetime DEFAULT NULL COMMENT '点赞时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_likes
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for community_questions
-- ----------------------------
DROP TABLE IF EXISTS `community_questions`;
CREATE TABLE `community_questions` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '问题ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `title` varchar(200) NOT NULL COMMENT '问题标题',
  `content` text NOT NULL COMMENT '问题内容',
  `image_urls` varchar(500) DEFAULT NULL COMMENT '图片URL，逗号分隔',
  `category` varchar(50) DEFAULT NULL COMMENT '分类',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签，逗号分隔',
  `view_count` int DEFAULT NULL COMMENT '浏览量',
  `answer_count` int DEFAULT NULL COMMENT '回答数',
  `like_count` int DEFAULT NULL COMMENT '点赞数',
  `status` int DEFAULT NULL COMMENT '状态: 1-开放, 0-关闭, 2-已解决',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_questions
-- ----------------------------
BEGIN;
INSERT INTO `community_questions` (`id`, `user_id`, `title`, `content`, `image_urls`, `category`, `tags`, `view_count`, `answer_count`, `like_count`, `status`, `created_at`, `updated_at`) VALUES (14, 1, '测试问题', '这是一个测试问题内容', NULL, '考研', NULL, 2, 0, 0, 1, '2026-04-29 19:53:42', '2026-04-29 20:23:06');
INSERT INTO `community_questions` (`id`, `user_id`, `title`, `content`, `image_urls`, `category`, `tags`, `view_count`, `answer_count`, `like_count`, `status`, `created_at`, `updated_at`) VALUES (15, 1, '2026年考研数学一的难度如何？有什么备考建议吗？', '最近开始准备2026年考研，想了解一下数学一的难度和备考策略，希望有经验的学长学姐能分享一下。', NULL, '考研', NULL, 0, 0, 0, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_questions` (`id`, `user_id`, `title`, `content`, `image_urls`, `category`, `tags`, `view_count`, `answer_count`, `like_count`, `status`, `created_at`, `updated_at`) VALUES (16, 2, '公务员考试申论怎么提高？有什么答题技巧？', '申论一直是我的弱项，每次模拟考试分数都不高，想请教一下申论的答题技巧和备考方法。', NULL, '公务员', NULL, 0, 0, 0, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_questions` (`id`, `user_id`, `title`, `content`, `image_urls`, `category`, `tags`, `view_count`, `answer_count`, `like_count`, `status`, `created_at`, `updated_at`) VALUES (17, 3, '考研英语阅读怎么提高正确率？有什么解题技巧？', '英语阅读总是错很多，尤其是细节题和推理题，想了解一下提高阅读正确率的方法。', NULL, '英语', NULL, 0, 0, 0, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_questions` (`id`, `user_id`, `title`, `content`, `image_urls`, `category`, `tags`, `view_count`, `answer_count`, `like_count`, `status`, `created_at`, `updated_at`) VALUES (18, 4, '考研政治选择题怎么复习？有什么重点？', '政治选择题总是丢分，想知道怎么有效复习，重点在哪里。', NULL, '政治', NULL, 0, 0, 0, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
INSERT INTO `community_questions` (`id`, `user_id`, `title`, `content`, `image_urls`, `category`, `tags`, `view_count`, `answer_count`, `like_count`, `status`, `created_at`, `updated_at`) VALUES (19, 5, '公务员行测数量关系怎么提高？', '行测中的数量关系题总是做不完，有没有什么快速解题的技巧？', NULL, '公务员', NULL, 0, 0, 0, 1, '2026-04-30 19:13:43', '2026-04-30 19:13:43');
COMMIT;

-- ----------------------------
-- Table structure for community_reports
-- ----------------------------
DROP TABLE IF EXISTS `community_reports`;
CREATE TABLE `community_reports` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '举报ID',
  `reporter_id` int NOT NULL COMMENT '举报者ID',
  `target_type` int NOT NULL COMMENT '目标类型: 1-问题, 2-回答, 3-评论, 4-帖子, 5-用户',
  `target_id` int NOT NULL COMMENT '目标ID',
  `reason` text NOT NULL COMMENT '举报原因',
  `status` int DEFAULT NULL COMMENT '处理状态: 0-待处理, 1-已处理, 2-已驳回',
  `handler_id` int DEFAULT NULL COMMENT '处理人ID',
  `handle_time` datetime DEFAULT NULL COMMENT '处理时间',
  `handle_note` text COMMENT '处理备注',
  `created_at` datetime DEFAULT NULL COMMENT '举报时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of community_reports
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for daily_practice_records
-- ----------------------------
DROP TABLE IF EXISTS `daily_practice_records`;
CREATE TABLE `daily_practice_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `practice_id` int NOT NULL COMMENT '题目ID',
  `user_answer` varchar(10) NOT NULL COMMENT '用户答案',
  `is_correct` tinyint(1) NOT NULL COMMENT '是否正确',
  `score` int DEFAULT NULL COMMENT '得分',
  `created_at` datetime DEFAULT NULL COMMENT '答题时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `practice_id` (`practice_id`),
  KEY `ix_daily_practice_records_id` (`id`),
  CONSTRAINT `daily_practice_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `daily_practice_records_ibfk_2` FOREIGN KEY (`practice_id`) REFERENCES `daily_practices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of daily_practice_records
-- ----------------------------
BEGIN;
INSERT INTO `daily_practice_records` (`id`, `user_id`, `practice_id`, `user_answer`, `is_correct`, `score`, `created_at`, `updated_at`) VALUES (7, 153, 4, 'C', 1, 10, '2026-04-30 17:33:02', '2026-04-30 17:33:02');
INSERT INTO `daily_practice_records` (`id`, `user_id`, `practice_id`, `user_answer`, `is_correct`, `score`, `created_at`, `updated_at`) VALUES (8, 153, 6, 'C', 0, 0, '2026-04-30 17:46:46', '2026-04-30 17:46:46');
COMMIT;

-- ----------------------------
-- Table structure for daily_practices
-- ----------------------------
DROP TABLE IF EXISTS `daily_practices`;
CREATE TABLE `daily_practices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(50) NOT NULL COMMENT '题目分类: 行测, 申论, 考研英语, 考研政治等',
  `question` text NOT NULL COMMENT '题目内容',
  `options` text NOT NULL COMMENT '选项JSON: [{"label":"A","text":"xxx"}]',
  `answer` varchar(10) NOT NULL COMMENT '正确答案: A/B/C/D',
  `analysis` text COMMENT '答案解析',
  `difficulty` int DEFAULT NULL COMMENT '难度: 1-简单, 2-中等, 3-困难',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `show_date` datetime DEFAULT NULL COMMENT '指定显示日期, 为空则随机',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_daily_practices_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of daily_practices
-- ----------------------------
BEGIN;
INSERT INTO `daily_practices` (`id`, `category`, `question`, `options`, `answer`, `analysis`, `difficulty`, `is_active`, `show_date`, `created_at`, `updated_at`) VALUES (4, '【行测】', '某单位采购办公用品，其中A4纸的数量是B5纸的2倍，B5纸比A3纸多50本。若A3纸有100本，则A4纸有多少本？', '[{\"label\":\"A\",\"text\":\"200本\"},{\"label\":\"B\",\"text\":\"250本\"},{\"label\":\"C\",\"text\":\"300本\"},{\"label\":\"D\",\"text\":\"350本\"}]', 'C', 'A3纸有100本，B5纸比A3纸多50本，所以B5纸有150本。A4纸是B5纸的2倍，所以A4纸有300本。', 2, 1, '2026-04-30 00:00:00', NULL, NULL);
INSERT INTO `daily_practices` (`id`, `category`, `question`, `options`, `answer`, `analysis`, `difficulty`, `is_active`, `show_date`, `created_at`, `updated_at`) VALUES (5, '【申论】', '下列关于我国乡村振兴战略的说法，不正确的是：', '[{\"label\":\"A\",\"text\":\"实施乡村振兴战略是党的十九大作出的重大决策部署\"},{\"label\":\"B\",\"text\":\"乡村振兴的战略目标是到2050年实现乡村全面振兴\"},{\"label\":\"C\",\"text\":\"产业兴旺是乡村振兴的首要任务\"},{\"label\":\"D\",\"text\":\"乡村振兴只需要发展农业经济即可\"}]', 'D', '乡村振兴不仅仅是发展农业经济，而是包括产业兴旺、生态宜居、乡风文明、治理有效、生活富裕五个方面的全面振兴。', 2, 1, '2026-05-01 00:00:00', NULL, NULL);
INSERT INTO `daily_practices` (`id`, `category`, `question`, `options`, `answer`, `analysis`, `difficulty`, `is_active`, `show_date`, `created_at`, `updated_at`) VALUES (6, '【考研政治】', '马克思主义哲学认为，世界的本原是：', '[{\"label\":\"A\",\"text\":\"物质\"},{\"label\":\"B\",\"text\":\"精神\"},{\"label\":\"C\",\"text\":\"物质和精神\"},{\"label\":\"D\",\"text\":\"不存在本原\"}]', 'A', '马克思主义哲学是唯物主义哲学，认为物质是世界的本原，精神是物质的产物和反映。', 1, 1, '2026-05-02 00:00:00', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for exam_schedules
-- ----------------------------
DROP TABLE IF EXISTS `exam_schedules`;
CREATE TABLE `exam_schedules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '考试名称',
  `exam_type` int NOT NULL COMMENT '考试类型: 1-考研, 2-考公',
  `exam_date` datetime NOT NULL COMMENT '考试日期',
  `description` text COMMENT '考试描述',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_exam_schedules_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of exam_schedules
-- ----------------------------
BEGIN;
INSERT INTO `exam_schedules` (`id`, `name`, `exam_type`, `exam_date`, `description`, `is_active`, `created_at`, `updated_at`) VALUES (5, '2026年教师资格证考试', 2, '2026-09-15 00:00:00', '全国中小学教师资格考试', 1, '2026-04-30 19:14:00', NULL);
INSERT INTO `exam_schedules` (`id`, `name`, `exam_type`, `exam_date`, `description`, `is_active`, `created_at`, `updated_at`) VALUES (6, '2026年国家公务员考试', 2, '2026-11-28 00:00:00', '国考公共科目笔试', 1, '2026-04-30 19:14:00', NULL);
INSERT INTO `exam_schedules` (`id`, `name`, `exam_type`, `exam_date`, `description`, `is_active`, `created_at`, `updated_at`) VALUES (7, '2026年考研初试', 1, '2026-12-20 00:00:00', '全国硕士研究生招生考试', 1, '2026-04-30 19:14:00', NULL);
INSERT INTO `exam_schedules` (`id`, `name`, `exam_type`, `exam_date`, `description`, `is_active`, `created_at`, `updated_at`) VALUES (8, '2027年省公务员考试', 2, '2027-03-15 00:00:00', '各省公务员考试', 1, '2026-04-30 19:14:00', NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of feedbacks
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for gift_exchanges
-- ----------------------------
DROP TABLE IF EXISTS `gift_exchanges`;
CREATE TABLE `gift_exchanges` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `gift_id` int NOT NULL,
  `points_used` int NOT NULL,
  `status` int DEFAULT '0',
  `tracking_number` varchar(100) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_gift_id` (`gift_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of gift_exchanges
-- ----------------------------
BEGIN;
INSERT INTO `gift_exchanges` (`id`, `user_id`, `gift_id`, `points_used`, `status`, `tracking_number`, `remark`, `created_at`, `updated_at`) VALUES (2, 153, 1, 10, 1, '', '', '2026-04-29 16:14:24', '2026-04-29 16:14:40');
COMMIT;

-- ----------------------------
-- Table structure for gifts
-- ----------------------------
DROP TABLE IF EXISTS `gifts`;
CREATE TABLE `gifts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `image_url` varchar(500) DEFAULT NULL,
  `points_required` int NOT NULL,
  `stock` int DEFAULT '0',
  `exchanged_count` int DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  `sort_order` int DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of gifts
-- ----------------------------
BEGIN;
INSERT INTO `gifts` (`id`, `name`, `description`, `image_url`, `points_required`, `stock`, `exchanged_count`, `is_active`, `sort_order`, `created_at`, `updated_at`) VALUES (1, '飞鼠', '飞鼠玩偶', '/uploads/gifts/1777209770_微信图片_2026-04-26_212223_875.jpg', 10, 99, 2, 1, 0, '2026-04-26 20:18:03', '2026-04-29 16:14:24');
COMMIT;

-- ----------------------------
-- Table structure for hot_topics
-- ----------------------------
DROP TABLE IF EXISTS `hot_topics`;
CREATE TABLE `hot_topics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL COMMENT '热点标题',
  `content` text COMMENT '热点内容',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图片URL',
  `link_url` varchar(500) DEFAULT NULL COMMENT '跳转链接URL',
  `category` varchar(50) DEFAULT NULL COMMENT '分类: 考研/考公/通用',
  `source` varchar(100) DEFAULT NULL COMMENT '来源',
  `views` int DEFAULT NULL COMMENT '浏览量',
  `sort_order` int DEFAULT NULL COMMENT '排序顺序，数字越大越靠前',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '是否启用',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_hot_topics_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of hot_topics
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
  `is_vip` tinyint(1) DEFAULT '0',
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
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`, `is_vip`) VALUES (1, '考公测试资料', '考公测试资料', 2, 7, '测试', 'uploads/361be862-13ab-49a5-89f1-d467da3f3262.txt', '/uploads/361be862-13ab-49a5-89f1-d467da3f3262.txt', 49, '.txt', '/uploads/f2129d8b-2eed-4286-9877-058287198d50.png', 1, '2026-04-22 13:50:32', 2, 0, 1, '2026-04-22 13:50:32', '2026-04-29 19:59:03', 0);
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`, `is_vip`) VALUES (2, '考公测试资料', '考公测试资料', 2, 7, '测试', 'uploads/d809c2c6-df9c-43f3-a34f-d6067bbcd1ec.txt', '/uploads/d809c2c6-df9c-43f3-a34f-d6067bbcd1ec.txt', 49, '.txt', '/uploads/1885a9ca-591e-4e09-bf03-46ace29a71eb.png', 1, '2026-04-22 13:54:37', 0, 0, 1, '2026-04-22 13:54:37', '2026-04-22 13:54:37', 0);
INSERT INTO `learning_materials` (`id`, `title`, `description`, `type`, `category_id`, `subject`, `file_path`, `file_url`, `file_size`, `file_extension`, `cover_image`, `uploader_id`, `upload_time`, `download_count`, `rating`, `is_valid`, `created_at`, `updated_at`, `is_vip`) VALUES (3, '考研测试资料', '考研测试资料', 1, 1, '111', 'uploads/b3f710bd-81f1-4a06-af90-788b32c22c7c.txt', '/uploads/b3f710bd-81f1-4a06-af90-788b32c22c7c.txt', 49, '.txt', '/uploads/421ab4ef-55bc-41e9-90e3-75ec013389c6.jpg', 1, '2026-04-22 13:55:55', 0, 0, 1, '2026-04-22 13:55:55', '2026-04-24 17:47:48', 0);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_comments
-- ----------------------------
BEGIN;
INSERT INTO `material_comments` (`id`, `user_id`, `material_id`, `parent_comment_id`, `comment`, `created_at`, `updated_at`) VALUES (6, 1, 3, NULL, '这是一条测试评论，用于检查显示问题', '2026-04-29 20:01:41', '2026-04-29 20:01:41');
INSERT INTO `material_comments` (`id`, `user_id`, `material_id`, `parent_comment_id`, `comment`, `created_at`, `updated_at`) VALUES (7, 153, 2, NULL, '999', '2026-04-29 20:03:55', '2026-04-29 20:03:55');
INSERT INTO `material_comments` (`id`, `user_id`, `material_id`, `parent_comment_id`, `comment`, `created_at`, `updated_at`) VALUES (8, 1, 3, NULL, '这是一条测试评论', '2026-04-29 21:01:59', '2026-04-29 21:01:59');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of material_ratings
-- ----------------------------
BEGIN;
INSERT INTO `material_ratings` (`id`, `user_id`, `material_id`, `rating`, `created_at`) VALUES (1, 1, 2, 8, '2026-04-29 19:32:23');
INSERT INTO `material_ratings` (`id`, `user_id`, `material_id`, `rating`, `created_at`) VALUES (2, 153, 2, 8, '2026-04-29 19:42:51');
INSERT INTO `material_ratings` (`id`, `user_id`, `material_id`, `rating`, `created_at`) VALUES (3, 1, 3, 5, '2026-04-29 19:50:55');
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
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of orders
-- ----------------------------
BEGIN;
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (132, 'ORDER202604291600001535', 153, 5, '考公VIP季卡', 119, 1, 119, 1, 1, NULL, '2026-04-29 16:00:01', NULL, NULL, '2026-04-29 16:00:00', '2026-04-29 16:00:01', '{\"email\": \"2105086055@qq.com\", \"phone\": \"18109271096\", \"gender\": 0, \"username\": \"惠重阳\", \"birthdate\": \"2026-04-29\", \"real_name\": \"惠重阳\", \"kaogong_requirements\": {\"majors\": \"计算机\", \"keywords\": \"计算机软件\", \"education\": \"本科\", \"provinces\": \"上海\", \"position_types\": \"公务员\", \"is_fresh_graduate\": \"否\"}}');
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (133, 'ORDER202604291601051534', 153, 4, '考公VIP月卡', 49, 1, 49, 1, 1, NULL, '2026-04-29 16:01:06', NULL, NULL, '2026-04-29 16:01:06', '2026-04-29 16:01:06', '{}');
INSERT INTO `orders` (`id`, `order_no`, `user_id`, `product_id`, `product_name`, `price`, `quantity`, `total_amount`, `payment_method`, `payment_status`, `trade_no`, `payment_time`, `refund_time`, `expire_time`, `created_at`, `updated_at`, `user_requirements`) VALUES (136, 'ORDER202604292134041534', 153, 4, '考公VIP月卡', 49, 1, 49, 2, 0, NULL, NULL, NULL, NULL, '2026-04-29 21:34:05', '2026-04-29 21:34:05', '{}');
COMMIT;

-- ----------------------------
-- Table structure for points_records
-- ----------------------------
DROP TABLE IF EXISTS `points_records`;
CREATE TABLE `points_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `points` int NOT NULL,
  `balance` int NOT NULL,
  `type` int NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `related_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_type` (`type`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of points_records
-- ----------------------------
BEGIN;
INSERT INTO `points_records` (`id`, `user_id`, `points`, `balance`, `type`, `description`, `related_id`, `created_at`) VALUES (1, 1, 10, 10, 1, '签到获得10积分', NULL, '2026-04-26 19:36:20');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `balance`, `type`, `description`, `related_id`, `created_at`) VALUES (9, 153, 10, 10, 1, '签到获得10积分', NULL, '2026-04-29 16:14:09');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `balance`, `type`, `description`, `related_id`, `created_at`) VALUES (10, 153, -10, 0, 2, '兑换礼品: 飞鼠', NULL, '2026-04-29 16:14:24');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `balance`, `type`, `description`, `related_id`, `created_at`) VALUES (11, 1, 10, 20, 1, '签到获得10积分', NULL, '2026-04-29 19:53:22');
INSERT INTO `points_records` (`id`, `user_id`, `points`, `balance`, `type`, `description`, `related_id`, `created_at`) VALUES (12, 153, 10, 10, 1, '签到获得10积分', NULL, '2026-04-30 13:32:09');
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
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
-- Table structure for sign_in_records
-- ----------------------------
DROP TABLE IF EXISTS `sign_in_records`;
CREATE TABLE `sign_in_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `sign_date` date NOT NULL,
  `points_earned` int DEFAULT '10',
  `continuous_days` int DEFAULT '1',
  `ip_address` varchar(45) DEFAULT NULL,
  `device_info` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_date` (`user_id`,`sign_date`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_sign_date` (`sign_date`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of sign_in_records
-- ----------------------------
BEGIN;
INSERT INTO `sign_in_records` (`id`, `user_id`, `sign_date`, `points_earned`, `continuous_days`, `ip_address`, `device_info`, `created_at`) VALUES (1, 1, '2026-04-26', 10, 1, NULL, NULL, '2026-04-26 19:36:20');
INSERT INTO `sign_in_records` (`id`, `user_id`, `sign_date`, `points_earned`, `continuous_days`, `ip_address`, `device_info`, `created_at`) VALUES (8, 153, '2026-04-29', 10, 1, NULL, NULL, '2026-04-29 16:14:09');
INSERT INTO `sign_in_records` (`id`, `user_id`, `sign_date`, `points_earned`, `continuous_days`, `ip_address`, `device_info`, `created_at`) VALUES (9, 1, '2026-04-29', 10, 1, NULL, NULL, '2026-04-29 19:53:22');
INSERT INTO `sign_in_records` (`id`, `user_id`, `sign_date`, `points_earned`, `continuous_days`, `ip_address`, `device_info`, `created_at`) VALUES (10, 153, '2026-04-30', 10, 2, NULL, NULL, '2026-04-30 13:32:09');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of system_config
-- ----------------------------
BEGIN;
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (1, 'crawler_interval', '10（更新后）', 1, '爬虫默认抓取间隔(分钟) - 更新于 2026-04-16', 1, 1, '2026-04-08 20:28:14', '2026-04-16 18:10:40');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (2, 'max_concurrent_crawlers', '5', 1, '最大并发爬虫数', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (4, 'trial_days', '3', 1, '免费试用天数', 1, 1, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (5, 'wechat_app_id', '', 0, '微信公众号AppID', 0, 1, '2026-04-08 20:28:14', '2026-04-16 18:11:06');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (6, 'wechat_app_secret', '', 0, '微信公众号AppSecret', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (7, 'alipay_app_id', '', 0, '支付宝AppID', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (8, 'alipay_private_key', '', 0, '支付宝私钥', 0, 0, '2026-04-08 20:28:14', '2026-04-08 20:28:14');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (9, 'push_settings', '{\'frequency\': \'weekly\', \'time\': \'10:30\'}', 3, '推送设置', 1, 1, '2026-04-20 17:12:40', '2026-04-20 17:12:40');
INSERT INTO `system_config` (`id`, `config_key`, `config_value`, `config_type`, `description`, `is_system`, `status`, `created_at`, `updated_at`) VALUES (10, 'email_1', '尊敬的 {username}：\n\n恭喜您支付成功！您的{service_type}推送服务已开通。\n\n服务详情：\n产品名称：{product_name}\n服务类型：{service_type}推送服务\n服务开始时间：{start_date}\n服务结束时间：{end_date}\n服务时长：{duration}天\n\n订阅信息：\n您已成功订阅{service_type}推送服务，我们将为您提供以下内容：\n- 最新{service_type}相关资讯和政策变化\n- 个性化的考试信息推送\n- 专业的备考指导和建议\n\n如有疑问，请联系客服。\n\n此致\n双赛道情报通团队\n', 0, '考研产品邮件通知', 0, 1, '2026-04-28 20:20:06', '2026-04-28 20:20:06');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_favorites
-- ----------------------------
BEGIN;
INSERT INTO `user_favorites` (`id`, `user_id`, `info_id`, `category`, `created_at`) VALUES (11, 1, 2, 3, '2026-04-29 16:17:59');
INSERT INTO `user_favorites` (`id`, `user_id`, `info_id`, `category`, `created_at`) VALUES (15, 1, 3, 3, '2026-04-29 21:00:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=251 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_keywords
-- ----------------------------
BEGIN;
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (146, 1, '人工智能', 1, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (147, 1, '机器学习', 1, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (148, 1, '公务员', 2, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (149, 1, '国考', 2, 1, '2026-04-15 03:16:17', '2026-04-15 11:16:17');
INSERT INTO `user_keywords` (`id`, `user_id`, `keyword`, `category`, `is_active`, `created_at`, `updated_at`) VALUES (250, 153, '计算机软件', 2, 1, '2026-04-29 16:00:00', '2026-04-29 16:00:00');
COMMIT;

-- ----------------------------
-- Table structure for user_login_records
-- ----------------------------
DROP TABLE IF EXISTS `user_login_records`;
CREATE TABLE `user_login_records` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `login_date` date NOT NULL COMMENT '登录日期',
  `login_time` datetime DEFAULT NULL COMMENT '登录时间',
  `login_ip` varchar(45) DEFAULT NULL COMMENT '登录IP',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_login_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user_login_records
-- ----------------------------
BEGIN;
INSERT INTO `user_login_records` (`id`, `user_id`, `login_date`, `login_time`, `login_ip`) VALUES (4, 1, '2026-04-28', '2026-04-28 18:27:18', '127.0.0.1');
INSERT INTO `user_login_records` (`id`, `user_id`, `login_date`, `login_time`, `login_ip`) VALUES (8, 1, '2026-04-29', '2026-04-29 14:16:58', '127.0.0.1');
INSERT INTO `user_login_records` (`id`, `user_id`, `login_date`, `login_time`, `login_ip`) VALUES (9, 153, '2026-04-29', '2026-04-29 15:58:32', '127.0.0.1');
INSERT INTO `user_login_records` (`id`, `user_id`, `login_date`, `login_time`, `login_ip`) VALUES (10, 153, '2026-04-30', '2026-04-30 13:32:08', '127.0.0.1');
INSERT INTO `user_login_records` (`id`, `user_id`, `login_date`, `login_time`, `login_ip`) VALUES (11, 1, '2026-04-30', '2026-04-30 15:03:11', '127.0.0.1');
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
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of user_subscriptions
-- ----------------------------
BEGIN;
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (71, 1, 3, 1, '{\"push\": {}, \"kaoyan\": {\"types\": \"招生简章\", \"majors\": \"计算机\", \"schools\": [\"复旦大学\", \"上海交通大学\", \"北京大学\"], \"keywords\": \"34所\", \"provinces\": [\"上海\", \"北京\", \"广东\"]}, \"kaogong\": {\"majors\": \"计算机\", \"keywords\": \"国考\", \"education\": \"本科\", \"provinces\": [\"上海\", \"北京\"], \"position_types\": \"公务员\", \"is_fresh_graduate\": \"否\"}}', '2026-04-15 03:14:44', '2026-04-29 21:23:27');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (118, 151, 3, 1, '{\"kaoyan\": {\"majors\": [], \"schools\": [], \"provinces\": [], \"study_type\": [], \"degree_type\": []}, \"kaogong\": {\"majors\": [], \"education\": [\"不限\"], \"provinces\": [], \"is_unlimited\": null, \"position_types\": [], \"is_fresh_graduate\": \"不限\"}}', '2026-04-29 14:15:54', '2026-04-29 14:15:54');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (119, 153, 3, 1, '{\"kaoyan\": {}, \"kaogong\": {\"majors\": \"计算机\", \"keywords\": \"计算机软件\", \"education\": \"本科\", \"provinces\": \"上海\", \"position_types\": \"公务员\", \"is_fresh_graduate\": \"否\"}}', '2026-04-29 15:58:32', '2026-04-29 16:00:00');
INSERT INTO `user_subscriptions` (`id`, `user_id`, `subscribe_type`, `status`, `config_json`, `created_at`, `updated_at`) VALUES (120, 154, 2, 1, '{\"kaoyan\": {\"majors\": [], \"schools\": [], \"provinces\": [], \"study_type\": [], \"degree_type\": []}, \"kaogong\": {\"majors\": [], \"education\": [\"不限\"], \"provinces\": [], \"is_unlimited\": null, \"position_types\": [], \"is_fresh_graduate\": \"不限\"}}', '2026-04-29 20:53:30', '2026-04-29 20:53:30');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
  `points` int DEFAULT '0',
  `continuous_sign_days` int DEFAULT '0',
  `last_sign_date` datetime DEFAULT NULL,
  `address` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_type` int DEFAULT '1',
  `wx_openid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `wx_unionid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_bound` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  UNIQUE KEY `uk_phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`, `points`, `continuous_sign_days`, `last_sign_date`, `address`, `user_type`, `wx_openid`, `wx_unionid`, `phone_bound`) VALUES (1, 'admin', 'admin@shuangsai.com', '13800138000', 'admin123', NULL, '测试用户', NULL, 0, NULL, NULL, '127.0.0.1', '2026-04-30 15:24:01', 1, 1, 1, '2026-04-16 11:29:54', '2026-07-15 11:29:54', 1, 0, '2026-04-08 20:28:14', '2026-04-30 16:12:09', 1, 40, 1, '2026-04-29 19:53:22', '北京市海淀区测试地址123号', 1, NULL, NULL, 0);
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`, `points`, `continuous_sign_days`, `last_sign_date`, `address`, `user_type`, `wx_openid`, `wx_unionid`, `phone_bound`) VALUES (153, '惠重阳', '2105086055@qq.com', '18109271096', '', NULL, '惠重阳', NULL, 0, '2026-04-29 00:00:00', '127.0.0.1', '127.0.0.1', '2026-04-29 15:58:32', 1, 0, 1, '2026-07-29 16:00:01', '2026-08-28 16:00:01', 2, 0, '2026-04-29 15:58:32', '2026-04-30 17:33:02', 1, 30, 2, '2026-04-30 13:32:09', '111', 2, 'mock_81f930c953705001', NULL, 1);
INSERT INTO `users` (`id`, `username`, `email`, `phone`, `password`, `avatar`, `real_name`, `id_card`, `gender`, `birthdate`, `register_ip`, `last_login_ip`, `last_login_time`, `is_active`, `is_admin`, `is_vip`, `vip_start_time`, `vip_end_time`, `vip_type`, `trial_status`, `created_at`, `updated_at`, `need_change_password`, `points`, `continuous_sign_days`, `last_sign_date`, `address`, `user_type`, `wx_openid`, `wx_unionid`, `phone_bound`) VALUES (154, 'testuser2', 'test2@example.com', '13900139000', 'changeme123', NULL, NULL, NULL, 0, NULL, '127.0.0.1', NULL, NULL, 1, 0, 0, NULL, NULL, 0, 1, '2026-04-29 20:53:30', '2026-04-29 20:53:30', 1, 0, 0, NULL, NULL, 1, NULL, NULL, 0);
COMMIT;

-- ----------------------------
-- View structure for order_statistics_view
-- ----------------------------
DROP VIEW IF EXISTS `order_statistics_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `order_statistics_view` AS select cast(`orders`.`created_at` as date) AS `date`,count(0) AS `total_orders`,sum(`orders`.`total_amount`) AS `total_amount`,count((case when (`orders`.`payment_status` = 1) then 1 end)) AS `paid_orders`,sum((case when (`orders`.`payment_status` = 1) then `orders`.`total_amount` else 0 end)) AS `paid_amount`,sum((case when (`orders`.`payment_status` = 3) then `orders`.`total_amount` else 0 end)) AS `refund_amount` from `orders` group by cast(`orders`.`created_at` as date);

SET FOREIGN_KEY_CHECKS = 1;
