-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 17, 2018 at 04:54 AM
-- Server version: 10.1.28-MariaDB
-- PHP Version: 5.6.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qwiktix`
--

-- --------------------------------------------------------

--
-- Table structure for table `movie`
--

CREATE TABLE `movie` (
  `MovieID` int(11) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Studio` varchar(20) NOT NULL,
  `CoverImg` blob NOT NULL,
  `Genre` varchar(20) NOT NULL,
  `ReleaseDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `movieimages`
--

CREATE TABLE `movieimages` (
  `MovieID` int(11) NOT NULL,
  `MovieImageNum` int(11) NOT NULL,
  `Image` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `online`
--

CREATE TABLE `online` (
  `VendorID` int(11) NOT NULL,
  `URL` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

CREATE TABLE `person` (
  `PersonID` int(11) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `Picture` blob NOT NULL,
  `DOB` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `provides`
--

CREATE TABLE `provides` (
  `VendorID` int(11) NOT NULL,
  `MovieID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `MovieID` int(11) NOT NULL,
  `PersonID` int(11) NOT NULL,
  `Title` varchar(20) NOT NULL,
  `CharacterName` varchar(20) DEFAULT NULL,
  `AssocPic` blob
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `search`
--

CREATE TABLE `search` (
  `MovieID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `Love` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `streaming`
--

CREATE TABLE `streaming` (
  `OrderID` int(11) NOT NULL,
  `VendorID` int(11) NOT NULL,
  `ExpDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `theatre`
--

CREATE TABLE `theatre` (
  `VendorID` int(11) NOT NULL,
  `Street` varchar(20) NOT NULL,
  `City` varchar(20) NOT NULL,
  `Country` varchar(20) NOT NULL,
  `Postal` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `OrderID` int(11) NOT NULL,
  `VendorID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ticketnumbers`
--

CREATE TABLE `ticketnumbers` (
  `OrderID` int(11) NOT NULL,
  `TicketNum` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `UserID` int(11) NOT NULL,
  `Email` varchar(20) NOT NULL,
  `FName` varchar(20) NOT NULL,
  `LName` varchar(20) NOT NULL,
  `Password` char(60) NOT NULL,
  `Salt` char(29) NOT NULL,
  `Phone` varchar(10) NOT NULL,
  `City` varchar(20) NOT NULL,
  `Street` varchar(20) NOT NULL,
  `Country` varchar(20) NOT NULL,
  `Postal` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `userorder`
--

CREATE TABLE `userorder` (
  `OrderID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `MovieID` int(11) NOT NULL,
  `Total` double NOT NULL,
  `PurchaseDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `VendorID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `PricePerMovie` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movie`
--
ALTER TABLE `movie`
  ADD PRIMARY KEY (`MovieID`);

--
-- Indexes for table `movieimages`
--
ALTER TABLE `movieimages`
  ADD PRIMARY KEY (`MovieID`,`MovieImageNum`);

--
-- Indexes for table `online`
--
ALTER TABLE `online`
  ADD PRIMARY KEY (`VendorID`);

--
-- Indexes for table `person`
--
ALTER TABLE `person`
  ADD PRIMARY KEY (`PersonID`);

--
-- Indexes for table `provides`
--
ALTER TABLE `provides`
  ADD PRIMARY KEY (`VendorID`,`MovieID`),
  ADD KEY `ProvidesMovieID` (`MovieID`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`MovieID`,`PersonID`,`Title`),
  ADD KEY `RolePersonID` (`PersonID`);

--
-- Indexes for table `search`
--
ALTER TABLE `search`
  ADD PRIMARY KEY (`MovieID`,`UserID`),
  ADD KEY `SearchUserID` (`UserID`);

--
-- Indexes for table `streaming`
--
ALTER TABLE `streaming`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `StreamingVendorID` (`VendorID`);

--
-- Indexes for table `theatre`
--
ALTER TABLE `theatre`
  ADD PRIMARY KEY (`VendorID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `TicketVendorID` (`VendorID`);

--
-- Indexes for table `ticketnumbers`
--
ALTER TABLE `ticketnumbers`
  ADD PRIMARY KEY (`OrderID`,`TicketNum`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserID`);

--
-- Indexes for table `userorder`
--
ALTER TABLE `userorder`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `OrderUserID` (`UserID`),
  ADD KEY `OrderMovieID` (`MovieID`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`VendorID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movie`
--
ALTER TABLE `movie`
  MODIFY `MovieID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `person`
--
ALTER TABLE `person`
  MODIFY `PersonID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `userorder`
--
ALTER TABLE `userorder`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `vendor`
--
ALTER TABLE `vendor`
  MODIFY `VendorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `movieimages`
--
ALTER TABLE `movieimages`
  ADD CONSTRAINT `MovieImagesMovieID` FOREIGN KEY (`MovieID`) REFERENCES `movie` (`MovieID`);

--
-- Constraints for table `online`
--
ALTER TABLE `online`
  ADD CONSTRAINT `OnlineVendorID` FOREIGN KEY (`VendorID`) REFERENCES `vendor` (`VendorID`);

--
-- Constraints for table `provides`
--
ALTER TABLE `provides`
  ADD CONSTRAINT `ProvidesMovieID` FOREIGN KEY (`MovieID`) REFERENCES `movie` (`MovieID`),
  ADD CONSTRAINT `ProvidesVendorID` FOREIGN KEY (`VendorID`) REFERENCES `vendor` (`VendorID`);

--
-- Constraints for table `role`
--
ALTER TABLE `role`
  ADD CONSTRAINT `RoleMovieID` FOREIGN KEY (`MovieID`) REFERENCES `movie` (`MovieID`),
  ADD CONSTRAINT `RolePersonID` FOREIGN KEY (`PersonID`) REFERENCES `person` (`PersonID`);

--
-- Constraints for table `search`
--
ALTER TABLE `search`
  ADD CONSTRAINT `SearchMovieID` FOREIGN KEY (`MovieID`) REFERENCES `movie` (`MovieID`),
  ADD CONSTRAINT `SearchUserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);

--
-- Constraints for table `streaming`
--
ALTER TABLE `streaming`
  ADD CONSTRAINT `StreamingOrderID` FOREIGN KEY (`OrderID`) REFERENCES `userorder` (`OrderID`),
  ADD CONSTRAINT `StreamingVendorID` FOREIGN KEY (`VendorID`) REFERENCES `online` (`VendorID`);

--
-- Constraints for table `theatre`
--
ALTER TABLE `theatre`
  ADD CONSTRAINT `TheatreVendorID` FOREIGN KEY (`VendorID`) REFERENCES `vendor` (`VendorID`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `TicketOrderID` FOREIGN KEY (`OrderID`) REFERENCES `userorder` (`OrderID`),
  ADD CONSTRAINT `TicketVendorID` FOREIGN KEY (`VendorID`) REFERENCES `theatre` (`VendorID`);

--
-- Constraints for table `ticketnumbers`
--
ALTER TABLE `ticketnumbers`
  ADD CONSTRAINT `TicketNumbersOrderID` FOREIGN KEY (`OrderID`) REFERENCES `ticket` (`OrderID`);

--
-- Constraints for table `userorder`
--
ALTER TABLE `userorder`
  ADD CONSTRAINT `OrderMovieID` FOREIGN KEY (`MovieID`) REFERENCES `movie` (`MovieID`),
  ADD CONSTRAINT `OrderUserID` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
