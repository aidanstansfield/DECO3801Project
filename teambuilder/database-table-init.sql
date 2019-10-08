-- This script will initialise the MySQL database
-- and associated tables for the TeamBuilder
-- application.

CREATE DATABASE IF NOT EXISTS tbdatabase;
USE tbdatabase;

-- We need to store the users for the system.
CREATE TABLE IF NOT EXISTS users (
    uid     int             not null    auto increment,
    name    varchar(255)    not null,
    primary key (uid)
);

-- Each user can have many courses
-- Each course is uniquely identified by the
-- combination of user and course name. A course
-- can only have a single survey linked to it. 
-- Some courses don't have surveys.
CREATE TABLE IF NOT EXISTS courses (
    cid         int             not null,
    name        varchar(255)    not null,
    uid         int             not null,
    PRIMARY KEY (cid),
    FOREIGN KEY (uid) REFERENCES users(uid),
);

-- -- Each course can have many allocations
-- -- An allocation only stores the constraints which
-- -- are set by the user since they can simply re-run
-- -- the allocator.
-- CREATE TABLE IF NOT EXISTS allocations (
--     aid     int             not null    auto increment,
--     name    varchar(255)    not null,
--     course  int             not null,
--     constraints TEXT,
--     PRIMARY KEY (aid),
--     FOREIGN KEY (course) REFERENCES courses(cid)
-- );

-- Each course has many students which can be 
-- allocated
CREATE TABLE IF NOT EXISTS students (
    sid         int             not null    auto increment,
    name        varchar(255)    not null,
    cid         varchar(255)    not null,
    response    LONGTEXT,
    PRIMARY KEY (sid),
    FOREIGN KEY (cid) REFERENCES courses(cid)
    FOREIGN KEY (surveyid) REFERENCES courses(sid);
)

-- This table is an index of all of the questions
-- and their associated surveys.
--      question -> the actual question text
--      parameter -> the parameter being asked for (e.g. age)
CREATE TABLE IF NOT EXISTS questions (
    qid         int             not null    auto increment,
    cid         int             not null,
    question    TEXT            not null,
    parameter   varchar(255)    not null,
    PRIMARY KEY (qid),
    FOREIGN KEY (cid) REFERENCES courses(cid)
);

-- -- This table is an index of all of the responses
-- -- which have been received and their associated
-- -- questions
-- CREATE TABLE IF NOT EXISTS responses (
--     rid     int     not null    auto increment,
--     qid     int     not null,
--     PRIMARY KEY (rid),
--     FOREIGN KEY (qid) REFERENCES questions(qid)
-- );

-- -- This table is necessary to allow questions to
-- -- have multiple answers (e.g. multi-select questions)
-- CREATE TABLE IF NOT EXISTS questions_responses (
--     qid     int     not null,
--     rid     int     not null,
--     PRIMARY KEY (qid, rid),
--     FOREIGN KEY (qid) REFERENCES questions(qid),
--     FOREIGN KEY (rid) REFERENCES responses(rid)
-- );

-- -- This table stores the answers to questions asking
-- -- for integer answers (e.g. What is your age)
-- CREATE TABLE IF NOT EXISTS integer_responses (
--     qid     int     not null,
--     answer  int     not null
--     PRIMARY KEY (qid) REFERENCES questions(qid)
-- );

-- -- This table stores the answers to questions asking
-- -- for multi-select answers (e.g. Select your preferences)
-- CREATE TABLE IF NOT EXISTS multi_select_responses (
--     qid     int     not null,
--     answer  TEXT    not null,
--     PRIMARY KEY (qid) REFERENCES questions(qid)
-- );