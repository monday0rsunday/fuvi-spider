CREATE USER 'fuvi'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON `fuvi`.* TO 'fuvi'@'localhost';
DROP DATABASE fuvi;
CREATE DATABASE IF NOT EXISTS fuvi CHARSET utf8;

USE fuvi;

CREATE TABLE IF NOT EXISTS category (
	id int PRIMARY KEY NOT NULL AUTO_INCREMENT
	, title varchar(64)
);

INSERT INTO category(id, title) VALUES(1, "Video");
INSERT INTO category(id, title) VALUES(2, "Image");
INSERT INTO category(id, title) VALUES(3, "Music");

CREATE TABLE IF NOT EXISTS item(
	id int PRIMARY KEY NOT NULL AUTO_INCREMENT
	, site varchar(255)
	, src varchar(255) UNIQUE
	, link varchar(512)
	, title varchar(1024)
	, sapo varchar(1024)
	, cover varchar(1024)
	, ctime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
	, cat_id int
	, FOREIGN KEY (cat_id) REFERENCES category(id)
);
