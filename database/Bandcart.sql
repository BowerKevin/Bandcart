-- ####################################
-- Table structure for 'Bands' table ##
-- ####################################
drop table if exists `Bands`;
create table `Bands` (
    `bandID` int(11) NOT NULL AUTO_INCREMENT,
    `bandName` varchar(255) NOT NULL,
    `numMembers` int(11),
    `genre` varchar(255),
    PRIMARY KEY(`bandID`)
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `Bands` (`bandName`, `numMembers`, `genre` ) VALUES (
   'Radiohead', 5, 'Progressive Rock / Experimental' 
);

-- #####################################
-- Table structure for 'Events' table ##
-- #####################################
drop table if exists `Events`;
create table `Events` (
    `eventID` int(11) NOT NULL AUTO_INCREMENT,
    `eventName` varchar(255) NOT NULL,
    `eventDate` datetime NOT NULL,
    `eventType` varchar(255) NOT NULL,
    `eventLocation` varchar(255) NOT NULL,
    `eventCity` varchar(255) NOT NULL,
    `eventState` varchar(255) NOT NULL,
    PRIMARY KEY(`eventID`)
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `Events` (`eventName`, `eventDate`, `eventType`,
 `eventLocation`, `eventCity`, `eventState` ) VALUES (
   'Forecastle Festival', '2015-11-05 13:43:16', 'tour', 'Louisville', 'Los', 'KY'
);

-- ########################################
-- Table structure for 'Customers' table ##
-- ########################################
drop table if exists `Customers`;
create table bandcart.`Customers` (
    `customerID` int(11) NOT NULL AUTO_INCREMENT,
    `customerFirst` varchar(255) NOT NULL,
    `customerLast` datetime NOT NULL,
    `customerDoB` varchar(255) NOT NULL,
    `phoneNum` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `eventID` int(11),
    PRIMARY KEY(`customerID`),
    CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`eventID`) references `Events` (`eventID`) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;