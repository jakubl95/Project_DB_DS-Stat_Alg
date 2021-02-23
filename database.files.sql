CREATE DATABASE covid19;

use covid19;

CREATE TABLE country (
	id int PRIMARY KEY auto_increment,
	name varchar(255) UNIQUE,
	code varchar(2) UNIQUE,
	who_region varchar(10)
);

CREATE TABLE reported_cases (
	id int PRIMARY KEY auto_increment,
	country_id int,
	report_date DATE,
	cases int unsigned,
	deaths int unsigned
);

CREATE TABLE reported_cases_archive (
	id int PRIMARY KEY auto_increment,
	country_id int,
	report_date DATE,
	cases int unsigned,
	deaths int unsigned,
	delete_date date;
);

CREATE TABLE cases_monthly(
	id int PRIMARY KEY auto_increment,
	country_id int,
	year_index int,
	month_index int,
	cases int unsigned,
	deaths int unsigned
);
CREATE TABLE cases_quarterly(
	id int PRIMARY KEY auto_increment,
	country_id int,
	quarter_name varchar(6),
	quarter_year int,
	quarter_index int,
	cases int unsigned,
	deaths int unsigned
);
CREATE TABLE cases_yearly(
	id int PRIMARY KEY auto_increment,
	country_id int,
	year_index int,
	cases int unsigned,
	deaths int unsigned
);

ALTER TABLE reported_cases ADD FOREIGN KEY(country_id) REFERENCES country(id);
ALTER TABLE cases_monthly ADD FOREIGN KEY(country_id) REFERENCES country(id);
ALTER TABLE cases_quarterly ADD FOREIGN KEY(country_id) REFERENCES country(id);
ALTER TABLE cases_yearly ADD FOREIGN KEY(country_id) REFERENCES country(id);

alter table reported_cases add unique index(country_id, report_date);
alter table cases_monthly add unique index(country_id, year_index, month_index);
alter table cases_quarterly add unique index(country_id, quarter_year, quarter_index);
alter table cases_yearly add unique index(country_id, year_index);