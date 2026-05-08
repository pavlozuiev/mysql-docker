USE my_database;

CREATE TABLE IF NOT EXISTS titanic (
    PassengerId INT PRIMARY KEY,
    Survived INT,
    Pclass INT,
    Name VARCHAR(255),
    Sex VARCHAR(50),
    Age FLOAT,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(100),
    Fare FLOAT,
    Cabin VARCHAR(100),
    Embarked VARCHAR(10)
);

LOAD DATA INFILE '/var/lib/mysql-files/titanic.csv'
INTO TABLE titanic
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(PassengerId, Survived, Pclass, Name, Sex, @v_Age, SibSp, Parch, Ticket, Fare, @v_Cabin, @v_Embarked)
SET 
    Age = NULLIF(@v_Age, ''),
    Cabin = NULLIF(@v_Cabin, ''),
    -- Використовуємо TRIM для уникнення проблем із символами перенесення рядка (\r) в кінці
    Embarked = NULLIF(TRIM(TRAILING '\r' FROM @v_Embarked), '');