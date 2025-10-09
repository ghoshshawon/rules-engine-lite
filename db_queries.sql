CREATE DATABASE IF NOT EXISTS rules_engine_db;
USE rules_engine_db;



CREATE TABLE rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(50) NOT NULL UNIQUE, 
    decision VARCHAR(20),
    score_delta INT,
    reason VARCHAR(255)
);

CREATE TABLE conditions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(50),  
    condition_type ENUM('all','any'),
    op VARCHAR(10),
    left_path VARCHAR(100),
    right_value JSON,
    FOREIGN KEY (rule_id) REFERENCES rules(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE defaults (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_id VARCHAR(50),
    decision VARCHAR(20),
    base_score INT,
    FOREIGN KEY (rule_id) REFERENCES rules(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);