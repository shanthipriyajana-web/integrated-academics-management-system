-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: academics_management_system
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `accounts_passwordresettoken`
--

DROP TABLE IF EXISTS `accounts_passwordresettoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_passwordresettoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` char(32) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `used` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `accounts_passwordresettoken_user_id_2789bc5c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_passwordresettoken_user_id_2789bc5c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_passwordresettoken`
--

LOCK TABLES `accounts_passwordresettoken` WRITE;
/*!40000 ALTER TABLE `accounts_passwordresettoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_passwordresettoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_preregistereduser`
--

DROP TABLE IF EXISTS `accounts_preregistereduser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_preregistereduser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `role` varchar(20) NOT NULL,
  `department` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `registered` tinyint(1) NOT NULL,
  `semester` varchar(5) NOT NULL,
  `academic_year` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_preregistereduser`
--

LOCK TABLES `accounts_preregistereduser` WRITE;
/*!40000 ALTER TABLE `accounts_preregistereduser` DISABLE KEYS */;
INSERT INTO `accounts_preregistereduser` VALUES (1,'chemistry@gmail.com','assistant','Chemistry','2026-05-08 06:29:21.785987',1,'',''),(2,'computers@gmail.com','assistant','Computer science','2026-05-08 06:29:43.682219',1,'',''),(3,'csprofessor1@gmail.com','faculty','Computer science','2026-05-08 06:33:39.684782',1,'',''),(4,'csprofessor2@gmail.com','faculty','Computer science','2026-05-08 06:33:48.286414',1,'',''),(5,'csprofessor3@gmail.com','faculty','Computer science','2026-05-08 06:33:57.841841',1,'',''),(6,'csguestfaculty@gmail.com','faculty','Computer science','2026-05-08 06:34:24.662034',1,'',''),(7,'student1@gmail.com','student','Computer science','2026-05-08 06:34:58.620158',1,'','2025-27'),(8,'chemistryp1@gmail.com','faculty','Chemistry','2026-05-08 06:37:51.541811',1,'',''),(9,'cstu1@gmail.com','student','Chemistry','2026-05-08 06:38:50.085263',1,'','2024-26'),(10,'cstu2@gmail.com','student','Chemistry','2026-05-08 06:39:36.926416',1,'','2025-27'),(11,'foodtech@gmail.com','assistant','Food Technology','2026-05-27 07:40:35.847967',0,'',''),(13,'marineboi@gmail.com','assistant','Marine Biology','2026-05-27 07:42:02.574222',0,'','');
/*!40000 ALTER TABLE `accounts_preregistereduser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `department` varchar(200) NOT NULL,
  `role` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `semester` varchar(5) NOT NULL,
  `academic_year` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1200000$kSLcZkP2TmFZvCXBnTqpcp$41X8QqSB8mLQMV2y8RLk5zuRaYmNqt/YnUQJJDWBA2E=','2026-05-27 08:47:43.760948',1,'vsu@gmail.com','Prof. Ch. Vijaya','','assistant',1,1,'2026-05-08 06:28:54.915335','',''),(2,'pbkdf2_sha256$1200000$OSnLMaITctDDmiRid6UWQj$/g8OMjgqVxDG9cKBAdfDpafJw98IAnFdxHrnyNthcO0=','2026-05-27 08:55:02.126856',0,'computers@gmail.com','Melody','Computer science','assistant',1,0,'2026-05-08 06:32:06.459248','',''),(3,'pbkdf2_sha256$1200000$QFs4ajjxx4FE74YCekDJLA$GLiKfQPJxsFfvWj6SaQCc17BxcM1/hddFk/m2Fl9740=','2026-05-27 07:44:24.685952',0,'chemistry@gmail.com','Naga Vishnu','Chemistry','assistant',1,0,'2026-05-08 06:36:38.834487','',''),(4,'pbkdf2_sha256$600000$ev2UL8PbY6LqxkkW4kfh8g$ApFzX4jDYdrkP/yeC+gWGxgh3+mvfQm+Ja5eNpLUWK8=','2026-05-08 06:41:18.323278',0,'chemistryp1@gmail.com','Dr. P. Thriveni','Chemistry','faculty',1,0,'2026-05-08 06:40:41.601423','',''),(5,'pbkdf2_sha256$600000$1kYyJaqkWwX8Cp7wuSlXEO$3H9cMk+15bLKOElC7xFS3OzPZLeCVjS9tGidAMsRqgw=',NULL,0,'cstu1@gmail.com','Thanuja','Chemistry','student',1,0,'2026-05-08 06:42:18.680608','','2024-26'),(6,'pbkdf2_sha256$600000$3gB2wRY8jDNIRbWBsFWspP$SwpJXIp3mvwFbZFWCqRBpGepz4c1IS5ZL8Y3gn48Sug=',NULL,0,'cstu2@gmail.com','Dharshitha','Chemistry','student',1,0,'2026-05-08 06:45:16.400275','','2025-27'),(7,'pbkdf2_sha256$600000$l3P75CLS2O0S0UqPH4032K$etbONK8mesL6hlWi12kBBYWYJaEN4irN8K/t1sHih9g=','2026-05-12 14:32:36.663756',0,'csprofessor1@gmail.com','Prof. Ande Prasad','Computer science','faculty',1,0,'2026-05-08 06:47:56.764132','',''),(8,'pbkdf2_sha256$600000$4F97SeMp6abzRHJjfrjtid$nDnB1oQ/1k7ZgjleD2qBQJ+3bNG/7vV99PyTcIlY1h0=',NULL,0,'csprofessor2@gmail.com','Dr. M. Ussenaiah','Computer science','faculty',1,0,'2026-05-08 06:48:33.306220','',''),(9,'pbkdf2_sha256$600000$4C3cMQgRFX1XMLQy6jZlmq$DLyLwjW3t8b+tEV3ppByAsgoZwLhgUSBqKk0pqLJ59M=',NULL,0,'csprofessor3@gmail.com','Dr. G. Vijaya Lakashmi','Computer science','faculty',1,0,'2026-05-08 06:51:55.119889','',''),(10,'pbkdf2_sha256$600000$7g19mQ0dOYtRlZYvfGfCza$dOWlzShUbdYXmpnWvfq+9Ea60NUX43+OUPLEge5p0as=',NULL,0,'csguestfaculty@gmail.com','Mr. P. Srennivasulu','Computer science','faculty',1,0,'2026-05-08 06:52:48.514456','',''),(11,'pbkdf2_sha256$600000$PBBhGuFV2iWRfWib37ENIT$mhn574xytGHWkoN95cag4OwLxOTzjigxrZIy/Grzk68=','2026-05-14 15:10:47.078254',0,'student1@gmail.com','Shanthipriya Jana','Computer science','student',1,0,'2026-05-12 10:34:04.538559','','2025-27');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add User',6,'add_user'),(22,'Can change User',6,'change_user'),(23,'Can delete User',6,'delete_user'),(24,'Can view User',6,'view_user'),(25,'Can add Pre-registered User',7,'add_preregistereduser'),(26,'Can change Pre-registered User',7,'change_preregistereduser'),(27,'Can delete Pre-registered User',7,'delete_preregistereduser'),(28,'Can view Pre-registered User',7,'view_preregistereduser'),(29,'Can add password reset token',8,'add_passwordresettoken'),(30,'Can change password reset token',8,'change_passwordresettoken'),(31,'Can delete password reset token',8,'delete_passwordresettoken'),(32,'Can view password reset token',8,'view_passwordresettoken'),(33,'Can add faculty',9,'add_faculty'),(34,'Can change faculty',9,'change_faculty'),(35,'Can delete faculty',9,'delete_faculty'),(36,'Can view faculty',9,'view_faculty'),(37,'Can add subject',10,'add_subject'),(38,'Can change subject',10,'change_subject'),(39,'Can delete subject',10,'delete_subject'),(40,'Can view subject',10,'view_subject'),(41,'Can add syllabus',11,'add_syllabus'),(42,'Can change syllabus',11,'change_syllabus'),(43,'Can delete syllabus',11,'delete_syllabus'),(44,'Can view syllabus',11,'view_syllabus'),(45,'Can add old question paper',12,'add_oldquestionpaper'),(46,'Can change old question paper',12,'change_oldquestionpaper'),(47,'Can delete old question paper',12,'delete_oldquestionpaper'),(48,'Can view old question paper',12,'view_oldquestionpaper');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_faculty`
--

DROP TABLE IF EXISTS `core_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_faculty` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `department` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_faculty_department_code_3510cc54_uniq` (`department`,`code`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_faculty`
--

LOCK TABLES `core_faculty` WRITE;
/*!40000 ALTER TABLE `core_faculty` DISABLE KEYS */;
INSERT INTO `core_faculty` VALUES (1,'AP','Prof. Ande Prasad','Computer science'),(2,'MU','Dr. M. Ussenaiah','Computer science'),(3,'GVL','Dr. G. Vijaya Lakshmi','Computer science'),(4,'PS','Mr. P. Sreenivasulu','Computer science'),(5,'TVN','Dr. P. Thriveni','Chemistry');
/*!40000 ALTER TABLE `core_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_oldquestionpaper`
--

DROP TABLE IF EXISTS `core_oldquestionpaper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_oldquestionpaper` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department` varchar(200) NOT NULL,
  `academic_year` varchar(10) NOT NULL,
  `semester` varchar(5) NOT NULL,
  `subject_name` varchar(200) NOT NULL,
  `subject_code` varchar(50) NOT NULL,
  `exam_type` varchar(100) NOT NULL,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `uploaded_by` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_oldquestionpaper`
--

LOCK TABLES `core_oldquestionpaper` WRITE;
/*!40000 ALTER TABLE `core_oldquestionpaper` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_oldquestionpaper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_subject`
--

DROP TABLE IF EXISTS `core_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_subject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `year` varchar(10) NOT NULL,
  `semester` varchar(5) NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(200) NOT NULL,
  `hours_per_week` smallint unsigned NOT NULL,
  `faculty_id` bigint NOT NULL,
  `department` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_subject_department_year_semester_code_e7456758_uniq` (`department`,`year`,`semester`,`code`),
  KEY `core_subject_faculty_id_be73a8a9_fk_core_faculty_id` (`faculty_id`),
  CONSTRAINT `core_subject_faculty_id_be73a8a9_fk_core_faculty_id` FOREIGN KEY (`faculty_id`) REFERENCES `core_faculty` (`id`),
  CONSTRAINT `core_subject_chk_1` CHECK ((`hours_per_week` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_subject`
--

LOCK TABLES `core_subject` WRITE;
/*!40000 ALTER TABLE `core_subject` DISABLE KEYS */;
INSERT INTO `core_subject` VALUES (1,'2025-26','II','ESE','Enterprise software Engineering',4,3,'Computer science'),(2,'2025-26','II','DS','Data science',4,3,'Computer science'),(3,'2025-26','II','DS Lab','Data science Lab',3,3,'Computer science'),(4,'2025-26','II','AI','Artificial intelligence',4,1,'Computer science'),(5,'2025-26','II','AI Lab','Artificial intelligence Lab',3,1,'Computer science'),(6,'2025-26','II','.NET','Web development using .net technologies',4,2,'Computer science'),(7,'2025-26','II','.NET Lab','Web development using .net technologies Lab',3,2,'Computer science'),(8,'2025-26','II','UI/UX','User interface and user experience design',4,2,'Computer science'),(9,'2025-26','II','UI/UX Lab','User interface and user experience design Lab',3,2,'Computer science'),(12,'2025-26','II','VM','Vedic Mathematics',4,1,'Computer science'),(13,'2026-27','III','SPM','Software project management',4,3,'Computer science'),(14,'2026-27','III','ML','Machine Learning',4,1,'Computer science'),(15,'2026-27','III','ML Lab','Machine Learning Lab',3,1,'Computer science'),(16,'2026-27','III','WID Lab','Web interface designing Lab',3,2,'Computer science'),(18,'2026-27','III','MEAN','MEAN Stack Development',4,3,'Computer science'),(19,'2026-27','III','MEAN Lab','MEAN Stack Development Lab',3,3,'Computer science'),(20,'2026-27','III','MongoDB','NoSQL with MongoDB',4,4,'Computer science'),(21,'2026-27','III','MongoDB Lab','NoSQL with MongoDB Lab',3,4,'Computer science'),(22,'2026-27','III','WID','Web interface designing',4,2,'Computer science'),(23,'2026-27','I','DSA','Data structures & Algorithms',4,1,'Computer science'),(24,'2026-27','I','CN','Computer Networks',4,2,'Computer science'),(25,'2026-27','I','CN Lab','Computer Networks Lab',3,2,'Computer science'),(26,'2026-27','I','PPP','Principles of Python programming',4,3,'Computer science'),(27,'2026-27','I','PPP Lab','Principles of Python programming Lab',3,3,'Computer science'),(28,'2026-27','I','AJP','Advance Java programming',4,4,'Computer science'),(29,'2026-27','I','AJP Lab','Advance Java programming Lab',3,4,'Computer science'),(30,'2026-27','I','OS Lab','Operating Systems Lab',3,3,'Computer science'),(31,'2026-27','I','OS','Operating Systems',4,3,'Computer science'),(32,'2026-27','I','IT Act','Information & Technology Act',4,1,'Computer science');
/*!40000 ALTER TABLE `core_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_syllabus`
--

DROP TABLE IF EXISTS `core_syllabus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_syllabus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department` varchar(200) NOT NULL,
  `academic_year` varchar(10) NOT NULL,
  `semester` varchar(5) NOT NULL,
  `title` varchar(300) NOT NULL,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `uploaded_by` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_syllabus_department_academic_year_semester_22248b0c_uniq` (`department`,`academic_year`,`semester`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_syllabus`
--

LOCK TABLES `core_syllabus` WRITE;
/*!40000 ALTER TABLE `core_syllabus` DISABLE KEYS */;
INSERT INTO `core_syllabus` VALUES (1,'Computer science','','II','MCA semester-2 Syllabus','syllabus/MCA_II_Sem_Syllabus_9pFr5Mo.pdf','2026-05-12 10:22:13.885255','Melody'),(2,'Computer science','2026-27','III','MCA semester-3 Syllabus','syllabus/MCA_III_Sem_Syllabus.pdf','2026-05-12 13:56:35.130044','Melody');
/*!40000 ALTER TABLE `core_syllabus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'accounts','passwordresettoken'),(7,'accounts','preregistereduser'),(6,'accounts','user'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(9,'core','faculty'),(12,'core','oldquestionpaper'),(10,'core','subject'),(11,'core','syllabus'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-05-08 06:26:19.897347'),(2,'contenttypes','0002_remove_content_type_name','2026-05-08 06:26:20.039249'),(3,'auth','0001_initial','2026-05-08 06:26:20.418337'),(4,'auth','0002_alter_permission_name_max_length','2026-05-08 06:26:20.500222'),(5,'auth','0003_alter_user_email_max_length','2026-05-08 06:26:20.508526'),(6,'auth','0004_alter_user_username_opts','2026-05-08 06:26:20.516258'),(7,'auth','0005_alter_user_last_login_null','2026-05-08 06:26:20.523277'),(8,'auth','0006_require_contenttypes_0002','2026-05-08 06:26:20.528686'),(9,'auth','0007_alter_validators_add_error_messages','2026-05-08 06:26:20.537849'),(10,'auth','0008_alter_user_username_max_length','2026-05-08 06:26:20.566370'),(11,'auth','0009_alter_user_last_name_max_length','2026-05-08 06:26:20.580496'),(12,'auth','0010_alter_group_name_max_length','2026-05-08 06:26:20.624099'),(13,'auth','0011_update_proxy_permissions','2026-05-08 06:26:20.647908'),(14,'auth','0012_alter_user_first_name_max_length','2026-05-08 06:26:20.674601'),(15,'accounts','0001_initial','2026-05-08 06:26:21.213713'),(16,'accounts','0002_user_department','2026-05-08 06:27:51.921841'),(17,'accounts','0003_enforce_assistant_uniqueness','2026-05-08 06:27:51.970958'),(18,'accounts','0004_preregistereduser_passwordresettoken','2026-05-08 06:27:52.351603'),(19,'accounts','0005_user_semester_academic_year','2026-05-08 06:27:52.651976'),(20,'admin','0001_initial','2026-05-08 06:27:52.840515'),(21,'admin','0002_logentry_remove_auto_add','2026-05-08 06:27:52.852303'),(22,'admin','0003_logentry_add_action_flag_choices','2026-05-08 06:27:52.860881'),(23,'core','0001_initial','2026-05-08 06:27:53.018060'),(24,'core','0002_add_department_to_subject','2026-05-08 06:27:53.145787'),(25,'core','0003_syllabus_oldquestionpaper','2026-05-08 06:27:53.216414'),(26,'core','0004_faculty_add_department','2026-05-08 06:27:53.339221'),(27,'sessions','0001_initial','2026-05-08 06:27:53.385629'),(28,'accounts','0006_alter_preregistereduser_academic_year_and_more','2026-05-28 10:59:40.122823'),(29,'core','0005_remove_syllabus_unique_syllabus_per_dept_year_sem_and_more','2026-05-28 10:59:40.258480');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-28 16:30:25
