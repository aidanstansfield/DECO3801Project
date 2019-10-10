CREATE DATABASE IF NOT EXISTS ipwdatabase;
USE ipwdatabase;

-- Table for people who are registering their interest 
CREATE TABLE IF NOT EXISTS registerd (
    uid     int             not null    auto increment,
    name    varchar(255)    not null
    email   varchar(255)    not null
);
