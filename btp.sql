-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: btp
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `env_attributes`
--

DROP TABLE IF EXISTS `env_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `env_attributes` (
  `env_attribute_id` int NOT NULL AUTO_INCREMENT,
  `env_attribute` varchar(64) NOT NULL,
  PRIMARY KEY (`env_attribute_id`),
  UNIQUE KEY `env_attribute` (`env_attribute`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `env_attributes`
--

LOCK TABLES `env_attributes` WRITE;
/*!40000 ALTER TABLE `env_attributes` DISABLE KEYS */;
INSERT INTO `env_attributes` VALUES (2,'office_hours'),(3,'otp_required'),(1,'weekday');
/*!40000 ALTER TABLE `env_attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `env_aval`
--

DROP TABLE IF EXISTS `env_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `env_aval` (
  `env_attribute_id` int NOT NULL,
  `env_val` varchar(64) NOT NULL,
  PRIMARY KEY (`env_attribute_id`,`env_val`),
  CONSTRAINT `env_aval_ibfk_1` FOREIGN KEY (`env_attribute_id`) REFERENCES `env_attributes` (`env_attribute_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `env_aval`
--

LOCK TABLES `env_aval` WRITE;
/*!40000 ALTER TABLE `env_aval` DISABLE KEYS */;
INSERT INTO `env_aval` VALUES (1,'0'),(1,'1'),(2,'0'),(2,'1'),(3,'0'),(3,'1');
/*!40000 ALTER TABLE `env_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs` (
  `log_no` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `org_id` int NOT NULL,
  `resource_id` int NOT NULL,
  `operation_id` int DEFAULT NULL,
  `decision` varchar(1) NOT NULL,
  PRIMARY KEY (`log_no`),
  KEY `logs_ibfk_4` (`operation_id`),
  KEY `logs_ibfk_1` (`user_id`),
  KEY `logs_ibfk_2` (`org_id`),
  KEY `logs_ibfk_3` (`resource_id`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `logs_ibfk_2` FOREIGN KEY (`org_id`) REFERENCES `org` (`org_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `logs_ibfk_3` FOREIGN KEY (`resource_id`) REFERENCES `resource` (`resource_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `logs_ibfk_4` FOREIGN KEY (`operation_id`) REFERENCES `operations` (`operation_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `logs_chk_1` CHECK ((`decision` in (_utf8mb4'y',_utf8mb4'n')))
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_env`
--

DROP TABLE IF EXISTS `logs_env`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_env` (
  `log_no` int NOT NULL,
  `env_attribute_id` int NOT NULL,
  `env_val` varchar(64) NOT NULL,
  PRIMARY KEY (`log_no`,`env_attribute_id`),
  KEY `env_attribute_id` (`env_attribute_id`,`env_val`),
  CONSTRAINT `logs_env_ibfk_1` FOREIGN KEY (`env_attribute_id`, `env_val`) REFERENCES `env_aval` (`env_attribute_id`, `env_val`),
  CONSTRAINT `logs_env_ibfk_2` FOREIGN KEY (`log_no`) REFERENCES `logs` (`log_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_env`
--

LOCK TABLES `logs_env` WRITE;
/*!40000 ALTER TABLE `logs_env` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs_env` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_user_aval`
--

DROP TABLE IF EXISTS `logs_user_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_user_aval` (
  `log_no` int NOT NULL,
  `user_attribute_id` int NOT NULL,
  `user_val` varchar(64) NOT NULL,
  PRIMARY KEY (`log_no`,`user_attribute_id`),
  KEY `logs_user_aval_ibfk_1` (`user_attribute_id`,`user_val`),
  CONSTRAINT `logs_user_aval_ibfk_1` FOREIGN KEY (`user_attribute_id`, `user_val`) REFERENCES `user_aval` (`user_attribute_id`, `user_val`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `logs_user_aval_ibfk_2` FOREIGN KEY (`log_no`) REFERENCES `logs` (`log_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_user_aval`
--

LOCK TABLES `logs_user_aval` WRITE;
/*!40000 ALTER TABLE `logs_user_aval` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs_user_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operations`
--

DROP TABLE IF EXISTS `operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operations` (
  `operation_id` int NOT NULL AUTO_INCREMENT,
  `operation_name` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`operation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operations`
--

LOCK TABLES `operations` WRITE;
/*!40000 ALTER TABLE `operations` DISABLE KEYS */;
INSERT INTO `operations` VALUES (1,'read'),(2,'write'),(3,'append');
/*!40000 ALTER TABLE `operations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `org`
--

DROP TABLE IF EXISTS `org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `org` (
  `org_id` int NOT NULL AUTO_INCREMENT,
  `org_name` varchar(64) NOT NULL,
  `public_key` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`org_id`),
  UNIQUE KEY `org_name` (`org_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `org`
--

LOCK TABLES `org` WRITE;
/*!40000 ALTER TABLE `org` DISABLE KEYS */;
INSERT INTO `org` VALUES (1,'IIT Kharagpur','PPEGKfx0EdASTw5nw1p3xylCx3BD5xbVv4Tuy5gkiAI='),(2,'IIT Kanpur','6uFXS8YJg/K5BpJw4WdrqhDNjF4rMMcisIhY376UhBY='),(3,'Jadavpur University','JrTZVzV61ywoQW77Vxx/U8bcg1VkIvDNQgsUyrTvBxk='),(4,'IIT Bombay','lyCQdXd0OWR5B8e2uJPb7O52ZmM8dG9nb5i5fnGdp0g=');
/*!40000 ALTER TABLE `org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policy`
--

DROP TABLE IF EXISTS `policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy` (
  `policy_id` int NOT NULL AUTO_INCREMENT,
  `operation_id` int NOT NULL,
  PRIMARY KEY (`policy_id`),
  KEY `operation_id` (`operation_id`),
  CONSTRAINT `policy_ibfk_1` FOREIGN KEY (`operation_id`) REFERENCES `operations` (`operation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy`
--

LOCK TABLES `policy` WRITE;
/*!40000 ALTER TABLE `policy` DISABLE KEYS */;
INSERT INTO `policy` VALUES (1,1),(2,1),(3,1),(5,1),(7,1),(4,2),(6,2),(8,3);
/*!40000 ALTER TABLE `policy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policy_env_aval`
--

DROP TABLE IF EXISTS `policy_env_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy_env_aval` (
  `policy_id` int NOT NULL,
  `env_attribute_id` int NOT NULL,
  `env_val` varchar(64) NOT NULL,
  PRIMARY KEY (`policy_id`,`env_attribute_id`,`env_val`),
  KEY `env_attribute_id` (`env_attribute_id`,`env_val`),
  CONSTRAINT `policy_env_aval_ibfk_1` FOREIGN KEY (`env_attribute_id`, `env_val`) REFERENCES `env_aval` (`env_attribute_id`, `env_val`),
  CONSTRAINT `policy_env_aval_ibfk_2` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`policy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy_env_aval`
--

LOCK TABLES `policy_env_aval` WRITE;
/*!40000 ALTER TABLE `policy_env_aval` DISABLE KEYS */;
INSERT INTO `policy_env_aval` VALUES (7,3,'1');
/*!40000 ALTER TABLE `policy_env_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policy_resource_aval`
--

DROP TABLE IF EXISTS `policy_resource_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy_resource_aval` (
  `policy_id` int NOT NULL,
  `resource_attribute_id` int NOT NULL,
  `resource_val` varchar(64) NOT NULL,
  PRIMARY KEY (`policy_id`,`resource_attribute_id`,`resource_val`),
  KEY `policy_resource_aval_ibfk_1` (`resource_attribute_id`,`resource_val`),
  CONSTRAINT `policy_resource_aval_ibfk_1` FOREIGN KEY (`resource_attribute_id`, `resource_val`) REFERENCES `resource_aval` (`resource_attribute_id`, `resource_val`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `policy_resource_aval_ibfk_2` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`policy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy_resource_aval`
--

LOCK TABLES `policy_resource_aval` WRITE;
/*!40000 ALTER TABLE `policy_resource_aval` DISABLE KEYS */;
INSERT INTO `policy_resource_aval` VALUES (1,2,'CSE'),(2,2,'ECE'),(6,2,'ME'),(7,2,'ME'),(8,2,'ME'),(3,6,'FacultyOfEngineering'),(4,6,'FacultyOfEngineering'),(5,6,'FacultyOfEngineering');
/*!40000 ALTER TABLE `policy_resource_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policy_user_aval`
--

DROP TABLE IF EXISTS `policy_user_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy_user_aval` (
  `policy_id` int NOT NULL,
  `user_attribute_id` int NOT NULL,
  `user_val` varchar(64) NOT NULL,
  PRIMARY KEY (`policy_id`,`user_attribute_id`,`user_val`),
  KEY `policy_user_aval_ibfk_1` (`user_attribute_id`,`user_val`),
  CONSTRAINT `policy_user_aval_ibfk_1` FOREIGN KEY (`user_attribute_id`, `user_val`) REFERENCES `user_aval` (`user_attribute_id`, `user_val`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `policy_user_aval_ibfk_2` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`policy_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy_user_aval`
--

LOCK TABLES `policy_user_aval` WRITE;
/*!40000 ALTER TABLE `policy_user_aval` DISABLE KEYS */;
INSERT INTO `policy_user_aval` VALUES (1,2,'CSE'),(2,2,'ECE'),(6,2,'ME'),(1,3,'AssistantDean'),(2,3,'AssistantDean'),(8,3,'AssistantDean'),(7,5,'School'),(5,5,'SchoolOfEducation'),(8,5,'SchoolOfEngineering'),(3,6,'FacultyOfEngineering'),(4,6,'FacultyOfEngineering');
/*!40000 ALTER TABLE `policy_user_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource` (
  `resource_id` int NOT NULL AUTO_INCREMENT,
  `resource_name` varchar(128) NOT NULL,
  PRIMARY KEY (`resource_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
INSERT INTO `resource` VALUES (1,'cormen.pdf'),(2,'galvin.pdf'),(3,'hennessey-patterson'),(4,'digital_electronics.pdf'),(5,'mechanics.pdf');
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_attributes`
--

DROP TABLE IF EXISTS `resource_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_attributes` (
  `resource_attribute_id` int NOT NULL AUTO_INCREMENT,
  `resource_attribute` varchar(64) NOT NULL,
  PRIMARY KEY (`resource_attribute_id`),
  UNIQUE KEY `resource_attribute` (`resource_attribute`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_attributes`
--

LOCK TABLES `resource_attributes` WRITE;
/*!40000 ALTER TABLE `resource_attributes` DISABLE KEYS */;
INSERT INTO `resource_attributes` VALUES (7,'College'),(2,'Department'),(6,'Faculty'),(5,'School');
/*!40000 ALTER TABLE `resource_attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_aval`
--

DROP TABLE IF EXISTS `resource_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_aval` (
  `resource_attribute_id` int NOT NULL,
  `resource_val` varchar(64) NOT NULL,
  PRIMARY KEY (`resource_attribute_id`,`resource_val`),
  CONSTRAINT `resource_aval_ibfk_1` FOREIGN KEY (`resource_attribute_id`) REFERENCES `resource_attributes` (`resource_attribute_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_aval`
--

LOCK TABLES `resource_aval` WRITE;
/*!40000 ALTER TABLE `resource_aval` DISABLE KEYS */;
INSERT INTO `resource_aval` VALUES (2,'BT'),(2,'CS'),(2,'CSE'),(2,'CSIT'),(2,'CY'),(2,'EC'),(2,'ECE'),(2,'EE'),(2,'IE'),(2,'IT'),(2,'Maths'),(2,'ME'),(2,'MI'),(2,'MNC'),(2,'MT'),(2,'PH'),(5,'SchoolOfBasicSciences'),(5,'SchoolOfBusiness'),(5,'SchoolOfComputingandElectricalEngineering'),(5,'SchoolOfEducation'),(5,'SchoolOfEngineering'),(5,'SchoolOfHumanities'),(5,'SchoolOfLaw'),(5,'SchoolOfManagement'),(5,'SchoolOfMedicine'),(6,'FacultyOfBiotechnology'),(6,'FacultyOfEngineering'),(6,'FacultyOfHumanities'),(6,'FacultyOfInterdisciplinarySciences'),(6,'FacultyOfSciences'),(7,'CollegeOfEngineering'),(7,'CollegeOfHumanities'),(7,'CollegeOfLiberalArts');
/*!40000 ALTER TABLE `resource_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_details`
--

DROP TABLE IF EXISTS `resource_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_details` (
  `resource_id` int NOT NULL,
  `resource_attribute_id` int NOT NULL,
  `resource_val` varchar(64) NOT NULL,
  PRIMARY KEY (`resource_id`,`resource_attribute_id`),
  KEY `resource_details_ibfk_1` (`resource_attribute_id`,`resource_val`),
  CONSTRAINT `resource_details_ibfk_1` FOREIGN KEY (`resource_attribute_id`, `resource_val`) REFERENCES `resource_aval` (`resource_attribute_id`, `resource_val`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_details`
--

LOCK TABLES `resource_details` WRITE;
/*!40000 ALTER TABLE `resource_details` DISABLE KEYS */;
INSERT INTO `resource_details` VALUES (2,2,'CSE'),(4,2,'ECE'),(1,2,'Maths'),(5,2,'ME'),(3,6,'FacultyOfEngineering');
/*!40000 ALTER TABLE `resource_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(64) NOT NULL,
  `login_name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login_name` (`login_name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','admin','admin@iitkgp.ac.in','pbkdf2:sha256:150000$VrgqgfRJ$909e6663566b363f28acb758ed4808b87730e14f27491e444b0698e558b1667b'),(2,'student1','student1','student1@gmail.com','pbkdf2:sha256:260000$yhZel5lewncMdvTn$6fa4c6316928a428fce3d1132bfc71c04201b9390aaa865ed06b8cb66d35a9a1'),(3,'student2','student2','student2@gmail.com','pbkdf2:sha256:260000$WhQ6KcWphKspE3OV$2d6a9b6f9b6a5f712620b61ec34bda510498c3e7fb4bb4edd3e16d4c1030361e'),(4,'professor1','professor1','professor1@gmail.com','pbkdf2:sha256:260000$LMsYmjLENeTgW1i3$1e563f34433e7539ac02f4a059220b04b55c930e46868dd890f7b108ce51f4f9'),(5,'professor2','professor2','professor2@gmail.com','pbkdf2:sha256:260000$xCCQCxzOVCYuIEZt$2e3325521e34b5aa4707e071d111b1cc8e95c07b6989b2ed5294f398871b41ac'),(6,'studentME','studentME','studentME@gmail.com','pbkdf2:sha256:150000$XGRdwS07$c9d064f14919bea0a5006a7e20af71bfe0b3477a859ddde22e1c609693e6d9f4'),(7,'deanS','deanS','deanS@gmail.com','pbkdf2:sha256:150000$wkNlmtEu$b2f61fea86ddf6fa319f1fe279ad1261381d06acd40a44ddc6216208b49e0ec1'),(8,'studentMaths','studentMaths','studentMaths@gmail.com','pbkdf2:sha256:150000$IzkLLQBL$3c44483f2318b817b4dfbf7dc6a0ef1893b116364219eff7f89a442fc51b6a3c');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_attributes`
--

DROP TABLE IF EXISTS `user_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_attributes` (
  `user_attribute_id` int NOT NULL AUTO_INCREMENT,
  `user_attribute` varchar(64) NOT NULL,
  PRIMARY KEY (`user_attribute_id`),
  UNIQUE KEY `user_attribute` (`user_attribute`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_attributes`
--

LOCK TABLES `user_attributes` WRITE;
/*!40000 ALTER TABLE `user_attributes` DISABLE KEYS */;
INSERT INTO `user_attributes` VALUES (7,'College'),(2,'Department'),(3,'Designation'),(6,'Faculty'),(4,'Role'),(5,'School'),(1,'user_type');
/*!40000 ALTER TABLE `user_attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_aval`
--

DROP TABLE IF EXISTS `user_aval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_aval` (
  `user_attribute_id` int NOT NULL,
  `user_val` varchar(64) NOT NULL,
  PRIMARY KEY (`user_attribute_id`,`user_val`),
  CONSTRAINT `user_aval_ibfk_1` FOREIGN KEY (`user_attribute_id`) REFERENCES `user_attributes` (`user_attribute_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_aval`
--

LOCK TABLES `user_aval` WRITE;
/*!40000 ALTER TABLE `user_aval` DISABLE KEYS */;
INSERT INTO `user_aval` VALUES (1,'Admin'),(1,'Adminnn'),(2,'BT'),(2,'CS'),(2,'CSE'),(2,'CSIT'),(2,'CY'),(2,'EC'),(2,'ECE'),(2,'EE'),(2,'IE'),(2,'IT'),(2,'Maths'),(2,'ME'),(2,'MI'),(2,'MNC'),(2,'MT'),(2,'PH'),(2,'School'),(3,'AdministrativeStaff'),(3,'AssistantDean'),(3,'Assistantprofessor'),(3,'Assistantregistrar'),(3,'Associatedean'),(3,'Associateprofessor'),(3,'CollegeEmployee'),(3,'Coordinator'),(3,'Dean'),(3,'Deaninfrastructure'),(3,'Deaninternationalrelations'),(3,'Deansric'),(3,'Deanstudentaffairs'),(3,'Deanug'),(3,'Deputydirector'),(3,'Deputyprincipal'),(3,'Director'),(3,'Employee'),(3,'Faculty'),(3,'Hallmanager'),(3,'HOD'),(3,'Juniorteacher'),(3,'Labassistant'),(3,'Principal'),(3,'Professor'),(3,'Registrar'),(3,'Researchassistant'),(3,'SchoolEmployee'),(3,'Student'),(3,'Teacher'),(3,'Visitingprofessor'),(3,'Warden'),(5,'School'),(5,'SchoolOfBasicSciences'),(5,'SchoolOfBusiness'),(5,'SchoolOfComputingandElectricalEngineering'),(5,'SchoolOfEducation'),(5,'SchoolOfEngineering'),(5,'SchoolOfHumanities'),(5,'SchoolOfLaw'),(5,'SchoolOfManagement'),(5,'SchoolOfMedicine'),(6,'FacultyOfBiotechnology'),(6,'FacultyOfEngineering'),(6,'FacultyOfHumanities'),(6,'FacultyOfInterdisciplinarySciences'),(6,'FacultyOfSciences'),(7,'CollegeOfEngineering'),(7,'CollegeOfHumanities'),(7,'CollegeOfLiberalArts');
/*!40000 ALTER TABLE `user_aval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_details`
--

DROP TABLE IF EXISTS `user_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_details` (
  `user_id` int NOT NULL,
  `user_attribute_id` int NOT NULL,
  `user_val` varchar(64) NOT NULL,
  PRIMARY KEY (`user_id`,`user_attribute_id`),
  KEY `user_details_ibfk_1` (`user_attribute_id`,`user_val`),
  CONSTRAINT `user_details_ibfk_1` FOREIGN KEY (`user_attribute_id`, `user_val`) REFERENCES `user_aval` (`user_attribute_id`, `user_val`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_details`
--

LOCK TABLES `user_details` WRITE;
/*!40000 ALTER TABLE `user_details` DISABLE KEYS */;
INSERT INTO `user_details` VALUES (1,1,'Admin'),(2,2,'CSE'),(4,2,'CSE'),(3,2,'ECE'),(5,2,'ECE'),(8,2,'Maths'),(6,2,'ME'),(7,2,'School'),(4,3,'Assistantprofessor'),(5,3,'Assistantprofessor'),(7,3,'Dean'),(2,3,'Student'),(3,3,'Student'),(6,3,'Student'),(8,3,'Student');
/*!40000 ALTER TABLE `user_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-14 23:43:47
