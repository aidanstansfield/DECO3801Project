-- This script will initialise the MySQL database
-- and associated tables for the TeamBuilder
-- application.

CREATE DATABASE IF NOT EXISTS tbdatabase;
USE tbdatabase;

-- We need to store the users for the system.
CREATE TABLE IF NOT EXISTS users (
    uid     varchar(255)    not null,
    primary key (uid)
);

-- Each user can have many courses
CREATE TABLE IF NOT EXISTS courses (
    name    varchar(255)    not null,
    uid     varchar(255)    not null,
    PRIMARY KEY (name, uid)
    FOREIGN KEY (uid) REFERENCES users(uid)
);

-- Each course can have many allocations
-- An allocation only stores the constraints which
-- are set by the user since they can simply re-run
-- the allocator.
CREATE TABLE IF NOT EXISTS allocations (
    name    varchar(255)    not null,
    course  varchar(255)    not null,
    constraints TEXT,
    PRIMARY KEY (name, course)
    FOREIGN KEY (course) REFERENCES courses(name)
);
