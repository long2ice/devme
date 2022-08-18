-- upgrade --
CREATE TABLE IF NOT EXISTS `gitprovider` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL,
    `type` VARCHAR(6) NOT NULL  COMMENT 'github: github\ngitlab: gitlab' DEFAULT 'github',
    `token` VARCHAR(200) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    UNIQUE KEY `uid_gitprovider_type_01a321` (`type`, `token`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `project` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `url` VARCHAR(200) NOT NULL,
    `framework` VARCHAR(14) NOT NULL  COMMENT 'nodejs: nodejs\nhtml: html\ndocker: docker\ndocker_compose: docker-compose',
    `image` VARCHAR(200),
    `root` VARCHAR(50),
    `deployment` JSON,
    `env` JSON,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `git_provider_id` INT,
    CONSTRAINT `fk_project_gitprovi_917ddb92` FOREIGN KEY (`git_provider_id`) REFERENCES `gitprovider` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `deploy` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `branch` VARCHAR(200) NOT NULL  DEFAULT 'main',
    `log` LONGTEXT,
    `status` VARCHAR(8) NOT NULL  COMMENT 'running: running\nsuccess: success\nfailed: failed\ncanceled: canceled',
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `project_id` INT NOT NULL,
    CONSTRAINT `fk_deploy_project_675c6512` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `domain` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `domain` VARCHAR(200) NOT NULL UNIQUE,
    `branch` VARCHAR(200) NOT NULL  DEFAULT 'main',
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `project_id` INT NOT NULL,
    CONSTRAINT `fk_domain_project_d0c82727` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
