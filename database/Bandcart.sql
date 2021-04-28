-- ####################################
-- Table structure for 'Bands' table ##
-- ####################################
drop table if exists `bands`;
create table `bands` (
    `bandID` int(11) NOT NULL AUTO_INCREMENT,
    `bandName` varchar(255) NOT NULL UNIQUE,
    `numMembers` int(11),
    `genre` varchar(255),
    PRIMARY KEY(`bandID`)
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `bands` (`bandName`, `numMembers`, `genre` ) VALUES (
   'Radiohead', 5, 'Progressive Rock / Experimental' 
);

-- #####################################
-- Table structure for 'Events' table ##
-- #####################################
drop table if exists `events`;
create table `events` (
    `eventID` int(11) NOT NULL AUTO_INCREMENT,
    `eventName` varchar(255) NOT NULL UNIQUE,
    `eventDate` datetime NOT NULL,
    `eventType` varchar(255) NOT NULL,
    `eventCity` varchar(255) NOT NULL,
    `eventState` varchar(255) NOT NULL,
    PRIMARY KEY(`eventID`)
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `events` (`eventName`, `eventDate`, `eventType`,
   `eventCity`, `eventState` ) VALUES (
   'Forecastle Festival', '2015-11-05 13:43:16', 'tour', 'Louisville', 'KY'
);

-- #####################################
-- Table structure for 'BandsEvents' table ##
-- #####################################
drop table if exists `bandsevents`;
create table `bandsevents` (
    `bandID` int(11),
    `eventID` int(11),
    PRIMARY KEY(`bandID`, `eventID`),
    CONSTRAINT `bandsevents_ibfk_1` FOREIGN KEY (`bandID`) references `bands` (`bandID`),
    CONSTRAINT `bandsevents_ibfk_2` FOREIGN KEY (`eventID`) references `events` (`eventID`)
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `bandsevents` (`bandID`, `eventID`) VALUES (
(SELECT bandID from bands where bandName = "Radiohead"),
(SELECT eventID from events where eventName = 'Forecastle Festival')
);

-- ########################################
-- Table structure for 'Customers' table ##
-- ########################################
drop table if exists `customers`;
create table `customers` (
    `customerID` int(11) NOT NULL AUTO_INCREMENT,
    `customerFirst` varchar(255) NOT NULL,
    `customerLast` varchar(255) NOT NULL,
    `customerDoB` date NOT NULL,
    `phoneNum` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    PRIMARY KEY(`customerID`),
    constraint full_name unique (`customerFirst`,`customerLast`,`customerDoB`)
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `customers` (`customerFirst`, `customerLast`, `customerDoB`, `phoneNum`, `email`) 
VALUES ('Kevin', 'Santi', '1996-03-11', '123-456-7890', 'fakemail@123.com'
);

-- ########################################
-- Table structure for 'Tickets' table ####
-- ########################################
drop table if exists `tickets`;
create table `tickets` (
    `ticketID` int(11) NOT NULL AUTO_INCREMENT,
    `orderDate` date NOT NULL,
    `price` float(20,2) NOT NULL,
    `numTickets` int(11) NOT NULL,
    `customerID` int(11),
    `eventID` int(11),
    PRIMARY KEY(`ticketID`),
    CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`customerID`) references `customers` (`customerID`) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`eventID`) references `events` (`eventID`) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

INSERT INTO `tickets` (`orderDate`, `price`, `numTickets`, `customerID`, `eventID`) VALUES (
'2021-04-27', '300.85', '5',
(SELECT customerID from customers where customerFirst = "Kevin" and customerLast ="Santi" and customerDoB="1996-03-11"),
(SELECT eventID from events where eventName = 'Forecastle Festival')
);