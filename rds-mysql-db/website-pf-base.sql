CREATE DATABASE  IF NOT EXISTS `website_pf`;
USE `website_pf`;

DROP TABLE IF EXISTS `author`;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `display_name` varchar(255) DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_name` varchar(255) DEFAULT NULL,
  `post_url` varchar(255) DEFAULT NULL,
  `post_s3_path` varchar(1000) DEFAULT NULL,
  `post_html_path` varchar(1000) DEFAULT NULL,
  `primary_image_path` varchar(1000) DEFAULT NULL,
  `thumbnail_image_path` varchar(1000) DEFAULT NULL,
  `post_summary` varchar(255) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `post_view_count` int(11) DEFAULT '0',
  `meta` json DEFAULT NULL,
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `POST_URL` (`post_url`),
  KEY `AUTHOR_idx` (`author_id`),
  CONSTRAINT `AUTHOR` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
