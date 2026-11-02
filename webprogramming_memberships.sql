-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: webprogramming
-- ------------------------------------------------------
-- Server version	8.0.45

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

--
-- Table structure for table `memberships`
--

DROP TABLE IF EXISTS `memberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memberships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `membership_id` varchar(30) NOT NULL,
  `full_name` varchar(70) NOT NULL,
  `email` varchar(100) NOT NULL,
  `age` int NOT NULL,
  `plan_id` int NOT NULL,
  `spend_cap` decimal(7,2) DEFAULT NULL,
  `age_restricted` tinyint(1) DEFAULT '0',
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `phone_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `memebership_id` (`membership_id`),
  KEY `plan_id` (`plan_id`),
  KEY `idx_membership_id` (`membership_id`),
  CONSTRAINT `memberships_ibfk_1` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`plan_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memberships`
--

LOCK TABLES `memberships` WRITE;
/*!40000 ALTER TABLE `memberships` DISABLE KEYS */;
INSERT INTO `memberships` VALUES (1,'FI-0001','Ola Eze','olaze9@email.com',16,32,10.00,1,'2026-06-08 10:23:14',NULL),(2,'FI-0002','Ibrahim Isah','ibrahimisah@email.com',22,18,NULL,0,'2026-06-08 11:05:18',NULL),(3,'FI-1374','Friendly Customer','customer@friendly.uk',20,16,0.00,0,NULL,NULL),(4,'FI-5823','Friendly Customer','customer@friendly.uk',20,16,0.00,0,NULL,NULL),(5,'FI-1804','Friendly Customer','customer@friendly.uk',20,16,0.00,0,NULL,NULL),(6,'FI-8280','Friendly Customer','customer@friendly.uk',20,2,0.00,0,NULL,NULL),(7,'FI-9577','Friendly Customer','customer@friendly.uk',20,2,0.00,0,NULL,NULL),(8,'FI-4242','Friendly Customer','customer@friendly.uk',20,3,0.00,0,NULL,NULL),(9,'FI-2699','Friendly Customer','customer@friendly.uk',20,24,0.00,0,NULL,NULL),(10,'FI-3949','Friendly Customer','customer@friendly.uk',20,24,0.00,0,NULL,NULL),(11,'FI-9486','Friendly Customer','customer@friendly.uk',14,3,10.00,1,NULL,NULL),(12,'FI-4507','Friendly Customer','customer@friendly.uk',14,17,10.00,1,NULL,NULL),(13,'FI-5058','conmuondingu','conmuondingu@gmail.com',43,8,55.00,0,NULL,NULL),(14,'FI-3147','longdepzaii','longdepzaii@gmail.com',18,3,16.00,0,NULL,NULL),(15,'FI-4832','longdepzaii','longdepzaii@gmail.com',18,16,10.00,0,NULL,'+447412895989'),(16,'FI-8971','JOHNson222','johnson223@gmail.com',23,36,70.00,0,NULL,'047374343'),(17,'FI-9902','longdepzaii','longdepzaii@gmail.com',18,17,14.00,0,NULL,'+447412895989'),(18,'FI-7855','caubedepda','caubedepdaa12@gmail.com',23,5,29.00,0,NULL,'039884033'),(19,'FI-7666','johnn','johnn@gmail.com',23,18,19.00,0,NULL,'0823743554'),(20,'FI-1537','johnn','johnn@gmail.com',23,3,16.00,0,NULL,'0823743554');
/*!40000 ALTER TABLE `memberships` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-10 14:26:30
