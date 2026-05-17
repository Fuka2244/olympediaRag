-- 选中的DDL（由schema linking生成）
/*
 Navicat Premium Data Transfer

 Source Server         : SportsQA
 Source Server Type    : MySQL
 Source Server Version : 90001 (9.0.1)
 Source Host           : localhost:3306
 Source Schema         : sport_qa

 Target Server Type    : MySQL
 Target Server Version : 90001 (9.0.1)
 File Encoding         : 65001

 Date: 19/03/2026 23:06:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for affiliations_athletes
-- ----------------------------
DROP TABLE IF EXISTS `affiliations_athletes`;
CREATE TABLE `affiliations_athletes`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `affiliation_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构唯一ID',
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `athlete_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家代码',
  `sport` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '体育项目',
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '类型（如Olympics, Non-starter）',
  `year` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '年份',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_affiliation_id`(`affiliation_id` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_sport`(`sport` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 151803 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '机构所有运动员表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for affiliations_infobox
-- ----------------------------
DROP TABLE IF EXISTS `affiliations_infobox`;
CREATE TABLE `affiliations_infobox`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `affiliation_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构唯一ID',
  `place_name_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地点名称ID',
  `full_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '机构全称',
  `short_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '机构简称',
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地点',
  `sports` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '体育项目',
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '备注',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据来源URL',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_affiliation_id`(`affiliation_id` ASC) USING BTREE,
  INDEX `idx_full_name`(`full_name` ASC) USING BTREE,
  INDEX `idx_place`(`place` ASC) USING BTREE,
  INDEX `idx_place_name_id`(`place_name_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 35467 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '机构信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for athlete_biography
-- ----------------------------
DROP TABLE IF EXISTS `athlete_biography`;
CREATE TABLE `athlete_biography`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动员ID',
  `pid` int NOT NULL COMMENT '段落ID',
  `biography_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '传记文本',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_athlete_pid`(`athlete_id` ASC, `pid` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99476 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '生平传记表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for athlete_infobox
-- ----------------------------
DROP TABLE IF EXISTS `athlete_infobox`;
CREATE TABLE `athlete_infobox`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动员唯一标识(直接采用url后的编号)',
  `affiliation_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '所属机构ID',
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家奥委会代码',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据来源URL',
  `roles` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色(运动员/教练等)',
  `sex` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '性别',
  `full_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '全名',
  `used_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '常用名',
  `original_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '原名',
  `other_names` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '其他名称',
  `born_time` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '出生时间',
  `died_time` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '死亡时间',
  `born_place` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '出生地点',
  `born_place_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '出生地点ID',
  `died_place` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '死亡地点',
  `died_place_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '死亡地点ID',
  `height` int NULL DEFAULT NULL COMMENT '身高(单位cm)',
  `weight` int NULL DEFAULT NULL COMMENT '体重(单位kg)',
  `affiliations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '所属机构',
  `nationality` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国籍',
  `name_order` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '姓名顺序',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_full_name`(`full_name` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 195316 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '运动员基本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for athlete_olympic_records
-- ----------------------------
DROP TABLE IF EXISTS `athlete_olympic_records`;
CREATE TABLE `athlete_olympic_records`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动员ID',
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运赛事名称',
  `edition_id` int NULL DEFAULT NULL COMMENT '奥运赛事的id',
  `date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '日期',
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `sport_group` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动组别',
  `sport_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目ID',
  `sport_group_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动组别ID',
  `event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '具体比赛',
  `event_name_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '具体比赛ID',
  `phase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '阶段',
  `mark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '成绩/纪录',
  `result_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '结果ID',
  `pos` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '排名',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 924 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运纪录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for athlete_organization_roles
-- ----------------------------
DROP TABLE IF EXISTS `athlete_organization_roles`;
CREATE TABLE `athlete_organization_roles`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动员ID',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '担任职务',
  `organization` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '组织名称',
  `organization_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '组织ID',
  `tenure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '任期',
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家奥委会代码',
  `as_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '曾用名',
  `nationality` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国籍',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4153 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '组织角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for athlete_other_participations
-- ----------------------------
DROP TABLE IF EXISTS `athlete_other_participations`;
CREATE TABLE `athlete_other_participations`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动员ID',
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运赛事名称',
  `edition_id` int NULL DEFAULT NULL COMMENT '奥运赛事的id',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色',
  `role_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色ID',
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家奥委会代码',
  `as_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '曾用名',
  `nationality` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国籍',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8805 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '其他参与表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for athlete_results
-- ----------------------------
DROP TABLE IF EXISTS `athlete_results`;
CREATE TABLE `athlete_results`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动员ID',
  `edition_id` int NULL DEFAULT NULL COMMENT '奥运赛事的id',
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家奥委会代码',
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运赛事名称',
  `discipline_sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目/运动',
  `event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '具体比赛项目',
  `team` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '团队名称',
  `pos` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '排名',
  `medal` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奖牌类型(金/银/铜)',
  `as_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '曾用名',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_games`(`games` ASC) USING BTREE,
  INDEX `idx_event`(`event` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 622118 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '参赛结果表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ceremonies_athlete_oath
-- ----------------------------
DROP TABLE IF EXISTS `ceremonies_athlete_oath`;
CREATE TABLE `ceremonies_athlete_oath`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `competition_type` enum('Olympic Games','Youth Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事类型',
  `edition_id` int NULL DEFAULT NULL COMMENT '对应links中的url编号',
  `season` enum('Summer','Winter','Equestrian') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛季类型',
  `olympics_year` year NULL DEFAULT NULL COMMENT '奥运会年份',
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '宣誓运动员名字',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_olympics_year`(`olympics_year` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_athlete`(`athlete`(100) ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运会运动员宣誓表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ceremonies_coach_oath
-- ----------------------------
DROP TABLE IF EXISTS `ceremonies_coach_oath`;
CREATE TABLE `ceremonies_coach_oath`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `competition_type` enum('Olympic Games','Youth Olympic Games','Intercalated Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事类型',
  `edition_id` int NULL DEFAULT NULL COMMENT '对应links中的url编号',
  `season` enum('Summer','Winter','Equestrian') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛季类型',
  `olympics_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运会年份',
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员名字',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_olympics_year`(`olympics_year` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_athlete`(`athlete`(100) ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE,
  INDEX `idx_season`(`season` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运会教练宣誓表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ceremonies_official_oath
-- ----------------------------
DROP TABLE IF EXISTS `ceremonies_official_oath`;
CREATE TABLE `ceremonies_official_oath`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `competition_type` enum('Olympic Games','Youth Olympic Games','Intercalated Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事类型',
  `edition_id` int NULL DEFAULT NULL COMMENT '对应links中的url编号',
  `season` enum('Summer','Winter','Equestrian') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛季类型',
  `olympics_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运会年份',
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员名字',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_olympics_year`(`olympics_year` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_athlete`(`athlete`(100) ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE,
  INDEX `idx_season`(`season` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运会官员宣誓表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ceremonies_officially_opened
-- ----------------------------
DROP TABLE IF EXISTS `ceremonies_officially_opened`;
CREATE TABLE `ceremonies_officially_opened`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `competition_type` enum('Olympic Games','Youth Olympic Games','Intercalated Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事类型',
  `edition_id` int NULL DEFAULT NULL COMMENT '对应links中的url编号',
  `season` enum('Summer','Winter','Equestrian') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛季类型',
  `olympics_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运会年份',
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '开幕者名字',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `function` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '职务',
  `noc` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_olympics_year`(`olympics_year` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_athlete`(`athlete`(100) ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE,
  INDEX `idx_season`(`season` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运会开幕式宣布者表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ceremonies_torch_bearers
-- ----------------------------
DROP TABLE IF EXISTS `ceremonies_torch_bearers`;
CREATE TABLE `ceremonies_torch_bearers`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `competition_type` enum('Olympic Games','Youth Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事类型',
  `edition_id` int NULL DEFAULT NULL COMMENT '对应links中的url编号',
  `season` enum('Summer','Winter','Equestrian') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛季类型',
  `olympics_year` year NULL DEFAULT NULL COMMENT '奥运会年份',
  `torch_bearer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '火炬手名字',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `role` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色描述',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_olympics_year`(`olympics_year` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_torch_bearer`(`torch_bearer`(100) ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 309 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运会火炬传递者表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for definitions
-- ----------------------------
DROP TABLE IF EXISTS `definitions`;
CREATE TABLE `definitions`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `definition_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '定义ID(从URL提取)',
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '页面标题',
  `pid` int NULL DEFAULT NULL COMMENT '段落ID(text类型时使用)',
  `text_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '文本内容',
  `links_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '链接URL集合(用#分隔)',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据来源URL',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_definition_id`(`definition_id` ASC) USING BTREE,
  INDEX `idx_pid`(`pid` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 519 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运定义表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_countries
-- ----------------------------
DROP TABLE IF EXISTS `edition_countries`;
CREATE TABLE `edition_countries`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '届次ID',
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '页面标题',
  `noc` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'NOC国家代码',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家名称',
  `men` int NULL DEFAULT NULL COMMENT '男性人数',
  `women` int NULL DEFAULT NULL COMMENT '女性人数',
  `total` int NULL DEFAULT NULL COMMENT '总人数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_country`(`country` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13197 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_result
-- ----------------------------
DROP TABLE IF EXISTS `edition_result`;
CREATE TABLE `edition_result`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '届次ID',
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '页面标题',
  `sport_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动大项名称',
  `event_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '比赛项目名称',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '参赛类别',
  `full_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '完整项目名称',
  `result_id` int NULL DEFAULT NULL COMMENT 'Olympedia 结果页编号',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始链接',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_name`(`event_name` ASC) USING BTREE,
  INDEX `idx_category`(`category` ASC) USING BTREE,
  INDEX `idx_sport_name`(`sport_name` ASC) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10089 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_sport_events
-- ----------------------------
DROP TABLE IF EXISTS `edition_sport_events`;
CREATE TABLE `edition_sport_events`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL COMMENT '项目 ID',
  `result_id` int NULL DEFAULT NULL COMMENT '结果ID',
  `event_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目名称',
  `participants` int NULL DEFAULT NULL COMMENT '参赛人数',
  `nocs_count` int NULL DEFAULT NULL COMMENT '参赛国家数',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目状态',
  `date` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '日期',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始链接',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_event_name`(`event_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11178 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_sport_info
-- ----------------------------
DROP TABLE IF EXISTS `edition_sport_info`;
CREATE TABLE `edition_sport_info`  (
  `edition_id` int NOT NULL COMMENT '从URL提取',
  `event_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事全称',
  `date` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '开始日期',
  `venue` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '比赛场馆',
  `venue_id` int NULL DEFAULT NULL COMMENT '场馆ID',
  `medal_events` int NULL DEFAULT NULL COMMENT '金牌项目总数',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始链接',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`edition_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_sport_medal
-- ----------------------------
DROP TABLE IF EXISTS `edition_sport_medal`;
CREATE TABLE `edition_sport_medal`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL COMMENT '从url上的编号',
  `sport_event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '比赛项目名称',
  `result_id` int NULL DEFAULT NULL COMMENT '结果ID',
  `gold` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '金牌获得者',
  `gold_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '金牌国家代码',
  `gold_athletes_id` int NULL DEFAULT NULL COMMENT '金牌运动员ID',
  `silver` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '银牌获得者',
  `silver_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '银牌国家代码',
  `silver_athletes_id` int NULL DEFAULT NULL COMMENT '银牌运动员ID',
  `bronze` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '铜牌获得者',
  `bronze_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '铜牌国家代码',
  `bronze_athletes_id` int NULL DEFAULT NULL COMMENT '铜牌运动员ID',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始链接',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_sport_event`(`sport_event` ASC) USING BTREE,
  INDEX `idx_gold_noc`(`gold_noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9193 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_sport_medal_table
-- ----------------------------
DROP TABLE IF EXISTS `edition_sport_medal_table`;
CREATE TABLE `edition_sport_medal_table`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL COMMENT '期次ID',
  `noc_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '国家代码',
  `country_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家名称',
  `gold` int NULL DEFAULT 0 COMMENT '金牌数',
  `silver` int NULL DEFAULT 0 COMMENT '银牌数',
  `bronze` int NULL DEFAULT 0 COMMENT '铜牌数',
  `total` int NULL DEFAULT 0 COMMENT '总计',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始链接',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_noc_code`(`noc_code` ASC) USING BTREE,
  INDEX `idx_total`(`total` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10934 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for edition_sport_overview
-- ----------------------------
DROP TABLE IF EXISTS `edition_sport_overview`;
CREATE TABLE `edition_sport_overview`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL COMMENT '期次ID',
  `pid` int NOT NULL COMMENT '段落ID',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '历史描述内容',
  `word_count` int NULL DEFAULT NULL COMMENT '字数',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始链接',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_pid`(`pid` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3019 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_basic_info
-- ----------------------------
DROP TABLE IF EXISTS `editions_basic_info`;
CREATE TABLE `editions_basic_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `orgnization_id` int NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `competition_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `number_and_year` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `host_city` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `opening_ceremony` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `closing_ceremony` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `competition_dates` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `ocog` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `participants` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `participants_count` int NULL DEFAULT NULL,
  `countries_count` int NULL DEFAULT NULL,
  `medal_events` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `medal_events_count` int NULL DEFAULT NULL,
  `medal_disciplines_count` int NULL DEFAULT NULL,
  `other_events` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `other_events_count` int NULL DEFAULT NULL,
  `other_disciplines_count` int NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_number_and_year`(`number_and_year` ASC) USING BTREE,
  INDEX `idx_host_city`(`host_city` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 374 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_bid_process
-- ----------------------------
DROP TABLE IF EXISTS `editions_bid_process`;
CREATE TABLE `editions_bid_process`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `paragraph_id` int NOT NULL,
  `paragraph_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `word_count` int NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_paragraph_id`(`paragraph_id` ASC) USING BTREE,
  CONSTRAINT `editions_bid_process_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 90 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_ceremonies
-- ----------------------------
DROP TABLE IF EXISTS `editions_ceremonies`;
CREATE TABLE `editions_ceremonies`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `ceremony_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `officially_opened_by` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `opened_by_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `opened_by_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `opened_by_noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `flagbearers_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `flagbearers_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_ceremony_type`(`ceremony_type` ASC) USING BTREE,
  CONSTRAINT `editions_ceremonies_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_medal_details
-- ----------------------------
DROP TABLE IF EXISTS `editions_medal_details`;
CREATE TABLE `editions_medal_details`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `sport_event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目名称 (from section_title)',
  `event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '具体项目名称 (from Event)',
  `gold` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '金牌获得者',
  `gold_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '金牌国家代码',
  `silver` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '银牌获得者',
  `silver_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '银牌国家代码',
  `bronze` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '铜牌获得者',
  `bronze_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '铜牌国家代码',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '原始URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_gold_noc`(`gold_noc` ASC) USING BTREE,
  INDEX `idx_sport_event`(`sport_event`(100) ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9112 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_medal_disciplines
-- ----------------------------
DROP TABLE IF EXISTS `editions_medal_disciplines`;
CREATE TABLE `editions_medal_disciplines`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `discipline_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `discipline_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `event_count` int NULL DEFAULT NULL,
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_discipline_name`(`discipline_name` ASC) USING BTREE,
  CONSTRAINT `editions_medal_disciplines_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_medal_table
-- ----------------------------
DROP TABLE IF EXISTS `editions_medal_table`;
CREATE TABLE `editions_medal_table`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `noc_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `country_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `gold` int NULL DEFAULT 0,
  `silver` int NULL DEFAULT 0,
  `bronze` int NULL DEFAULT 0,
  `total` int NULL DEFAULT 0,
  `rank` int NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_noc_code`(`noc_code` ASC) USING BTREE,
  INDEX `idx_rank`(`rank` ASC) USING BTREE,
  INDEX `idx_total`(`total` ASC) USING BTREE,
  CONSTRAINT `editions_medal_table_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1399 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_mixed_team_medals
-- ----------------------------
DROP TABLE IF EXISTS `editions_mixed_team_medals`;
CREATE TABLE `editions_mixed_team_medals`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `sport_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `event_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `gold_team` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `silver_team` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `bronze_team` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  CONSTRAINT `editions_mixed_team_medals_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_other_disciplines
-- ----------------------------
DROP TABLE IF EXISTS `editions_other_disciplines`;
CREATE TABLE `editions_other_disciplines`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `discipline_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `discipline_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_discipline_name`(`discipline_name` ASC) USING BTREE,
  CONSTRAINT `editions_other_disciplines_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_overview
-- ----------------------------
DROP TABLE IF EXISTS `editions_overview`;
CREATE TABLE `editions_overview`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `paragraph_id` int NOT NULL,
  `paragraph_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `word_count` int NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_paragraph_id`(`paragraph_id` ASC) USING BTREE,
  CONSTRAINT `editions_overview_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 438 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for editions_top_competitors
-- ----------------------------
DROP TABLE IF EXISTS `editions_top_competitors`;
CREATE TABLE `editions_top_competitors`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `edition_id` int NOT NULL,
  `athlete_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `athlete_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `noc_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `gold` int NULL DEFAULT 0,
  `silver` int NULL DEFAULT 0,
  `bronze` int NULL DEFAULT 0,
  `total` int NULL DEFAULT 0,
  `athlete_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_athlete_name`(`athlete_name` ASC) USING BTREE,
  INDEX `idx_total`(`total` ASC) USING BTREE,
  CONSTRAINT `editions_top_competitors_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1427 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_basic_info
-- ----------------------------
DROP TABLE IF EXISTS `event_names_basic_info`;
CREATE TABLE `event_names_basic_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '项目ID',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据来源URL',
  `page_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '页面标题',
  `times_held` int NULL DEFAULT NULL COMMENT '举办次数',
  `total_participants` int NULL DEFAULT NULL COMMENT '总参与人数',
  `total_countries` int NULL DEFAULT NULL COMMENT '总参与国家数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1687 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '项目基本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_best_performance_bycountry
-- ----------------------------
DROP TABLE IF EXISTS `event_names_best_performance_bycountry`;
CREATE TABLE `event_names_best_performance_bycountry`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '项目ID',
  `country_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家名称',
  `country_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `games` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事',
  `edition_id` int NULL DEFAULT NULL COMMENT '赛事ID',
  `athlete_team` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员/团队',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `placement` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名次',
  `result_id` int NULL DEFAULT NULL COMMENT '结果ID',
  `medal` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奖牌',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_country_code`(`country_code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 40488 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '各国最佳表现表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_medal_winners
-- ----------------------------
DROP TABLE IF EXISTS `event_names_medal_winners`;
CREATE TABLE `event_names_medal_winners`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '项目ID',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '年份',
  `result_id` int NULL DEFAULT NULL COMMENT '结果ID',
  `gold_athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '金牌获得者',
  `gold_noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '金牌国家代码',
  `gold_athlete_id` int NULL DEFAULT NULL COMMENT '金牌运动员ID',
  `silver_athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '银牌获得者',
  `silver_noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '银牌国家代码',
  `silver_athlete_id` int NULL DEFAULT NULL COMMENT '银牌运动员ID',
  `bronze_athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '铜牌获得者',
  `bronze_noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '铜牌国家代码',
  `bronze_athlete_id` int NULL DEFAULT NULL COMMENT '铜牌运动员ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_year`(`year` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9115 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奖牌获得者表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_medals_by_country
-- ----------------------------
DROP TABLE IF EXISTS `event_names_medals_by_country`;
CREATE TABLE `event_names_medals_by_country`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '项目ID',
  `country_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家名称',
  `country_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `gold` int NULL DEFAULT 0 COMMENT '金牌数',
  `silver` int NULL DEFAULT 0 COMMENT '银牌数',
  `bronze` int NULL DEFAULT 0 COMMENT '铜牌数',
  `total` int NULL DEFAULT 0 COMMENT '总奖牌数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_country_code`(`country_code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10724 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '各国奖牌数表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_participants
-- ----------------------------
DROP TABLE IF EXISTS `event_names_participants`;
CREATE TABLE `event_names_participants`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_name_id` int NOT NULL COMMENT '项目ID',
  `event_id` int NULL DEFAULT NULL COMMENT '赛事ID',
  `result_id` int NULL DEFAULT NULL COMMENT '结果ID',
  `year` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '年份',
  `event_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事名称',
  `status` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '状态',
  `participants` int NULL DEFAULT NULL COMMENT '参与人数',
  `nocs` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '参与国家',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_year`(`year` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10090 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '参与者表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_top_medallists
-- ----------------------------
DROP TABLE IF EXISTS `event_names_top_medallists`;
CREATE TABLE `event_names_top_medallists`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '项目ID',
  `athlete_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `gold` int NULL DEFAULT 0 COMMENT '金牌数',
  `silver` int NULL DEFAULT 0 COMMENT '银牌数',
  `bronze` int NULL DEFAULT 0 COMMENT '铜牌数',
  `total` int NULL DEFAULT 0 COMMENT '总奖牌数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_athlete_name`(`athlete_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9403 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '顶级奖牌得主表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_names_total_participants
-- ----------------------------
DROP TABLE IF EXISTS `event_names_total_participants`;
CREATE TABLE `event_names_total_participants`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_name_id` int NOT NULL COMMENT '项目ID (从URL提取)',
  `athlete_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `athlete_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `roles` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色',
  `sports` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `era` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '参赛时期',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_event_name_athlete`(`event_name_id` ASC, `athlete_id` ASC) USING BTREE,
  INDEX `idx_event_name_id`(`event_name_id` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 289058 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '项目参与者信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for event_total_participants
-- ----------------------------
DROP TABLE IF EXISTS `event_total_participants`;
CREATE TABLE `event_total_participants`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '赛事ID (从URL提取)',
  `athlete_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员ID',
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `athlete_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `roles` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色',
  `sports` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动项目',
  `era` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '参赛时期',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_event_athlete`(`event_id` ASC, `athlete_id` ASC) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 370809 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '赛事参与者信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for events_non_starters
-- ----------------------------
DROP TABLE IF EXISTS `events_non_starters`;
CREATE TABLE `events_non_starters`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '赛事ID',
  `athletes_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员ID',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据来源URL',
  `page_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '页面标题',
  `nr` int NULL DEFAULT NULL COMMENT '编号',
  `athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `noc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家代码',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_nr`(`nr` ASC) USING BTREE,
  INDEX `idx_athlete`(`athlete` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19532 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '报名但未参赛的运动员信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for events_participants
-- ----------------------------
DROP TABLE IF EXISTS `events_participants`;
CREATE TABLE `events_participants`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NOT NULL COMMENT '赛事ID',
  `athletes_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员ID',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据来源URL',
  `page_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '页面标题',
  `nr` int NULL DEFAULT NULL COMMENT '编号',
  `athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `noc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家代码',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_nr`(`nr` ASC) USING BTREE,
  INDEX `idx_athlete`(`athlete` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 355232 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '赛事参与者表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for horse_biography
-- ----------------------------
DROP TABLE IF EXISTS `horse_biography`;
CREATE TABLE `horse_biography`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `horse_id` int NOT NULL COMMENT '马匹ID',
  `pid` int NOT NULL COMMENT '段落ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '传记内容',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_horse_id`(`horse_id` ASC) USING BTREE,
  INDEX `idx_pid`(`pid` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 345 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '马匹传记表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for horse_event_record
-- ----------------------------
DROP TABLE IF EXISTS `horse_event_record`;
CREATE TABLE `horse_event_record`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `horse_id` int NOT NULL COMMENT '马匹ID',
  `games` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奥运赛事',
  `edition_id` int NULL DEFAULT NULL COMMENT '届次ID',
  `discipline` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目/运动',
  `event` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '具体赛事',
  `noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `rider` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '骑手姓名',
  `pos` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名次',
  `medal` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奖牌',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_horse_id`(`horse_id` ASC) USING BTREE,
  INDEX `idx_games`(`games` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8609 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '马匹赛事记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for horse_info
-- ----------------------------
DROP TABLE IF EXISTS `horse_info`;
CREATE TABLE `horse_info`  (
  `horse_id` int NOT NULL COMMENT '马匹ID',
  `name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '马匹名称',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据来源URL',
  `color` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '毛色',
  `sex` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '性别',
  `birth_year` int NULL DEFAULT NULL COMMENT '出生年份',
  `death_year` int NULL DEFAULT NULL COMMENT '死亡年份',
  PRIMARY KEY (`horse_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '马匹基本信息表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
