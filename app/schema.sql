-- CREATE DATABASE Library if not exists;
-- USE Library;
DROP TABLE IF EXISTS BOOKS;
CREATE TABLE BOOKS (
  bookID INT  PRIMARY KEY,
  title VARCHAR(60) ,
  authors VARCHAR(60) ,
  average_rating FLOAT ,
  isbn VARCHAR(13) ,
  isbn13 VARCHAR(13) ,
  language_code VARCHAR(3) ,
  num_pages INT ,
  ratings_count INT ,
  text_reviews_count INT ,
  publication_date DATE ,
  publisher VARCHAR(60) ,
  total_count INT ,
  available_count INT,
  rent_count INT
  );
INSERT INTO `books` (`bookID`, `title`, `authors`, `average_rating`, `isbn`, `isbn13`, `language_code`, `num_pages`, `ratings_count`, `text_reviews_count`, `publication_date`, `publisher`, `total_count`, `available_count`, `rent_count`) VALUES
(1, 'A Man Called Ove', 'Fredrik Backman', 4.5, '1476738017', '9781476738017', 'ENG', 337, 600, 300, '2012-08-01', 'Atria Books', 20, 20, 1);
INSERT INTO `books` (`bookID`, `title`, `authors`, `average_rating`, `isbn`, `isbn13`, `language_code`, `num_pages`, `ratings_count`, `text_reviews_count`, `publication_date`, `publisher`, `total_count`, `available_count`, `rent_count`) VALUES
(2, 'A Man Called Ove', 'Fredrik Backman', 4.5, '1476738017', '9781476738017', 'ENG', 337, 600, 300, '2012-08-01', 'Atria Books', 20, 20, 1);

DROP TABLE IF EXISTS MEMBERS;
CREATE TABLE MEMBERS(
  memberID INT  PRIMARY KEY,
  name VARCHAR(60) ,
  email VARCHAR(60) ,
  reg_date DATE  DEFAULT CURRENT_DATE,
  total_books_rented INT  DEFAULT 0,
  debt FLOAT  DEFAULT 0,
  amount_spent FLOAT  DEFAULT 0
  );
INSERT INTO `members` (`memberID`, `name`, `email`, `reg_date`, `total_books_rented`, `debt`, `amount_spent`) VALUES
(1, 'John Doe', 'john@jo.com','', 0, 0, 0);

DROP TABLE IF EXISTS RENT;
CREATE TABLE RENT(
  rentID INT PRIMARY KEY,
  memberID INT ,
  bookID INT ,
  day_fee FLOAT ,
  amount_paid FLOAT ,
  total_amount FLOAT ,
  rent_date DATE  DEFAULT CURRENT_DATE,
  return_date DATE ,
  FOREIGN KEY (memberID) REFERENCES MEMBERS(memberID),
  FOREIGN KEY (bookID) REFERENCES BOOKS(bookID)
  );
  INSERT INTO `rent` (`rentID`, `memberID`, `bookID`, `day_fee`, `amount_paid`, `total_amount`, `rent_date`, `return_date`) VALUES
(1, 1, 1, 1, 1, 1, '2019-01-01', '2019-01-01');