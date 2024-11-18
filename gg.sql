CREATE DATABASE book_db;
Use book_db ;
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INT NOT NULL
);

INSERT INTO books (id,title, author, year) 
VALUES 
    (1,'To Kill a Mockingbird', 'Harper Lee', 1960),
    (2,'1984', 'George Orwell', 1949),
    (3,'The Great Gatsby', 'F. Scott Fitzgerald', 1925);
