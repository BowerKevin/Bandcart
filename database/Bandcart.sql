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