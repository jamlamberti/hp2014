CREATE SCHEMA IF NOT EXISTS `grades` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE grades;
DROP TABLE IF EXISTS `members`;
CREATE TABLE IF NOT EXISTS `members`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(45) NOT NULL,
    `salt` VARCHAR(40) NOT NULL,
    `hashs` VARCHAR(300) NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `preparse`;
CREATE TABLE IF NOT EXISTS `preparse`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `prof` VARCHAR(75) NOT NULL,
    `school` VARCHAR(100) NOT NULL,
    `helpfulness` INT(2) NOT NULL,
    `clarity` INT(2) NOT NULL,
    `easiness` INT(2) NOT NULL,
    -- `comment` VARCHAR(4000) NOT NULL,
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

DROP TABLE IF EXISTS `comments`;
CREATE TABLE IF NOT EXISTS `comments`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `uid` INT(10) UNSIGNED NOT NULL,
    `comment` VARCHAR(4000) NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `profClusters`;
CREATE TABLE IF NOT EXISTS `profClusters`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `uid` INT(10) UNSIGNED NOT NULL,
    `cid` INT(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `studentClusters`;
CREATE TABLE IF NOT EXISTS `studentClusters`(
    `id` INT(10) UNSIGNED NOT NULL,
    `sid` INT(10) UNSIGNED NOT NULL,
    `cid` INT(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `crn` INT(10) NOT NULL,
    `course` VARCHAR(10) NOT NULL,
    `title` VARCHAR(75) NOT NULL,
    `dist` VARCHAR(10) NOT NULL,
    `sect` VARCHAR(10) NOT NULL,
    `days` VARCHAR(10) NOT NULL,
    `time` VARCHAR(25) NOT NULL,
    `prof` VARCHAR(50),
    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `students`;
CREATE TABLE IF NOT EXISTS `students`(
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `sid` INT(10) UNSIGNED NOT NULL,
    `crn` INT(10) UNSIGNED NOT NULL,
    `rating` INT(50) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
);


