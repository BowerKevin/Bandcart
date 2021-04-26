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
);