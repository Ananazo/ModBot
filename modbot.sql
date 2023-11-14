-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 14, 2023 at 08:50 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

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
-- Table structure for table `bans`
--

CREATE TABLE `bans` (
  `Date` varchar(255) NOT NULL,
  `Banner` varchar(255) NOT NULL,
  `Banned` varchar(255) NOT NULL,
  `Reason` varchar(255) NOT NULL,
  `Duration` varchar(255) NOT NULL,
  `Guild` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clemess`
--

CREATE TABLE `clemess` (
  `Date` varchar(255) NOT NULL,
  `Server` varchar(255) NOT NULL,
  `Channel` varchar(255) NOT NULL,
  `Deleter` varchar(255) NOT NULL,
  `Count` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `Date` varchar(255) NOT NULL,
  `Giver` varchar(255) NOT NULL,
  `Feedback` varchar(2555) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `guilds`
--

CREATE TABLE `guilds` (
  `guild` varchar(255) NOT NULL,
  `testh` varchar(255) NOT NULL,
  `warn_count` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kicks`
--

CREATE TABLE `kicks` (
  `Date` varchar(255) NOT NULL,
  `Kicker` varchar(255) NOT NULL,
  `Kicked` varchar(255) NOT NULL,
  `Reason` varchar(255) NOT NULL,
  `Guild` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `warns`
--

CREATE TABLE `warns` (
  `Date` varchar(255) NOT NULL,
  `Warner` varchar(255) NOT NULL,
  `Warned` varchar(255) NOT NULL,
  `Reason` varchar(255) NOT NULL,
  `Guild` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bans`
--
ALTER TABLE `bans`
  ADD PRIMARY KEY (`Date`);

--
-- Indexes for table `clemess`
--
ALTER TABLE `clemess`
  ADD PRIMARY KEY (`Date`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`Date`);

--
-- Indexes for table `guilds`
--
ALTER TABLE `guilds`
  ADD PRIMARY KEY (`guild`);

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
