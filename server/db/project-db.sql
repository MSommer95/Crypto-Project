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

-- Exportiere Daten aus Tabelle project.settings: ~1 rows (ungefähr)
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.users: ~6 rows (ungefähr)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `email`, `password`) VALUES
	(1, 'test@mail.de', '123'),
	(2, 'test2@mail.de', '5132'),
	(3, 'max@web.de', 'abc'),
	(4, 'Test@test', 'a6906caa2528d9c60122a82f4d9de1832e0cace9c325f5d9d996fee11ed722ecd2b350401c89b9d1ba2d7faa41d184a3cf56ebe799ec0ff3bde074f789860e514e2ccc2d990b929a4f3e9350dc8269d74feff7aa634e950bd8cb5e3086eccfe0'),
	(5, 'test@me.de', '624082f6e5546ad8a12bc8f75acd795b60da291700686711bbd652b12c4ab28255afe96f159d8f1739137ceb25dd2e02fcd943931bf85f6bd9e3d3fdeee7d5dfe75678459c2846cfc696cce5cb1d8ba933cdf36c730c88804e42a433ec5b2c9e'),
	(6, 'zonaafa@web.de', 'e9fa407622d249111c65190d40fbc1107937ad8fc5e7e5d9ac14de64f00e8e22c340de148469e5097c0857f9c40c41ada366d1986b4c16047d6500a0ebf71d9512a3e4698ee32dbb3f15809345c7b0b47c2dc84918e3a103ea4b4c7494857203');
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
  `user_id` int(11) NOT NULL,
  `current_otp` varchar(50) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_otp_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_otp: ~1 rows (ungefähr)
/*!40000 ALTER TABLE `user_otp` DISABLE KEYS */;
INSERT INTO `user_otp` (`user_id`, `current_otp`, `timestamp`) VALUES
	(6, '71771509', 1570811729);
/*!40000 ALTER TABLE `user_otp` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle project.user_setting
CREATE TABLE IF NOT EXISTS `user_setting` (
  `user_id` int(11) NOT NULL,
  `settings_id` int(11) NOT NULL,
  `setting_value` tinyint(11) NOT NULL DEFAULT '0',
  KEY `settings_id` (`settings_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FK_user_setting_settings` FOREIGN KEY (`settings_id`) REFERENCES `settings` (`id`),
  CONSTRAINT `user_setting_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exportiere Daten aus Tabelle project.user_setting: ~1 rows (ungefähr)
/*!40000 ALTER TABLE `user_setting` DISABLE KEYS */;
INSERT INTO `user_setting` (`user_id`, `settings_id`, `setting_value`) VALUES
	(6, 1, 1);
/*!40000 ALTER TABLE `user_setting` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
