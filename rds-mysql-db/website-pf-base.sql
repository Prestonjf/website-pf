CREATE DATABASE  IF NOT EXISTS `website_pf` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `website_pf`;

DROP TABLE IF EXISTS `author`;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_s3_path` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_html_path` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `primary_image_path` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_summary` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `post_view_count` int(11) DEFAULT '0',
  `meta` json DEFAULT NULL,
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `POST_URL` (`post_url`),
  KEY `AUTHOR_idx` (`author_id`),
  CONSTRAINT `AUTHOR` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;