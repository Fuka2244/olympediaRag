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

 Date: 14/04/2026 16:41:46
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
  `born_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `died_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `born_place` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '出生地点',
  `born_place_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '出生地点ID',
  `died_place` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '死亡地点',
  `died_place_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '死亡地点ID',
  `height` int NULL DEFAULT NULL COMMENT '身高(单位cm)',
  `weight` int NULL DEFAULT NULL COMMENT '体重(单位kg)',
  `affiliations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '所属机构',
  `nationality` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国籍',
  `name_order` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '姓名顺序',
  `age` int NULL DEFAULT NULL,
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
-- Table structure for country_description
-- ----------------------------
DROP TABLE IF EXISTS `country_description`;
CREATE TABLE `country_description`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `pid` int NULL DEFAULT NULL COMMENT '段落ID',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文本内容',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_noc_pid`(`noc` ASC, `pid` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 885 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '国家描述表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_edition
-- ----------------------------
DROP TABLE IF EXISTS `country_edition`;
CREATE TABLE `country_edition`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `edition_id` int NULL DEFAULT NULL COMMENT '届次ID',
  `edition` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '届次名称',
  `as` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参赛名称',
  `men` int NULL DEFAULT NULL COMMENT '男性参赛人数',
  `women` int NULL DEFAULT NULL COMMENT '女性参赛人数',
  `total` int NULL DEFAULT NULL COMMENT '总参赛人数',
  `competition_type` enum('Olympic Games','Ancient Olympic Games','Youth Olympic Games','Intercalated Games','Forerunners To The Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛类型',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6237 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '国家不同届奥运会参赛情况表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_edition_result
-- ----------------------------
DROP TABLE IF EXISTS `country_edition_result`;
CREATE TABLE `country_edition_result`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `result_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `edition_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `athlete_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `medal` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_record`(`noc` ASC, `edition_id` ASC, `sport` ASC, `result_id` ASC, `athlete_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_sport`(`sport` ASC) USING BTREE,
  INDEX `idx_medal`(`medal` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1043097 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_infobox
-- ----------------------------
DROP TABLE IF EXISTS `country_infobox`;
CREATE TABLE `country_infobox`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据来源URL',
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '页面标题',
  `organization` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家奥委会名称',
  `flagbearer` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '旗手数量',
  `organization_id` int NULL DEFAULT NULL COMMENT '组织ID',
  `flagbearer_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '旗手ID(国家代码)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_source_url`(`source_url` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 444 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '国家基本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_medal_by_game
-- ----------------------------
DROP TABLE IF EXISTS `country_medal_by_game`;
CREATE TABLE `country_medal_by_game`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `edition_id` int NULL DEFAULT NULL COMMENT '届次ID',
  `edition` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '届次名称',
  `competition_type` enum('Olympic Games','Ancient Olympic Games','Youth Olympic Games','Intercalated Games','Forerunners To The Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛类型',
  `gold` int NULL DEFAULT 0 COMMENT '金牌数',
  `silver` int NULL DEFAULT 0 COMMENT '银牌数',
  `bronze` int NULL DEFAULT 0 COMMENT '铜牌数',
  `total` int NULL DEFAULT 0 COMMENT '总奖牌数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3182 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '按届次奖牌统计表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_medal_by_sport
-- ----------------------------
DROP TABLE IF EXISTS `country_medal_by_sport`;
CREATE TABLE `country_medal_by_sport`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `competition_type` enum('Olympic Games','Ancient Olympic Games','Youth Olympic Games','Intercalated Games','Forerunners To The Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛类型',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动名称',
  `sport_id` int NULL DEFAULT NULL COMMENT '运动项目ID',
  `gold` int NULL DEFAULT 0 COMMENT '金牌数',
  `silver` int NULL DEFAULT 0 COMMENT '银牌数',
  `bronze` int NULL DEFAULT 0 COMMENT '铜牌数',
  `total` int NULL DEFAULT 0 COMMENT '总奖牌数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE,
  INDEX `idx_sport_id`(`sport_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3045 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '按运动项目奖牌统计表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_most_successful_competitors
-- ----------------------------
DROP TABLE IF EXISTS `country_most_successful_competitors`;
CREATE TABLE `country_most_successful_competitors`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `competition_type` enum('Olympic Games','Ancient Olympic Games','Youth Olympic Games','Intercalated Games','Forerunners To The Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛类型',
  `athlete` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '选手姓名',
  `athlete_id` int NULL DEFAULT NULL COMMENT '选手ID',
  `nat` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家代码(如果有多个用#连接)',
  `gold` int NULL DEFAULT 0 COMMENT '金牌数',
  `silver` int NULL DEFAULT 0 COMMENT '银牌数',
  `bronze` int NULL DEFAULT 0 COMMENT '铜牌数',
  `total` int NULL DEFAULT 0 COMMENT '总奖牌数',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3740 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '最成功的选手表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_participants
-- ----------------------------
DROP TABLE IF EXISTS `country_participants`;
CREATE TABLE `country_participants`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `olympic_games_count` int NULL DEFAULT NULL COMMENT '奥运会参赛人数',
  `olympic_games_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '奥运会参赛统计链接中的国家编号',
  `youth_olympic_games_count` int NULL DEFAULT NULL COMMENT '青奥会参赛人数',
  `youth_olympic_games_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '青奥会参赛统计链接中的国家编号',
  `ancient_olympic_games_count` int NULL DEFAULT NULL COMMENT '古代奥运会参赛人数',
  `ancient_olympic_games_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '古代奥运会参赛统计链接中的国家编号',
  `intercalated_games_count` int NULL DEFAULT NULL COMMENT '届间奥运会参赛人数',
  `intercalated_games_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '届间奥运会参赛统计链接中的国家编号',
  `other_competitors_count` int NULL DEFAULT NULL COMMENT '其他国籍选手人数',
  `other_competitors_noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '其他国籍选手统计链接中的国家编号',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 411 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '国家参赛人员统计表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_sport
-- ----------------------------
DROP TABLE IF EXISTS `country_sport`;
CREATE TABLE `country_sport`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '国家唯一ID(如CHN)',
  `sport_id` int NULL DEFAULT NULL COMMENT '运动项目ID',
  `sport_group_id` int NULL DEFAULT NULL COMMENT '运动组别ID',
  `discipline` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '项目名称(页面中的形式为Discipline (Sport))',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动名称',
  `as` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参赛名称',
  `men` int NULL DEFAULT NULL COMMENT '男性参赛人数',
  `women` int NULL DEFAULT NULL COMMENT '女性参赛人数',
  `total` int NULL DEFAULT NULL COMMENT '总参赛人数',
  `competition_type` enum('Olympic Games','Ancient Olympic Games','Youth Olympic Games','Intercalated Games','Forerunners To The Olympic Games') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛类型',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_sport_id`(`sport_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8257 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '国家不同运动项目参赛情况表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for country_sport_result
-- ----------------------------
DROP TABLE IF EXISTS `country_sport_result`;
CREATE TABLE `country_sport_result`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `page_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `noc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sport_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `competition_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `edition_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `result_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `athlete` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `athlete_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `medal` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_record`(`noc` ASC, `sport_id` ASC, `competition_type` ASC, `edition_name` ASC, `result_id` ASC, `athlete_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_sport_id`(`sport_id` ASC) USING BTREE,
  INDEX `idx_competition_type`(`competition_type` ASC) USING BTREE,
  INDEX `idx_medal`(`medal` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1037146 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

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
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_paragraph_id`(`paragraph_id` ASC) USING BTREE,
  CONSTRAINT `editions_bid_process_ibfk_1` FOREIGN KEY (`edition_id`) REFERENCES `editions_basic_info` (`edition_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 90 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

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
-- Table structure for event_names_countries
-- ----------------------------
DROP TABLE IF EXISTS `event_names_countries`;
CREATE TABLE `event_names_countries`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `event_id` int NULL DEFAULT NULL COMMENT '项目ID',
  `noc` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '国家代码',
  `edition_id` int NULL DEFAULT NULL COMMENT '奥运赛事ID',
  `athlete_id` int NULL DEFAULT NULL COMMENT '运动员ID',
  `result_id` int NULL DEFAULT NULL COMMENT '结果ID',
  `page_title` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '页面标题',
  `game` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '赛事',
  `athlete_team` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运动员/团队',
  `placement` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名次',
  `medal` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '奖牌',
  `source_url` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据来源URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_id`(`event_id` ASC) USING BTREE,
  INDEX `idx_noc`(`noc` ASC) USING BTREE,
  INDEX `idx_edition_id`(`edition_id` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_result_id`(`result_id` ASC) USING BTREE,
  INDEX `idx_noc_event_id`(`noc` ASC, `event_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 228940 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '该项目在某国家的情况表' ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 9092 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '顶级奖牌得主表' ROW_FORMAT = Dynamic;

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
-- Table structure for flagbearers
-- ----------------------------
DROP TABLE IF EXISTS `flagbearers`;
CREATE TABLE `flagbearers`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `country_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ceremony_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `edition` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `edition_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `athlete_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `discipline` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `discipline_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `notes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `order_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `source_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `noc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `country_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15014 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

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

-- ----------------------------
-- Table structure for ioc_meetings
-- ----------------------------
DROP TABLE IF EXISTS `ioc_meetings`;
CREATE TABLE `ioc_meetings`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `meeting_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'Olympedia官方会议ID',
  `meeting_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '会议完整名称',
  `meeting_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '会议类型',
  `year` int NULL DEFAULT NULL COMMENT '年份',
  `dates` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '召开具体日期',
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '举办地点',
  `opened_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '宣布开幕者',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_url_id`(`meeting_url_id` ASC) USING BTREE,
  INDEX `idx_meeting_type`(`meeting_type` ASC) USING BTREE,
  INDEX `idx_year`(`year` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 621 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '国际奥委会(IOC)历史行政会议表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for olympic_athlete_results
-- ----------------------------
DROP TABLE IF EXISTS `olympic_athlete_results`;
CREATE TABLE `olympic_athlete_results`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '唯一标识符',
  `athlete_id` int NOT NULL COMMENT '运动员ID',
  `games` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '奥运会名称',
  `team` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '代表队代码 (NOC)',
  `discipline` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '运动项目',
  `event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '具体项目',
  `position` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '排名',
  `medal` enum('GOLD','SILVER','BRONZE','-') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '奖牌类型',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_games`(`games` ASC) USING BTREE,
  INDEX `idx_team`(`team` ASC) USING BTREE,
  INDEX `idx_discipline`(`discipline` ASC) USING BTREE,
  INDEX `idx_medal`(`medal` ASC) USING BTREE,
  CONSTRAINT `olympic_athlete_results_ibfk_1` FOREIGN KEY (`athlete_id`) REFERENCES `olympics_athletes_infobox` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 251164 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '奥运成绩表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for olympics_athlete_biographies
-- ----------------------------
DROP TABLE IF EXISTS `olympics_athlete_biographies`;
CREATE TABLE `olympics_athlete_biographies`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '唯一标识符',
  `athlete_id` int NOT NULL COMMENT '运动员ID',
  `passage_id` int NOT NULL COMMENT '段落ID',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文本内容',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_id` ASC) USING BTREE,
  INDEX `idx_passage_id`(`passage_id` ASC) USING BTREE,
  FULLTEXT INDEX `ft_text`(`text`),
  CONSTRAINT `olympics_athlete_biographies_ibfk_1` FOREIGN KEY (`athlete_id`) REFERENCES `olympics_athletes_infobox` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 38455 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '传记文本表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for olympics_athletes_infobox
-- ----------------------------
DROP TABLE IF EXISTS `olympics_athletes_infobox`;
CREATE TABLE `olympics_athletes_infobox`  (
  `id` int NOT NULL COMMENT '唯一标识符',
  `source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据源',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `year_of_birth` int NULL DEFAULT NULL COMMENT '出生年份',
  `country` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '国家/地区',
  `games_participations` int NULL DEFAULT NULL COMMENT '参赛次数',
  `first_olympic_games` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '首次参赛奥运',
  `gender` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '性别 (M/F)',
  `disciplines` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '运动项目（逗号分隔）',
  `gold_count` int NULL DEFAULT 0 COMMENT '金牌数量',
  `silver_count` int NULL DEFAULT 0 COMMENT '银牌数量',
  `bronze_count` int NULL DEFAULT 0 COMMENT '铜牌数量',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE,
  INDEX `idx_country`(`country` ASC) USING BTREE,
  INDEX `idx_gender`(`gender` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '运动员基础信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for organizations
-- ----------------------------
DROP TABLE IF EXISTS `organizations`;
CREATE TABLE `organizations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `org_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `abbreviation` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `founded` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `disbanded` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `recognized_by_ioc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `country_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `country_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `games_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `games_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discipline_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discipline_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sport_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sport_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 394 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for organizations_members
-- ----------------------------
DROP TABLE IF EXISTS `organizations_members`;
CREATE TABLE `organizations_members`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `org_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tenure` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `person_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `country_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `country_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 549 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for organizations_presidents
-- ----------------------------
DROP TABLE IF EXISTS `organizations_presidents`;
CREATE TABLE `organizations_presidents`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `org_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `org_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tenure` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `person_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `person_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `country_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `country_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2774 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for place_names
-- ----------------------------
DROP TABLE IF EXISTS `place_names`;
CREATE TABLE `place_names`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `place_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'Olympedia官方地点ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地点名称',
  `admin_division` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '行政区划/州/省',
  `country_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家全称',
  `country_noc` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '国家代码',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_place_url_id`(`place_url_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 43623 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for place_people_relations
-- ----------------------------
DROP TABLE IF EXISTS `place_people_relations`;
CREATE TABLE `place_people_relations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `place_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联的地名ID',
  `athlete_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联的运动员ID',
  `athlete_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动员姓名',
  `relation_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联类型 (Born here / Died here)',
  `additional_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '原始表中的其他信息(如日期、项目等)',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_place_id`(`place_url_id` ASC) USING BTREE,
  INDEX `idx_athlete_id`(`athlete_url_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 187822 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '地名与人物(出生/去世)关联明细表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for records_archery
-- ----------------------------
DROP TABLE IF EXISTS `records_archery`;
CREATE TABLE `records_archery`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `progression_order` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `performance` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `competitor_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete_url_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `record_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete`(`competitor_name`(100) ASC, `noc`(10) ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 193 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '射箭项目奥运/世界纪录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for records_short_track_speed_skating
-- ----------------------------
DROP TABLE IF EXISTS `records_short_track_speed_skating`;
CREATE TABLE `records_short_track_speed_skating`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `progression_order` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `performance` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `competitor_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete_url_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `record_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete`(`competitor_name`(100) ASC, `noc`(10) ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 120 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '短道速滑项目奥运/世界纪录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for records_ski_jumping
-- ----------------------------
DROP TABLE IF EXISTS `records_ski_jumping`;
CREATE TABLE `records_ski_jumping`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `progression_order` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `performance` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `competitor_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete_url_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `record_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete`(`competitor_name`(100) ASC, `noc`(10) ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 116 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '跳台滑雪项目奥运/世界纪录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for records_speed_skating
-- ----------------------------
DROP TABLE IF EXISTS `records_speed_skating`;
CREATE TABLE `records_speed_skating`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `progression_order` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `performance` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `competitor_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete_url_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `games` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `record_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_athlete`(`competitor_name`(100) ASC, `noc`(10) ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 313 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '速度滑冰项目奥运/世界纪录表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_events
-- ----------------------------
DROP TABLE IF EXISTS `sport_events`;
CREATE TABLE `sport_events`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sport_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `times_held` int NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1686 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_group_events
-- ----------------------------
DROP TABLE IF EXISTS `sport_group_events`;
CREATE TABLE `sport_group_events`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `group` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `group_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discipline` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discipline_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `event_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `times_held` int NULL DEFAULT NULL,
  `url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3371 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_group_medals
-- ----------------------------
DROP TABLE IF EXISTS `sport_group_medals`;
CREATE TABLE `sport_group_medals`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `group` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `group_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gold` int NULL DEFAULT NULL,
  `silver` int NULL DEFAULT NULL,
  `bronze` int NULL DEFAULT NULL,
  `total` int NULL DEFAULT NULL,
  `url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2819 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_group_top_athletes
-- ----------------------------
DROP TABLE IF EXISTS `sport_group_top_athletes`;
CREATE TABLE `sport_group_top_athletes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `group` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `group_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nation_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gold` int NULL DEFAULT NULL,
  `silver` int NULL DEFAULT NULL,
  `bronze` int NULL DEFAULT NULL,
  `total` int NULL DEFAULT NULL,
  `url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1266 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_groups
-- ----------------------------
DROP TABLE IF EXISTS `sport_groups`;
CREATE TABLE `sport_groups`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `disciplines` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `participants` int NULL DEFAULT NULL,
  `nocs` int NULL DEFAULT NULL,
  `competitions_held` int NULL DEFAULT NULL,
  `distinct_events` int NULL DEFAULT NULL,
  `if_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `if_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 169 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_medals
-- ----------------------------
DROP TABLE IF EXISTS `sport_medals`;
CREATE TABLE `sport_medals`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sport_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `noc_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gold` int NULL DEFAULT NULL,
  `silver` int NULL DEFAULT NULL,
  `bronze` int NULL DEFAULT NULL,
  `total` int NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2102 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sport_top_athletes
-- ----------------------------
DROP TABLE IF EXISTS `sport_top_athletes`;
CREATE TABLE `sport_top_athletes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sport_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `athlete_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nation_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gold` int NULL DEFAULT NULL,
  `silver` int NULL DEFAULT NULL,
  `bronze` int NULL DEFAULT NULL,
  `total` int NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1398 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sports
-- ----------------------------
DROP TABLE IF EXISTS `sports`;
CREATE TABLE `sports`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `discipline_of` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `group_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `participants` int NULL DEFAULT NULL,
  `nocs` int NULL DEFAULT NULL,
  `competitions_held` int NULL DEFAULT NULL,
  `distinct_events` int NULL DEFAULT NULL,
  `if_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `if_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 133 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for venue_events_relations
-- ----------------------------
DROP TABLE IF EXISTS `venue_events_relations`;
CREATE TABLE `venue_events_relations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `venue_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联的场馆ID',
  `games_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '所属奥运会(如 2012 Summer Olympics)',
  `games_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '奥运会ID',
  `sport` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运动大项(如 Archery)',
  `event` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛小项(如 Team, Men)',
  `event_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛小项ID',
  `held_dates` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '比赛举办日期',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_venue_id`(`venue_url_id` ASC) USING BTREE,
  INDEX `idx_games_id`(`games_url_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10816 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '场馆与承办赛事关联表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for venues
-- ----------------------------
DROP TABLE IF EXISTS `venues`;
CREATE TABLE `venues`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `venue_url_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'Olympedia场馆ID',
  `venue_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '场馆名称',
  `place` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '地点/城市',
  `coordinates` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '经纬度坐标',
  `opened` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '开放年份',
  `capacity` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '场馆容量',
  `venue_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '场馆类型(室内/室外等)',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_venue_url_id`(`venue_url_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1247 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'Olympedia比赛场馆基础表' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
