-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server Version:               8.0.17 - MySQL Community Server - GPL
-- Server Betriebssystem:        Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Exportiere Datenbank Struktur für project
CREATE DATABASE IF NOT EXISTS `project` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `project`;

-- Exportiere Struktur von Tabelle project.settings
CREATE TABLE IF NOT EXISTS `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.settings: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` (`id`, `description`) VALUES
	(1, '2FA-Mail'),
	(2, '2FA-App');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.users: ~5 rows (ungefähr)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `email`, `password`) VALUES
	(4, 'Test@test', 'a6906caa2528d9c60122a82f4d9de1832e0cace9c325f5d9d996fee11ed722ecd2b350401c89b9d1ba2d7faa41d184a3cf56ebe799ec0ff3bde074f789860e514e2ccc2d990b929a4f3e9350dc8269d74feff7aa634e950bd8cb5e3086eccfe0'),
	(5, 'test@me.de', '624082f6e5546ad8a12bc8f75acd795b60da291700686711bbd652b12c4ab28255afe96f159d8f1739137ceb25dd2e02fcd943931bf85f6bd9e3d3fdeee7d5dfe75678459c2846cfc696cce5cb1d8ba933cdf36c730c88804e42a433ec5b2c9e'),
	(6, 'zonaafa@web.de', 'e9fa407622d249111c65190d40fbc1107937ad8fc5e7e5d9ac14de64f00e8e22c340de148469e5097c0857f9c40c41ada366d1986b4c16047d6500a0ebf71d9512a3e4698ee32dbb3f15809345c7b0b47c2dc84918e3a103ea4b4c7494857203'),
	(8, 'max.sommer_95@web.de', 'ca2681e47edcda6a0894d28ba3e4fae805d7309c69dbd4f1715067e7485a0a85b6b5469fb92509e00d0e3681bd48bcfe2ddf6d6425e891e4a0523b138d1c426da5a4d75fb2c4312091f8c7af8121596cc90f8b60ed71bc79b9f3db268c61a7eb'),
	(15, 'maximilian.sommer@stud.hshl.de', '114d8f13ab287dd6a2f501955f50f2a134441c1f094f83ccc6d59140fd3b75d539b4aea4f141272a14a07f5d678dc316933efb253d67795b6d207e35ac3c08a7af13b5c374e4a3b7e16adce14470085873e00abaddd92db36c6d15ba8c8e90b7'),
	(16, 'testMe@mail.de', '48b6cba61dcb54e4dc58f6c07c67fdd2893a271cc8d16f4026e923e37833f4935ebd969bb56d4ffddbb91d5f3f32c5e76808e1eb7443c2fdf4f4b624cdc75948ae906985838a6725d221c4a58f44db088c34eca4cf2b1d4c9eda180e71d51ab6'),
	(17, 'test@test', '7e13dfd479e71d669c6658b4d043c8a2a4c7eebb9ea00b93b500cdd49347e81f774d799cfb405ab1dba5f6b6cf126c7b058f67fc34a66f53b0d7d94d29017bfe1d735dd9910aaebd519535e639a4bf22b7a7d03b74fe80ee11a5d34280e0d67b');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_data
CREATE TABLE IF NOT EXISTS `user_data` (
  `id` bigint(20) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL,
  `file_name` varchar(258) NOT NULL DEFAULT '',
  `path` longtext NOT NULL,
  `is_encrypted` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_user_data_users` (`user_id`),
  CONSTRAINT `FK_user_data_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_data: ~2 rows (ungefähr)
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_device
CREATE TABLE IF NOT EXISTS `user_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `device_id` varchar(258) DEFAULT NULL,
  `device_name` varchar(258) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_user_device_users` (`user_id`),
  CONSTRAINT `FK_user_device_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_device: ~2 rows (ungefähr)
/*!40000 ALTER TABLE `user_device` DISABLE KEYS */;
INSERT INTO `user_device` (`id`, `user_id`, `device_id`, `device_name`) VALUES
	(1, 8, 'eZsXTXyZveo:APA91bHjZxX3KCS2FKW1r9-u5_RERs7j2mAp2BF714ClXG9jhQAtNpzUML-TjOWpeimLcTbQm83uUH7eY-rtN0LVS0Fd8oSKd0zIG-X252WfMk3_GDD9Pjjxi-ejo_t4tcuex65Nj9S9', 'max_android'),
	(2, 15, 'fzS31eVR9dA:APA91bEY38-1mWq2YVhMUg_dc1pkAB2Mfmbc4UCtkoR64k9U3432PZWradMVl3IKgs3maBcVMR1IdXoFRJ_8euBkdg09gDnSaeXoI9KkVx54ws7JN3GASt0MmtZ9VofAMol3GRGoou3V', 'AOSP on IA Emulator');
/*!40000 ALTER TABLE `user_device` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_key
CREATE TABLE IF NOT EXISTS `user_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `file_id` bigint(20) NOT NULL DEFAULT '0',
  `key_path` varchar(258) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_user_key_users` (`user_id`),
  KEY `FK_user_key_user_data` (`file_id`),
  CONSTRAINT `FK_user_key_user_data` FOREIGN KEY (`file_id`) REFERENCES `user_data` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_user_key_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_key: ~2 rows (ungefähr)
/*!40000 ALTER TABLE `user_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_key` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_otp
CREATE TABLE IF NOT EXISTS `user_otp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `current_otp` varchar(50) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `verified` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_otp: ~2 rows (ungefähr)
/*!40000 ALTER TABLE `user_otp` DISABLE KEYS */;
INSERT INTO `user_otp` (`id`, `user_id`, `current_otp`, `timestamp`, `verified`) VALUES
	(145, 8, '33562210', 1574173026, 0),
	(155, 15, '31220851', 1574181073, 0);
/*!40000 ALTER TABLE `user_otp` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_otp_used
CREATE TABLE IF NOT EXISTS `user_otp_used` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `used_otp` varchar(50) NOT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_used_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8 COMMENT='used OTPs go in here';

-- Exportiere Daten aus Tabelle project.user_otp_used: ~150 rows (ungefähr)
/*!40000 ALTER TABLE `user_otp_used` DISABLE KEYS */;
INSERT INTO `user_otp_used` (`id`, `user_id`, `used_otp`, `timestamp`) VALUES
	(1, 8, '74083486', 1571910485),
	(2, 8, '02630876', 1571910485),
	(3, 8, '50022336', 1571910520),
	(4, 8, '81102708', 1571910584),
	(5, 8, '35815824', 1571911347),
	(6, 8, '58180640', 1571912110),
	(7, 8, '78848263', 1571912149),
	(8, 8, '55483377', 1571912633),
	(9, 8, '25063076', 1571912740),
	(10, 8, '53080404', 1571912804),
	(11, 8, '50552567', 1571912908),
	(12, 8, '72365167', 1571913040),
	(13, 8, '84611052', 1571950172),
	(14, 8, '34147863', 1571950277),
	(15, 8, '01871640', 1571950363),
	(16, 8, '87430075', 1571950560),
	(17, 8, '42502223', 1571950587),
	(18, 8, '68660811', 1571950589),
	(19, 8, '55036408', 1571950623),
	(20, 8, '56856001', 1571951410),
	(21, 8, '01252255', 1571951472),
	(22, 8, '30578667', 1572364603),
	(23, 8, '28652555', 1572364718),
	(24, 8, '75483806', 1572365781),
	(25, 8, '87636717', 1572365907),
	(26, 8, '44307658', 1572370475),
	(27, 8, '03168477', 1572372872),
	(28, 8, '06201081', 1572431351),
	(29, 8, '26616575', 1572431470),
	(30, 8, '78834551', 1572431531),
	(31, 8, '40100722', 1572431594),
	(32, 8, '38436633', 1572619535),
	(33, 8, '31440756', 1572639362),
	(34, 8, '27128166', 1572640895),
	(35, 8, '71337280', 1572641234),
	(36, 8, '16534203', 1572642180),
	(37, 8, '06130062', 1572644039),
	(38, 8, '41165767', 1573414919),
	(39, 8, '01060884', 1573414938),
	(40, 8, '84627062', 1573414964),
	(41, 15, '83348532', 1573416550),
	(42, 8, '46260550', 1573469121),
	(43, 8, '32840386', 1573469404),
	(44, 8, '61704510', 1573469420),
	(45, 8, '56638547', 1573469506),
	(46, 8, '76818863', 1573469575),
	(47, 15, '05261211', 1573496176),
	(48, 15, '82212850', 1573498872),
	(49, 15, '76382647', 1573499017),
	(50, 15, '84410545', 1573499130),
	(51, 15, '41143176', 1573499224),
	(52, 15, '02067147', 1573500358),
	(53, 15, '31424282', 1573500897),
	(54, 15, '63853770', 1573501102),
	(55, 15, '75444720', 1573501154),
	(56, 15, '51323408', 1573501205),
	(57, 15, '81161376', 1573501369),
	(58, 15, '83621202', 1573501675),
	(59, 15, '76478652', 1573501686),
	(60, 15, '33554045', 1573502046),
	(61, 15, '57850535', 1573503520),
	(62, 15, '36205640', 1573505508),
	(63, 15, '81616481', 1573505686),
	(64, 15, '77562848', 1573505987),
	(65, 15, '86767077', 1573506069),
	(66, 15, '28525332', 1573506270),
	(67, 15, '67270400', 1573506483),
	(68, 15, '55730532', 1573506624),
	(69, 15, '17465088', 1573506726),
	(70, 15, '04855826', 1573506744),
	(71, 15, '82564654', 1573506763),
	(72, 15, '54506673', 1573506771),
	(73, 15, '56868260', 1573506819),
	(74, 15, '18366051', 1573506876),
	(75, 15, '41768135', 1573506989),
	(76, 15, '55238586', 1573507036),
	(77, 15, '86046772', 1573507105),
	(78, 15, '30633317', 1573507233),
	(79, 15, '83533640', 1573507249),
	(80, 15, '01683350', 1573508492),
	(81, 15, '86815874', 1573508647),
	(82, 15, '81367671', 1573508757),
	(83, 15, '55501234', 1573508796),
	(84, 15, '63746013', 1573508865),
	(85, 15, '31458842', 1573510610),
	(86, 15, '46826824', 1573510731),
	(87, 15, '14583467', 1573510859),
	(88, 15, '41656530', 1573510924),
	(89, 15, '12271481', 1573510968),
	(90, 15, '24153207', 1573511126),
	(91, 15, '84603502', 1573511306),
	(92, 15, '08456055', 1573511425),
	(93, 15, '21401272', 1573511524),
	(94, 15, '52120638', 1573511811),
	(95, 8, '00217845', 1573512193),
	(96, 8, '06606580', 1573512250),
	(97, 8, '26407136', 1573512311),
	(98, 15, '78841124', 1573512364),
	(99, 8, '17860466', 1573512389),
	(100, 15, '67022842', 1573512397),
	(101, 15, '02841546', 1573512407),
	(102, 15, '72653253', 1573512436),
	(103, 15, '73417107', 1573512558),
	(104, 15, '48018163', 1573512843),
	(105, 15, '10735241', 1573513283),
	(106, 8, '11282400', 1573554530),
	(107, 15, '14325281', 1573948727),
	(108, 15, '62143811', 1573948892),
	(109, 15, '27460506', 1573948971),
	(110, 8, '55304535', 1573949312),
	(111, 8, '80787126', 1573997369),
	(112, 8, '40661245', 1573997419),
	(113, 8, '52004457', 1573997642),
	(114, 8, '22734476', 1573998079),
	(115, 15, '20456684', 1574085816),
	(116, 15, '13280002', 1574086101),
	(117, 15, '62805616', 1574086136),
	(118, 15, '72820550', 1574087494),
	(119, 15, '07023310', 1574087851),
	(120, 8, '78624466', 1574114602),
	(121, 15, '78264080', 1574168723),
	(122, 15, '37017602', 1574169097),
	(123, 15, '76238861', 1574169517),
	(124, 15, '37026341', 1574169763),
	(125, 15, '42881663', 1574169863),
	(126, 15, '00417124', 1574170201),
	(127, 8, '86055742', 1574170225),
	(128, 8, '54742452', 1574170601),
	(129, 15, '88726387', 1574171026),
	(130, 15, '04876150', 1574171141),
	(131, 15, '76104161', 1574171207),
	(132, 15, '05631328', 1574171255),
	(133, 15, '18650808', 1574171302),
	(134, 15, '48420844', 1574171969),
	(135, 15, '22844686', 1574172124),
	(136, 15, '61610081', 1574172148),
	(137, 15, '81508562', 1574172246),
	(138, 15, '05054005', 1574172285),
	(139, 15, '66726713', 1574172314),
	(140, 15, '76672328', 1574172454),
	(141, 15, '46456220', 1574172827),
	(142, 15, '45287232', 1574172926),
	(143, 15, '12125231', 1574172963),
	(144, 15, '37886786', 1574172970),
	(145, 8, '33562210', 1574173026),
	(146, 15, '07100503', 1574173054),
	(147, 15, '75155447', 1574173325),
	(148, 15, '52747173', 1574173569),
	(149, 15, '30351556', 1574173574),
	(150, 15, '88420086', 1574173578),
	(151, 15, '50075452', 1574173664),
	(152, 15, '62441060', 1574173754),
	(153, 15, '18116171', 1574173802),
	(154, 15, '11821874', 1574173895),
	(155, 15, '31220851', 1574181073);
/*!40000 ALTER TABLE `user_otp_used` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_setting
CREATE TABLE IF NOT EXISTS `user_setting` (
  `user_id` int(11) NOT NULL,
  `settings_id` int(11) NOT NULL,
  `setting_value` tinyint(11) NOT NULL DEFAULT '0',
  KEY `settings_id` (`settings_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_setting_settings` FOREIGN KEY (`settings_id`) REFERENCES `settings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_user_setting_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_setting: ~9 rows (ungefähr)
/*!40000 ALTER TABLE `user_setting` DISABLE KEYS */;
INSERT INTO `user_setting` (`user_id`, `settings_id`, `setting_value`) VALUES
	(6, 1, 1),
	(8, 1, 0),
	(8, 2, 1),
	(15, 1, 0),
	(15, 2, 0),
	(16, 1, 0),
	(16, 2, 0),
	(4, 1, 1),
	(4, 2, 0);
/*!40000 ALTER TABLE `user_setting` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
