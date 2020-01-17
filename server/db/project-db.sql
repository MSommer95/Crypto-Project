-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: project
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `auth_tokens`
--

DROP TABLE IF EXISTS `auth_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `token` varchar(512) DEFAULT NULL,
  `session_id` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_auth_tokens_users` (`user_id`),
  CONSTRAINT `FK_auth_tokens_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=488 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_tokens`
--

LOCK TABLES `auth_tokens` WRITE;
/*!40000 ALTER TABLE `auth_tokens` DISABLE KEYS */;
INSERT INTO `auth_tokens` VALUES (487,15,'7f3daf16a70681d91d4587598dcc53e3975da1c5bf1383f7b8c3045d9b4ca07331000cd961147821e59c8691aea39131176d6c9af975aa11a306e3e6fed73ad0','945b43a5309afddcb05060d6507cbe890ca483b15b9216b68f752722cecb3efc67274e48af452cfefde61a684b6f33dad7638d79ddb41ccac14f6729e1b7108f');
/*!40000 ALTER TABLE `auth_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_logs`
--

DROP TABLE IF EXISTS `login_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT '0',
  `counter` int(11) DEFAULT '0',
  `timestamp` int(11) DEFAULT '0',
  `is_send` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_login_logs_users` (`user_id`),
  CONSTRAINT `FK_login_logs_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_logs`
--

LOCK TABLES `login_logs` WRITE;
/*!40000 ALTER TABLE `login_logs` DISABLE KEYS */;
INSERT INTO `login_logs` VALUES (22,19,1,1574969876,0),(232,15,1,1578847456,0);
/*!40000 ALTER TABLE `login_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'2FA-Mail'),(2,'2FA-App');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_data`
--

DROP TABLE IF EXISTS `user_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_data` (
  `id` bigint(20) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL,
  `file_name` varchar(258) NOT NULL DEFAULT '',
  `file_description` varchar(512) NOT NULL DEFAULT '',
  `path` longtext NOT NULL,
  `is_encrypted` tinyint(4) NOT NULL DEFAULT '0',
  `encrypt_key` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_user_data_users` (`user_id`),
  KEY `FK_user_data_user_key` (`encrypt_key`),
  CONSTRAINT `FK_user_data_user_key` FOREIGN KEY (`encrypt_key`) REFERENCES `user_key` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_user_data_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_data`
--

LOCK TABLES `user_data` WRITE;
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
INSERT INTO `user_data` VALUES (1578771258665,15,'test.jpg.encrypted','My encrypted file','/files/encrypted/6a243d81a00661d94ec8c5cdedf10c08d882dc47',1,1578771258666),(1578782409998,15,'Neues RTF-Dokument.rtf','','/files/unencrypted/b8a1b1ae6f02ffc6b94e84726f6eba537c7c7ed2',0,NULL),(1578782737720,15,'Leistungsnachweis1.-6.Fachsemester.pdf','','/files/unencrypted/f2854eb3f87787011481c0762d49854a52a35b00',0,NULL),(1578931252265,15,'test.jpg','My decrypted file','/files/unencrypted/a8bb331894e351d0fca37cedf45b85b2cd346430',0,NULL);
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_device`
--

DROP TABLE IF EXISTS `user_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `device_id` varchar(258) DEFAULT NULL,
  `device_name` varchar(258) DEFAULT NULL,
  `device_is_active` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_user_device_users` (`user_id`),
  CONSTRAINT `FK_user_device_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_device`
--

LOCK TABLES `user_device` WRITE;
/*!40000 ALTER TABLE `user_device` DISABLE KEYS */;
INSERT INTO `user_device` VALUES (8,15,'fzS31eVR9dA:APA91bEY38-1mWq2YVhMUg_dc1pkAB2Mfmbc4UCtkoR64k9U3432PZWradMVl3IKgs3maBcVMR1IdXoFRJ_8euBkdg09gDnSaeXoI9KkVx54ws7JN3GASt0MmtZ9VofAMol3GRGoou3V','Android',0);
/*!40000 ALTER TABLE `user_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_key`
--

DROP TABLE IF EXISTS `user_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_key` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `file_id` bigint(20) NOT NULL DEFAULT '0',
  `key_path` varchar(258) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_user_key_users` (`user_id`),
  KEY `FK_user_key_user_data` (`file_id`),
  CONSTRAINT `FK_user_key_user_data` FOREIGN KEY (`file_id`) REFERENCES `user_data` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_user_key_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_key`
--

LOCK TABLES `user_key` WRITE;
/*!40000 ALTER TABLE `user_key` DISABLE KEYS */;
INSERT INTO `user_key` VALUES (1578771258666,15,1578771258665,'/keys/fae38ae56ac5cfe8348a530bc6c5c00225d24fca.key');
/*!40000 ALTER TABLE `user_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_otp`
--

DROP TABLE IF EXISTS `user_otp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_otp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `current_otp` varchar(50) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `verified` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=523 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_otp`
--

LOCK TABLES `user_otp` WRITE;
/*!40000 ALTER TABLE `user_otp` DISABLE KEYS */;
INSERT INTO `user_otp` VALUES (145,8,'33562210',1574173026,0),(413,19,'55865126',1574969675,0),(522,15,'40147478',1578064284,0);
/*!40000 ALTER TABLE `user_otp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_otp_used`
--

DROP TABLE IF EXISTS `user_otp_used`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_otp_used` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `used_otp` varchar(50) NOT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_used_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8 COMMENT='used OTPs go in here';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_otp_used`
--

LOCK TABLES `user_otp_used` WRITE;
/*!40000 ALTER TABLE `user_otp_used` DISABLE KEYS */;
INSERT INTO `user_otp_used` VALUES (1,15,'27287867',1575503974),(2,15,'62683212',1575504039),(3,15,'36704464',1575504142),(4,15,'22034044',1575553111),(5,15,'71515316',1575553327),(6,15,'70744738',1575553954),(7,15,'51215236',1575554050),(8,15,'44083102',1575554931),(9,15,'43506413',1575556384),(10,15,'07023055',1575587134),(11,15,'01641651',1575587150),(12,15,'42402740',1575588068),(13,15,'07387151',1575588128),(14,15,'73255476',1575588136),(15,15,'81026358',1575588188),(16,15,'01013426',1575588401),(17,15,'53888677',1575588417),(18,15,'43855003',1575588429),(19,15,'26346128',1575588679),(20,15,'58434588',1575635190),(21,15,'88384282',1575679052),(22,15,'66313271',1575753342),(23,15,'40818894',1576270010),(24,15,'81627304',1576270891),(25,15,'46815042',1576274275),(26,15,'23574595',1576275619),(27,15,'74584220',1576275691),(28,15,'08351409',1576275921),(29,15,'43257608',1576276056),(30,15,'45814074',1576276177),(31,15,'56877615',1576276257),(32,15,'51220239',1576276397),(33,15,'96852214',1576276614),(34,15,'21920276',1576276701),(35,15,'39800914',1576276812),(36,15,'37651283',1576276947),(37,15,'43459932',1576277051),(38,15,'65470145',1576277113),(39,15,'14823706',1576277279),(40,15,'95707104',1576277345),(41,15,'81790357',1576277490),(42,15,'25418184',1576277842),(43,15,'33552807',1576278077),(44,15,'16811017',1576278294),(45,15,'46496440',1576278382),(46,15,'17479183',1576278422),(47,15,'59324349',1576278759),(48,15,'33088068',1576278850),(49,15,'65098982',1576278923),(50,15,'57940606',1576279066),(51,15,'22680581',1576279073),(52,15,'42362648',1576279074),(53,15,'38290046',1576279092),(54,15,'66632437',1576279093),(55,15,'47360843',1576279101),(56,15,'93131340',1576279103),(57,15,'47055069',1576279320),(58,15,'05994988',1576279322),(59,15,'60408931',1576279992),(60,15,'50900689',1576280043),(61,15,'23863806',1576280098),(62,15,'44849750',1576281821),(63,15,'78200118',1577185816),(64,15,'64936625',1577186276),(65,15,'27191574',1577186463),(66,15,'06562869',1577186661),(67,15,'01276758',1577186676),(68,15,'11651049',1577186879),(69,15,'09052357',1578064043),(70,15,'31949036',1578064176),(71,15,'40147478',1578064284);
/*!40000 ALTER TABLE `user_otp_used` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_setting`
--

DROP TABLE IF EXISTS `user_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_setting` (
  `user_id` int(11) NOT NULL,
  `settings_id` int(11) NOT NULL,
  `setting_value` tinyint(11) NOT NULL DEFAULT '0',
  KEY `settings_id` (`settings_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_setting_settings` FOREIGN KEY (`settings_id`) REFERENCES `settings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_user_setting_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_setting`
--

LOCK TABLES `user_setting` WRITE;
/*!40000 ALTER TABLE `user_setting` DISABLE KEYS */;
INSERT INTO `user_setting` VALUES (6,1,1),(8,1,0),(8,2,1),(15,1,0),(15,2,0),(16,1,0),(16,2,0),(4,1,1),(4,2,0),(18,1,0),(18,2,0),(19,1,0),(19,2,0);
/*!40000 ALTER TABLE `user_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tokens`
--

DROP TABLE IF EXISTS `user_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `token` varchar(256) NOT NULL DEFAULT '0',
  `reset_case` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `user_tokens_user_id` (`user_id`),
  CONSTRAINT `user_tokens_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tokens`
--

LOCK TABLES `user_tokens` WRITE;
/*!40000 ALTER TABLE `user_tokens` DISABLE KEYS */;
INSERT INTO `user_tokens` VALUES (12,15,'e8454aacae5962f6d76690e8d164be061e6c98734b57bf9ae12ff077dfd676b66ff5855ae0c3d08e845c5099b5198cdae1ac55765c2f6f217a9dc1e25c34b5c033a834750ff1a808ec8d45b3653efc51f91d30e000fa2e70324159fba6b293c0',1);
/*!40000 ALTER TABLE `user_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1576 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'Test@test','a6906caa2528d9c60122a82f4d9de1832e0cace9c325f5d9d996fee11ed722ecd2b350401c89b9d1ba2d7faa41d184a3cf56ebe799ec0ff3bde074f789860e514e2ccc2d990b929a4f3e9350dc8269d74feff7aa634e950bd8cb5e3086eccfe0'),(5,'test@me.de','624082f6e5546ad8a12bc8f75acd795b60da291700686711bbd652b12c4ab28255afe96f159d8f1739137ceb25dd2e02fcd943931bf85f6bd9e3d3fdeee7d5dfe75678459c2846cfc696cce5cb1d8ba933cdf36c730c88804e42a433ec5b2c9e'),(6,'zonaafa@web.de','e9fa407622d249111c65190d40fbc1107937ad8fc5e7e5d9ac14de64f00e8e22c340de148469e5097c0857f9c40c41ada366d1986b4c16047d6500a0ebf71d9512a3e4698ee32dbb3f15809345c7b0b47c2dc84918e3a103ea4b4c7494857203'),(8,'max.sommer_95@web.de','ca2681e47edcda6a0894d28ba3e4fae805d7309c69dbd4f1715067e7485a0a85b6b5469fb92509e00d0e3681bd48bcfe2ddf6d6425e891e4a0523b138d1c426da5a4d75fb2c4312091f8c7af8121596cc90f8b60ed71bc79b9f3db268c61a7eb'),(15,'maximilian.sommer@stud.hshl.de','4748e3f07d5fab8dc0a57cd75af698b24c4d51fb11ebf791bd83688c9b305cd141624546996dc2be3b84fec1785d42d7e3482f28ac07f6653480d11a5268f8cd1dc4412f6928407ad6f8b78259c4ac7d88fc130c99fc07357148cb9e25bfaec5'),(16,'testMe@mail.de','48b6cba61dcb54e4dc58f6c07c67fdd2893a271cc8d16f4026e923e37833f4935ebd969bb56d4ffddbb91d5f3f32c5e76808e1eb7443c2fdf4f4b624cdc75948ae906985838a6725d221c4a58f44db088c34eca4cf2b1d4c9eda180e71d51ab6'),(17,'test@test','7e13dfd479e71d669c6658b4d043c8a2a4c7eebb9ea00b93b500cdd49347e81f774d799cfb405ab1dba5f6b6cf126c7b058f67fc34a66f53b0d7d94d29017bfe1d735dd9910aaebd519535e639a4bf22b7a7d03b74fe80ee11a5d34280e0d67b'),(18,'haha@lol.de','291f2a6c5e9dbeef402f0c72819c8e65dd9c129eece0b9eb04ba16216e43e14792fb983504b666df8d36556a0fb40d4dcae1be57bdb14dac0743c2c318675b28dcada48dc17b96c9fbf0c7813cd003510d72fb90736f7a836148fdc7131aeead'),(19,'Testi@test','a16eb9e7c13042950b99b80d9d0fca48821e8468cd2e3293a9194635cbaf09e48b42924582fbe99a28259b048ed9afef15d1565a9b98bbed0f465ff4c9f9ecbaae78802830440b0bdccc92c054c30d7d33968e39ca2561eb749606a0ed6c1799');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-17  1:16:45
