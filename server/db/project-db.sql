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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.settings: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` (`id`, `description`) VALUES
	(1, '2FA');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.users: ~5 rows (ungefähr)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `email`, `password`) VALUES
	(4, 'Test@test', 'a6906caa2528d9c60122a82f4d9de1832e0cace9c325f5d9d996fee11ed722ecd2b350401c89b9d1ba2d7faa41d184a3cf56ebe799ec0ff3bde074f789860e514e2ccc2d990b929a4f3e9350dc8269d74feff7aa634e950bd8cb5e3086eccfe0'),
	(5, 'test@me.de', '624082f6e5546ad8a12bc8f75acd795b60da291700686711bbd652b12c4ab28255afe96f159d8f1739137ceb25dd2e02fcd943931bf85f6bd9e3d3fdeee7d5dfe75678459c2846cfc696cce5cb1d8ba933cdf36c730c88804e42a433ec5b2c9e'),
	(6, 'zonaafa@web.de', 'e9fa407622d249111c65190d40fbc1107937ad8fc5e7e5d9ac14de64f00e8e22c340de148469e5097c0857f9c40c41ada366d1986b4c16047d6500a0ebf71d9512a3e4698ee32dbb3f15809345c7b0b47c2dc84918e3a103ea4b4c7494857203'),
	(8, 'max.sommer_95@web.de', 'ca2681e47edcda6a0894d28ba3e4fae805d7309c69dbd4f1715067e7485a0a85b6b5469fb92509e00d0e3681bd48bcfe2ddf6d6425e891e4a0523b138d1c426da5a4d75fb2c4312091f8c7af8121596cc90f8b60ed71bc79b9f3db268c61a7eb');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_data
CREATE TABLE IF NOT EXISTS `user_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `path` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_user_data_users` (`user_id`),
  CONSTRAINT `FK_user_data_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_data: ~0 rows (ungefähr)
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
  CONSTRAINT `FK_user_device_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_device: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `user_device` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_device` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_key
CREATE TABLE IF NOT EXISTS `user_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `key` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_user_key_users` (`user_id`),
  CONSTRAINT `FK_user_key_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_key: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `user_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_key` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_otp
CREATE TABLE IF NOT EXISTS `user_otp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `current_otp` varchar(50) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_otp: ~1 rows (ungefähr)
/*!40000 ALTER TABLE `user_otp` DISABLE KEYS */;
INSERT INTO `user_otp` (`id`, `user_id`, `current_otp`, `timestamp`) VALUES
	(32, 8, '38436633', 1572619535);
/*!40000 ALTER TABLE `user_otp` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_otp_used
CREATE TABLE IF NOT EXISTS `user_otp_used` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `used_otp` varchar(50) NOT NULL,
  `timestamp` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_used_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COMMENT='used OTPs go in here';

-- Exportiere Daten aus Tabelle project.user_otp_used: ~31 rows (ungefähr)
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
	(32, 8, '38436633', 1572619535);
/*!40000 ALTER TABLE `user_otp_used` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_setting
CREATE TABLE IF NOT EXISTS `user_setting` (
  `user_id` int(11) NOT NULL,
  `settings_id` int(11) NOT NULL,
  `setting_value` tinyint(11) NOT NULL DEFAULT '0',
  KEY `settings_id` (`settings_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_setting_settings` FOREIGN KEY (`settings_id`) REFERENCES `settings` (`id`),
  CONSTRAINT `FK_user_setting_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_setting: ~2 rows (ungefähr)
/*!40000 ALTER TABLE `user_setting` DISABLE KEYS */;
INSERT INTO `user_setting` (`user_id`, `settings_id`, `setting_value`) VALUES
	(6, 1, 1),
	(8, 1, 1);
/*!40000 ALTER TABLE `user_setting` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
