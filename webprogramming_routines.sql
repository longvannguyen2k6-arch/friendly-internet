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
-- Temporary view structure for view `account_details`
--

DROP TABLE IF EXISTS `account_details`;
/*!50001 DROP VIEW IF EXISTS `account_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `account_details` AS SELECT 
 1 AS `account_id`,
 1 AS `username`,
 1 AS `account_email`,
 1 AS `membership_id`,
 1 AS `full_name`,
 1 AS `age`,
 1 AS `provider`,
 1 AS `type_of_plan`,
 1 AS `data_label`,
 1 AS `calls_texts`,
 1 AS `phone`,
 1 AS `price_per_month`,
 1 AS `spend_cap`,
 1 AS `age_restricted`,
 1 AS `status_of_account`,
 1 AS `account_created`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `recommended_plans`
--

DROP TABLE IF EXISTS `recommended_plans`;
/*!50001 DROP VIEW IF EXISTS `recommended_plans`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `recommended_plans` AS SELECT 
 1 AS `plan_id`,
 1 AS `provider`,
 1 AS `type_of_plan`,
 1 AS `plans_type`,
 1 AS `data_label`,
 1 AS `data_gb`,
 1 AS `unlimited`,
 1 AS `calls_texts`,
 1 AS `phone`,
 1 AS `price_per_month`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `plans_available`
--

DROP TABLE IF EXISTS `plans_available`;
/*!50001 DROP VIEW IF EXISTS `plans_available`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `plans_available` AS SELECT 
 1 AS `plan_id`,
 1 AS `provider`,
 1 AS `type_of_plan`,
 1 AS `data_label`,
 1 AS `data_gb`,
 1 AS `unlimited`,
 1 AS `calls_texts`,
 1 AS `phone`,
 1 AS `price_per_month`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `membership_details`
--

DROP TABLE IF EXISTS `membership_details`;
/*!50001 DROP VIEW IF EXISTS `membership_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `membership_details` AS SELECT 
 1 AS `membership_id`,
 1 AS `full_name`,
 1 AS `email`,
 1 AS `age`,
 1 AS `provider`,
 1 AS `type_of_plan`,
 1 AS `data_label`,
 1 AS `data_gb`,
 1 AS `calls_texts`,
 1 AS `phone`,
 1 AS `price_per_month`,
 1 AS `spend_cap`,
 1 AS `age_restricted`,
 1 AS `created`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `account_details`
--

/*!50001 DROP VIEW IF EXISTS `account_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `account_details` AS select `accounts`.`account_id` AS `account_id`,`accounts`.`username` AS `username`,`accounts`.`email` AS `account_email`,`accounts`.`membership_id` AS `membership_id`,`memberships`.`full_name` AS `full_name`,`memberships`.`age` AS `age`,`plans`.`provider` AS `provider`,`plans`.`type_of_plan` AS `type_of_plan`,`plans`.`data_label` AS `data_label`,`plans`.`calls_texts` AS `calls_texts`,`plans`.`phone` AS `phone`,`plans`.`price_per_month` AS `price_per_month`,`memberships`.`spend_cap` AS `spend_cap`,`memberships`.`age_restricted` AS `age_restricted`,`accounts`.`status_of_account` AS `status_of_account`,`accounts`.`created` AS `account_created` from ((`accounts` left join `memberships` on((`accounts`.`membership_id` = `memberships`.`membership_id`))) left join `plans` on((`memberships`.`plan_id` = `plans`.`plan_ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recommended_plans`
--

/*!50001 DROP VIEW IF EXISTS `recommended_plans`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recommended_plans` AS select `plans`.`plan_ID` AS `plan_id`,`plans`.`provider` AS `provider`,`plans`.`type_of_plan` AS `type_of_plan`,(case when (`plans`.`type_of_plan` = 'Just phone') then 'Phone only' when (`plans`.`type_of_plan` = 'All-in') then 'Phone with a mobile plan' else 'only SIM ' end) AS `plans_type`,`plans`.`data_label` AS `data_label`,`plans`.`data_gb` AS `data_gb`,`plans`.`unlimited` AS `unlimited`,`plans`.`calls_texts` AS `calls_texts`,`plans`.`phone` AS `phone`,`plans`.`price_per_month` AS `price_per_month` from `plans` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `plans_available`
--

/*!50001 DROP VIEW IF EXISTS `plans_available`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `plans_available` AS select `plans`.`plan_ID` AS `plan_id`,`plans`.`provider` AS `provider`,`plans`.`type_of_plan` AS `type_of_plan`,coalesce(`plans`.`data_label`,'No data included') AS `data_label`,`plans`.`data_gb` AS `data_gb`,`plans`.`unlimited` AS `unlimited`,coalesce(`plans`.`calls_texts`,'No calls/texts included') AS `calls_texts`,coalesce(`plans`.`phone`,'No phone included') AS `phone`,`plans`.`price_per_month` AS `price_per_month` from `plans` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `membership_details`
--

/*!50001 DROP VIEW IF EXISTS `membership_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `membership_details` AS select `memberships`.`membership_id` AS `membership_id`,`memberships`.`full_name` AS `full_name`,`memberships`.`email` AS `email`,`memberships`.`age` AS `age`,`plans`.`provider` AS `provider`,`plans`.`type_of_plan` AS `type_of_plan`,`plans`.`data_label` AS `data_label`,`plans`.`data_gb` AS `data_gb`,`plans`.`calls_texts` AS `calls_texts`,`plans`.`phone` AS `phone`,`plans`.`price_per_month` AS `price_per_month`,`memberships`.`spend_cap` AS `spend_cap`,`memberships`.`age_restricted` AS `age_restricted`,`memberships`.`created` AS `created` from (`memberships` join `plans` on((`memberships`.`plan_id` = `plans`.`plan_ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-10 14:26:30
