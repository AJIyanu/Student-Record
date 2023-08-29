-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS Student_Record;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'mesacot';
GRANT ALL PRIVILEGES ON `Student_Record`.* TO 'admin'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
