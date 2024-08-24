CREATE DATABASE lost_and_found;

USE lost_and_found;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE lost_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_description TEXT NOT NULL,
    item_image LONGBLOB NOT NULL,
    date_lost DATE NOT NULL,
    location_lost VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE found_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    finder_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_description TEXT NOT NULL,
    item_image LONGBLOB NOT NULL,
    date_found DATE NOT NULL,
    location_found VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    FOREIGN KEY (finder_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE claimed_items (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_description TEXT NOT NULL,
    item_image LONGBLOB NOT NULL,
    date_lost DATE NOT NULL,
    location_lost VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    claimed_by INT,
    claim_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (claimed_by) REFERENCES users(user_id) ON DELETE CASCADE
);

ALTER TABLE found_items ADD user_id INT;

select * from users;
select * from lost_items;
select * from found_items;
select * from claimed_items;

-- which user lost what
SELECT
    users.username AS user_name,
    lost_items.item_name,
    lost_items.item_description,
    lost_items.date_lost,
    lost_items.location_lost,
    lost_items.contact_info
FROM
    users
JOIN
    lost_items ON users.user_id = lost_items.user_id;
    
    
    
CREATE VIEW user_lost_items AS
SELECT
    users.username AS user_name,
    lost_items.item_name,
    lost_items.item_description,
    lost_items.date_lost,
    lost_items.location_lost,
    lost_items.contact_info
FROM
    users
JOIN
    lost_items ON users.user_id = lost_items.user_id;

SELECT * FROM user_lost_items;



