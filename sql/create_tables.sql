CREATE SCHEMA IF NOT EXISTS `grades` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE grades;

DROP TABLE IF EXISTS `preparse`;
CREATE TABLE IF NOT EXISTS `preparse`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `prof` VARCHAR(75) NOT NULL,
    `school` VARCHAR(100) NOT NULL,
    `helpfulness` INT(2) NOT NULL,
    `clarity` INT(2) NOT NULL,
    `easiness` INT(2) NOT NULL,
    `comment` VARCHAR(4000) NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `postparse`;
CREATE TABLE IF NOT EXISTS `postparse`(
    `id` INT(10) UNSIGNED NOT NULL,
    `prof` VARCHAR(50) NOT NULL,
    `school` VARCHAR(50) NOT NULL,
    `helpfulness` INT(2) NOT NULL,
    `clarity` INT(2) NOT NULL,
    `easiness` INT(2) NOT NULL,
    `sentiment` INT(3) NOT NULL,
    `overall` INT(3) NOT NULL,
    PRIMARY KEY (`id`)
);
