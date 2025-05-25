-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: warehousedatabase
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `sup_ID` int NOT NULL,
  `description` text,
  PRIMARY KEY (`ID`),
  KEY `sup_ID` (`sup_ID`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`sup_ID`) REFERENCES `supplier` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,1,'Telephone'),(2,2,'EX30'),(3,2,'XC60'),(4,2,'V60'),(5,3,'Key'),(6,1,'Software'),(7,1,'5G'),(8,5,'Table'),(9,5,'Chair'),(10,5,'Meatballs'),(11,5,'Blåhaj'),(12,6,'Rabies'),(13,6,'Trash'),(14,3,'Half-Life 3');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock`
--

DROP TABLE IF EXISTS `stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `prod_ID` int NOT NULL,
  `WH_ID` int NOT NULL,
  `minQuantity` int NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `prod_wh_key` (`prod_ID`,`WH_ID`),
  KEY `WH_ID` (`WH_ID`),
  CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`prod_ID`) REFERENCES `product` (`ID`),
  CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`WH_ID`) REFERENCES `warehouse` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock`
--

LOCK TABLES `stock` WRITE;
/*!40000 ALTER TABLE `stock` DISABLE KEYS */;
INSERT INTO `stock` VALUES (1,450,1,1,100),(2,999,6,1,1000),(3,4264,6,5,1000),(4,4,7,1,5),(5,9999999,7,3,100),(6,99999,7,4,70),(7,30,7,5,50),(8,4842,6,3,100000),(9,50,1,6,420),(10,6,1,4,999994),(11,0,3,5,500),(12,749,3,6,750),(13,80,3,1,10),(14,123456,12,4,0),(15,77777,12,3,1),(16,75766,13,4,99999),(17,99998,13,3,99999),(18,5,11,5,0),(19,8999,11,6,9999),(20,540,11,3,999),(21,1000,1,3,500),(22,200,2,3,100),(23,36,2,1,20),(24,101,2,4,80),(25,20,10,3,10),(26,10,10,6,20);
/*!40000 ALTER TABLE `stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `address` text NOT NULL,
  `contact` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (1,'Ericsson','+46722185976'),(2,'Volvo Cars','volvo.cars@email.de'),(3,'Steam Software','gaben@valvesoftware.com'),(4,'Fortum','Carrier Pigeon'),(5,'IKEA','+46752345056'),(6,'Raccoon','Any Trashcan');
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `torestock`
--

DROP TABLE IF EXISTS `torestock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `torestock` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `stock_ID` int NOT NULL,
  `dateAdded` datetime NOT NULL,
  `dateOrdered` datetime DEFAULT NULL,
  `orderCount` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `stock_ID` (`stock_ID`),
  CONSTRAINT `torestock_ibfk_1` FOREIGN KEY (`stock_ID`) REFERENCES `stock` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `torestock`
--

LOCK TABLES `torestock` WRITE;
/*!40000 ALTER TABLE `torestock` DISABLE KEYS */;
INSERT INTO `torestock` VALUES (1,2,'2024-09-04 00:00:00',NULL,NULL),(2,4,'2025-01-24 00:00:00',NULL,NULL),(3,7,'2025-04-01 00:00:00',NULL,NULL),(4,8,'2023-12-31 00:00:00',NULL,NULL),(5,9,'2025-05-25 14:30:36',NULL,NULL),(6,10,'2022-08-09 00:00:00',NULL,NULL),(7,11,'2025-05-25 14:30:36',NULL,NULL),(8,12,'2025-05-25 14:30:36',NULL,NULL),(9,16,'2025-04-01 00:00:00',NULL,NULL),(10,17,'2025-05-25 14:30:36',NULL,NULL),(11,19,'2025-05-25 14:30:36',NULL,NULL),(12,20,'2025-05-23 00:00:00',NULL,NULL),(13,26,'2020-10-15 00:00:00',NULL,NULL),(14,2,'2022-05-03 00:00:00','2023-12-04 00:00:00',100),(15,10,'2020-11-01 00:00:00','2021-12-01 00:00:00',400),(16,3,'2023-10-02 00:00:00','2023-10-14 00:00:00',2000),(17,7,'2023-10-02 00:00:00','2023-10-14 00:00:00',2),(18,1,'2020-01-01 00:00:00','2025-04-13 00:00:00',600),(19,18,'2023-10-20 00:00:00','2023-12-23 00:00:00',8),(20,18,'2023-12-25 00:00:00','2024-12-20 00:00:00',90),(21,19,'2019-02-19 00:00:00','2019-02-21 00:00:00',1),(22,19,'2019-02-22 00:00:00','2019-02-23 00:00:00',1500),(23,19,'2019-02-24 00:00:00','2020-06-02 00:00:00',9999),(24,19,'2024-08-17 00:00:00','2024-08-20 00:00:00',300),(25,8,'2021-07-30 00:00:00','2021-08-07 00:00:00',100),(26,20,'2023-10-22 00:00:00','2023-10-22 00:00:00',12);
/*!40000 ALTER TABLE `torestock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse`
--

DROP TABLE IF EXISTS `warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `address` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse`
--

LOCK TABLES `warehouse` WRITE;
/*!40000 ALTER TABLE `warehouse` DISABLE KEYS */;
INSERT INTO `warehouse` VALUES (1,'Karlskrona'),(2,'Karlshamn'),(3,'Stockholm North'),(4,'Stockholm West'),(5,'Malmö'),(6,'Gothenburg');
/*!40000 ALTER TABLE `warehouse` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-25 14:41:05
