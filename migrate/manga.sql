DROP TABLE IF EXISTS `chapter`;
CREATE TABLE `chapter`  (
  `chapterId` int NOT NULL AUTO_INCREMENT,
  `mangaId` int NULL DEFAULT NULL,
  `page` int NULL DEFAULT NULL,
  `status` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`chapterId`) USING BTREE
);
DROP TABLE IF EXISTS `chapter_image`;
CREATE TABLE `chapter_image`  (
  `imageId` int NOT NULL AUTO_INCREMENT,
  `chapterId` int NULL DEFAULT NULL,
  `image` varchar(255) NULL DEFAULT NULL,
  PRIMARY KEY (`imageId`) USING BTREE
);
DROP TABLE IF EXISTS `data`;
CREATE TABLE `data`  (
  `mangaId` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255)NULL DEFAULT NULL,
  `logo` text NULL,
  `description` text NULL,
  `genres` varchar(255)NULL DEFAULT NULL,
  `link` text NULL,
  `index` int NULL DEFAULT NULL,
  `status` int NULL DEFAULT 0,
  `updated` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
  `last` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`mangaId`) USING BTREE
);
DROP TABLE IF EXISTS `queued`;
CREATE TABLE `queued`  (
  `queuedId` int NOT NULL AUTO_INCREMENT,
  `mangaId` int NULL DEFAULT NULL,
  `link` text NULL,
  `status` int NULL DEFAULT 0,
  PRIMARY KEY (`queuedId`) USING BTREE
);
DROP VIEW IF EXISTS `v_manga`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_manga` AS select `m`.`mangaId` AS `mangaId`,`m`.`name` AS `name`,`m`.`logo` AS `logo`,`m`.`description` AS `description`,`m`.`genres` AS `genres`,`m`.`link` AS `link`,`m`.`index` AS `index`,`m`.`status` AS `status`,`m`.`updated` AS `updated`,`m`.`last` AS `last`,(select count(`c`.`chapterId`) from `chapter` `c` where (`c`.`mangaId` = `m`.`mangaId`)) AS `total` from `data` `m` where `m`.`mangaId` in (select `chapter`.`mangaId` from `chapter`) order by `m`.`updated` desc;
SET FOREIGN_KEY_CHECKS = 1;