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

DROP TABLE IF EXISTS `plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plans` (
  `plan_ID` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(50) NOT NULL,
  `type_of_plan` varchar(50) NOT NULL,
  `data_label` varchar(20) DEFAULT NULL,
  `data_gb` decimal(6,2) DEFAULT NULL,
  `unlimited` tinyint(1) DEFAULT '0',
  `calls_texts` varchar(20) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `price_per_month` decimal(6,2) NOT NULL,
  PRIMARY KEY (`plan_ID`),
  KEY `idx_plan_search` (`provider`,`type_of_plan`,`phone`,`price_per_month`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `plans` WRITE;
/*!40000 ALTER TABLE `plans` DISABLE KEYS */;
INSERT INTO `plans` VALUES (1,'Fone','Super saver','0.5 GB',0.50,0,'500/500',NULL,8.00),(2,'Fone','Saver','1 GB',1.00,0,'750/750',NULL,11.00),(3,'Fone','Average','4 GB',4.00,0,'unl/unl',NULL,16.00),(4,'Fone','Regular','8 GB',8.00,0,'unl/unl',NULL,19.00),(5,'Fone','Spender','100 GB',100.00,0,'unl/unl',NULL,29.00),(6,'Fone','All-in','100 GB',100.00,0,'unl/unl','iPhone 14 Pro',75.00),(7,'Fone','All-in','100 GB',100.00,0,'unl/unl','iPhone 14',60.00),(8,'Fone','All-in','100 GB',100.00,0,'unl/unl','iPhone 13',55.00),(9,'Fone','All-in','100 GB',100.00,0,'unl/unl','Samsung S22',75.00),(10,'Fone','All-in','100 GB',100.00,0,'unl/unl','Samsung S21',52.00),(11,'Fone','Just phone',NULL,NULL,0,NULL,'iPhone 14 Pro',55.00),(12,'Fone','Just phone',NULL,NULL,0,NULL,'iPhone 14',40.00),(13,'Fone','Just phone',NULL,NULL,0,NULL,'iPhone 13',35.00),(14,'Fone','Just phone',NULL,NULL,0,NULL,'Samsung S22',55.00),(15,'Fone','Just phone',NULL,NULL,0,NULL,'Samsung S21',32.00),(16,'Gap','Super saver','1 GB',1.00,0,'unl/unl',NULL,10.00),(17,'Gap','Saver','2 GB',2.00,0,'unl/unl',NULL,14.00),(18,'Gap','Average','5 GB',5.00,0,'unl/unl',NULL,19.00),(19,'Gap','Regular','10 GB',10.00,0,'unl/unl',NULL,25.00),(20,'Gap','Spender','unl GB',999.00,1,'unl/unl',NULL,32.00),(21,'Gap','All-in','unl GB',999.00,1,'unl/unl','iPhone 14 Pro',79.00),(22,'Gap','All-in','unl GB',999.00,1,'unl/unl','iPhone 14',55.00),(23,'Gap','All-in','unl GB',999.00,1,'unl/unl','iPhone 13',50.00),(24,'Gap','All-in','unl GB',999.00,1,'unl/unl','Samsung S22',72.00),(25,'Gap','All-in','unl GB',999.00,1,'unl/unl','Samsung S21',50.00),(26,'Gap','Just phone',NULL,NULL,0,NULL,'iPhone 14 Pro',59.00),(27,'Gap','Just phone',NULL,NULL,0,NULL,'iPhone 14',42.00),(28,'Gap','Just phone',NULL,NULL,0,NULL,'iPhone 13',37.00),(29,'Gap','Just phone',NULL,NULL,0,NULL,'Samsung S22',57.00),(30,'Gap','Just phone',NULL,NULL,0,NULL,'Samsung S21',30.00),(31,'Flipper','Super saver','1 GB',1.00,0,'500/500',NULL,6.00),(32,'Flipper','Saver','2 GB',2.00,0,'750/750',NULL,8.00),(33,'Flipper','Average','3 GB',3.00,0,'unl/unl',NULL,10.00),(34,'Flipper','Regular','6 GB',6.00,0,'unl/unl',NULL,15.00),(35,'Flipper','Spender','35 GB',35.00,0,'unl/unl',NULL,22.00),(36,'Flipper','All-in','35 GB',35.00,0,'unl/unl','iPhone 14 Pro',70.00),(37,'Flipper','All-in','35 GB',35.00,0,'unl/unl','iPhone 14',58.00),(38,'Flipper','All-in','35 GB',35.00,0,'unl/unl','iPhone 13',49.00),(39,'Flipper','All-in','35 GB',35.00,0,'unl/unl','Samsung S22',70.00),(40,'Flipper','All-in','35 GB',35.00,0,'unl/unl','Samsung S21',48.00),(41,'Flipper','Just phone',NULL,NULL,0,NULL,'iPhone 14 Pro',60.00),(42,'Flipper','Just phone',NULL,NULL,0,NULL,'iPhone 14',39.00),(43,'Flipper','Just phone',NULL,NULL,0,NULL,'iPhone 13',29.00),(44,'Flipper','Just phone',NULL,NULL,0,NULL,'Samsung S22',50.00),(45,'Flipper','Just phone',NULL,NULL,0,NULL,'Samsung S21',35.00);
/*!40000 ALTER TABLE `plans` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
