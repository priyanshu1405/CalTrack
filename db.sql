-- Active: 1670594712078@@127.0.0.1@3306@caltrack
create table nutrition(
    food_name VARCHAR(50) PRIMARY KEY,
    calories FLOAT,
    serving_size_g FLOAT,
    protein_g FLOAT,
    sodium_mg FLOAT,
    potassium_mg FLOAT,
    cholesterol_mg FLOAT,
    carbohydrates_total_g FLOAT,
    fiber_g FLOAT,
    suger_g FLOAT);

create table user(
    uname VARCHAR(50) PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50),
    dob DATE,
    gender VARCHAR(10),
    address VARCHAR(50),
    phone VARCHAR(50),
    medical_history VARCHAR(100),
    body_fat FLOAT,
    pass VARCHAR(50),
    reg_date DATE,
    email VARCHAR(50)
);

create Table mygoals(
    goal_id INT,
    target_weight FLOAT,
    activity_level VARCHAR(50),
    weight_gain_pace VARCHAR(50),
    uname VARCHAR(50),
    create_date DATE,
    FOREIGN KEY (uname) REFERENCES user(uname)
);

Alter Table mygoals ADD PRIMARY KEY(goal_id, uname);

create Table healthreport(
    reportid INT,weight FLOAT,height FLOAT,bmi FLOAT,uname VARCHAR(50),create_date DATE,
    FOREIGN KEY (uname) REFERENCES user(uname));

create table healthnote(
    note_day DATE, note varchar(200), uname varchar(50), color varchar(50), FOREIGN KEY (uname) REFERENCES user(uname)
);

Alter Table healthnote ADD PRIMARY KEY(note_day, uname);

create table meal(
    meal_id INT, meal_name VARCHAR(50), food_name VARCHAR(50), quantity FLOAT, uname VARCHAR(50), meal_date DATETIME,
    Foreign Key (uname) REFERENCES user(uname)
);

Alter Table meal ADD PRIMARY KEY(meal_id, uname);

alter table nutrition
add column fat_total_g float after carbohydrates_total_g;

alter table nutrition
add column fat_saturated_g float after carbohydrates_total_g;

select * from nutrition;

select * from meal where uname = 'Sai05';

select * from (meal)
where CAST(meal_date as date) = "2022-12-10";

desc user;

select * from user;

insert into meal
VALUES  (1, 1, 'egg', 23, 'Sai05', '2022-12-09 22:38:00');

desc healthnote;

desc nutrition;

select * from meal where uname = 'sai2';

select * from meal where uname = 'Sai05' and CAST(meal_date as date) = '2022-12-10'