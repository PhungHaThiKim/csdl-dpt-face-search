-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: csdl_dpt_search_img
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP DATABASE IF EXISTS csdl_dpt_search_img;
CREATE DATABASE csdl_dpt_search_img CHARACTER SET utf8 COLLATE utf8_general_ci;
USE csdl_dpt_search_img;

--
-- Table structure for table `face`
--

DROP TABLE IF EXISTS `face`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `face` (
  `face_id` int NOT NULL AUTO_INCREMENT,
  `face_path` varchar(255) DEFAULT NULL,
  `frame_id` int NOT NULL,
  PRIMARY KEY (`face_id`),
  KEY `frame_fk1_idx` (`frame_id`),
  CONSTRAINT `frame_fk1` FOREIGN KEY (`frame_id`) REFERENCES `frame` (`frame_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `frame`
--

DROP TABLE IF EXISTS `frame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frame` (
  `frame_id` int NOT NULL AUTO_INCREMENT,
  `frame_path` varchar(255) DEFAULT NULL,
  `frame_short_pos_start` int NOT NULL,
  `frame_short_pos_end` int NOT NULL,
  `frame_short_fps` int NOT NULL,
  `video_id` int NOT NULL,
  PRIMARY KEY (`frame_id`),
  KEY `video_fk1_idx` (`video_id`),
  CONSTRAINT `video_fk1` FOREIGN KEY (`video_id`) REFERENCES `video` (`video_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lbp_feature`
--

DROP TABLE IF EXISTS `lbp_feature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lbp_feature` (
  `lbp_feature_id` int NOT NULL AUTO_INCREMENT,
  `lbp_feature_path` varchar(255) DEFAULT NULL,
  `face_id` int NOT NULL,
  PRIMARY KEY (`lbp_feature_id`),
  UNIQUE KEY `face_id_UNIQUE` (`face_id`),
  CONSTRAINT `face_fk2` FOREIGN KEY (`face_id`) REFERENCES `face` (`face_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sift_feature`
--

DROP TABLE IF EXISTS `sift_feature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sift_feature` (
  `sift_feature_id` int NOT NULL AUTO_INCREMENT,
  `sift_feature_path` varchar(255) DEFAULT NULL,
  `face_id` int NOT NULL,
  PRIMARY KEY (`sift_feature_id`),
  UNIQUE KEY `face_id_UNIQUE` (`face_id`),
  KEY `face_fk1_idx` (`face_id`),
  CONSTRAINT `face_fk1` FOREIGN KEY (`face_id`) REFERENCES `face` (`face_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video` (
  `video_id` int NOT NULL AUTO_INCREMENT,
  `video_folder` varchar(255) DEFAULT NULL,
  `video_path` varchar(255) DEFAULT NULL,
  `video_datetime` datetime NOT NULL,
  `video_des` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`video_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-21 19:58:12
