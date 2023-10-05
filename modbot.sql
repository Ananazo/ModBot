-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 05, 2023 at 09:17 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `modbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `clemess`
--

CREATE TABLE `clemess` (
  `Date` varchar(255) NOT NULL,
  `Channel` varchar(255) NOT NULL,
  `Deleter` varchar(255) NOT NULL,
  `Count` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Dumping data for table `clemess`
--

INSERT INTO `clemess` (`Date`, `Channel`, `Deleter`, `Count`) VALUES
('2023-10-05 09:48:52.134767', '1158488964785786882', '429911513952944129', '2');

-- --------------------------------------------------------

--
-- Table structure for table `dm`
--

CREATE TABLE `dm` (
  `Date` varchar(255) NOT NULL,
  `Sender` varchar(255) NOT NULL,
  `Reciver` varchar(255) NOT NULL,
  `Content` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Dumping data for table `dm`
--

INSERT INTO `dm` (`Date`, `Sender`, `Reciver`, `Content`) VALUES
('2023-10-05 10:04:23.244610', '429911513952944129', 'ananazzo#0', 'j');

-- --------------------------------------------------------

--
-- Table structure for table `kicks`
--

CREATE TABLE `kicks` (
  `Date` varchar(255) NOT NULL,
  `Warner` varchar(255) NOT NULL,
  `Warned` varchar(255) NOT NULL,
  `Reason` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warns`
--

CREATE TABLE `warns` (
  `Date` varchar(255) NOT NULL,
  `Warner` varchar(255) NOT NULL,
  `Warned` varchar(255) NOT NULL,
  `Reason` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Dumping data for table `warns`
--

INSERT INTO `warns` (`Date`, `Warner`, `Warned`, `Reason`) VALUES
('2023-10-05 10:10:22.916239', '429911513952944129', 'ananazzo#0', '6'),
('2023-10-05 10:10:55.545628', '429911513952944129', 'ananazzo#0', 'b'),
('2023-10-05 10:11:44.954871', '429911513952944129', 'ananazzo#0', 'hk');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clemess`
--
ALTER TABLE `clemess`
  ADD PRIMARY KEY (`Date`);

--
-- Indexes for table `dm`
--
ALTER TABLE `dm`
  ADD PRIMARY KEY (`Date`);

--
-- Indexes for table `kicks`
--
ALTER TABLE `kicks`
  ADD PRIMARY KEY (`Date`);

--
-- Indexes for table `warns`
--
ALTER TABLE `warns`
  ADD PRIMARY KEY (`Date`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
