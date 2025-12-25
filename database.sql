DROP DATABASE IF EXISTS narratio;
CREATE DATABASE narratio;
USE narratio;

/*-------------------------------------------------------------------------------------*/

CREATE TABLE user(
    userid INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255)
);

DELIMITER $$
CREATE PROCEDURE get_a_user_by_id(
    IN myuserid INTEGER
)
BEGIN
    SELECT userid, username, password FROM user WHERE userid = myuserid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE get_a_user_by_username(
    IN myusername VARCHAR(255)
)
BEGIN
    SELECT userid, username, password FROM user WHERE username = myusername;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE create_new_user(
    IN myusername VARCHAR(255),
    IN mypassword VARCHAR(255)
)
BEGIN
    INSERT INTO user (username, password) VALUES (myusername, mypassword);
END $$
DELIMITER ;

/*-------------------------------------------------------------------------------------*/

CREATE TABLE code(
    codeid INTEGER PRIMARY KEY AUTO_INCREMENT,
    codename VARCHAR(255) UNIQUE,
    description TEXT,
    filetype ENUM('txt', 'mp3'),
    language ENUM('en', 'es') DEFAULT 'en'
);

DELIMITER $$
CREATE PROCEDURE get_codes_with_pagination(
    IN mycodename VARCHAR(255),
    IN mypage INTEGER
)
BEGIN
    DECLARE mylimit INTEGER DEFAULT 5;
    DECLARE myoffset INTEGER DEFAULT (mypage - 1) * mylimit;
    SELECT codeid, codename FROM code WHERE codename LIKE CONCAT('%', mycodename, '%') ORDER BY codeid ASC LIMIT mylimit OFFSET myoffset;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE get_a_code(
    IN mycodeid INTEGER
)
BEGIN
    SELECT codeid, codename, description, filetype, language FROM code WHERE codeid = mycodeid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE create_new_code(
    IN mycodename VARCHAR(255),
    IN mydescription TEXT,
    IN myfiletype ENUM('txt', 'mp3'),
    IN mylanguage ENUM('en', 'es')
)
BEGIN
    DECLARE mycodeid INTEGER DEFAULT 0;
    INSERT INTO code (codename, description, filetype, language) VALUES (mycodename, mydescription, myfiletype, mylanguage);
    SET mycodeid = last_insert_id();
    SELECT mycodeid AS codeid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE update_code(
    IN mycodeid INTEGER,
    IN mycodename VARCHAR(255),
    IN mydescription TEXT,
    IN myfiletype ENUM('txt', 'mp3'),
    IN mylanguage ENUM('en', 'es')
)
BEGIN
    UPDATE code SET codename = mycodename, description = mydescription, filetype = myfiletype, language = mylanguage WHERE codeid = mycodeid;
    SELECT mycodeid AS codeid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE destroy_qrcode(
    IN mycodeid INTEGER
)
BEGIN
    SELECT mycodeid AS codeid;
    DELETE FROM code WHERE codeid = mycodeid;
END $$
DELIMITER ;

/*-------------------------------------------------------------------------------------*/
