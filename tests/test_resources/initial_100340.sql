create table if not exists employees
(
	id int,
	name varchar(50) null,
	salary bigint default 0 null,
	team_id int null
);

create table if not exists teams
(
	id int,
	name varchar(50) null
);


INSERT INTO teams (id, name) VALUES (1, 'shopping_operation');
INSERT INTO teams (id, name) VALUES (2, 'shopping_commercial');
INSERT INTO teams (id, name) VALUES (3, 'delivery');
INSERT INTO teams (id, name) VALUES (4, 'fulfillment');
INSERT INTO teams (id, name) VALUES (5, 'app');
INSERT INTO teams (id, name) VALUES (6, 'ollivander');
INSERT INTO teams (id, name) VALUES (7, 'finance');
INSERT INTO teams (id, name) VALUES (8, 'commercial');
INSERT INTO teams (id, name) VALUES (9, 'marketplace');
INSERT INTO teams (id, name) VALUES (10, 'ad_service');

INSERT INTO employees (id, name, salary, team_id) VALUES (1, 'nima', 20000, 1);
INSERT INTO employees (id, name, salary, team_id) VALUES (2, 'shayan', 10000, 1);
INSERT INTO employees (id, name, salary, team_id) VALUES (3, 'akbar', 15000, 6);
INSERT INTO employees (id, name, salary, team_id) VALUES (4, 'ali', 50000, 2);
INSERT INTO employees (id, name, salary, team_id) VALUES (5, 'andersson', 40000, 1);
INSERT INTO employees (id, name, salary, team_id) VALUES (6, 'alimohammad', 30000, 8);
INSERT INTO employees (id, name, salary, team_id) VALUES (7, 'alireza', 500, 1);
INSERT INTO employees (id, name, salary, team_id) VALUES (8, 'amirhassan', 35000, 3);
INSERT INTO employees (id, name, salary, team_id) VALUES (9, 'farzan', 35000, 3);
INSERT INTO employees (id, name, salary, team_id) VALUES (10, 'nahid', 35000, 2);
INSERT INTO employees (id, name, salary, team_id) VALUES (11, 'afzoun', 45000, 4);
INSERT INTO employees (id, name, salary, team_id) VALUES (12, 'mohammad', 45000, 4);
INSERT INTO employees (id, name, salary, team_id) VALUES (13, 'reza', 45000, 5);
INSERT INTO employees (id, name, salary, team_id) VALUES (14, 'amin', 10000, 5);
INSERT INTO employees (id, name, salary, team_id) VALUES (15, 'kazem', 50000, 5);
INSERT INTO employees (id, name, salary, team_id) VALUES (16, 'soheil', 60000, 6);
INSERT INTO employees (id, name, salary, team_id) VALUES (17, 'hadi', 20000, 2);
INSERT INTO employees (id, name, salary, team_id) VALUES (19, 'danial', 25000, 10);
INSERT INTO employees (id, name, salary, team_id) VALUES (20, 'osame', 30000, 3);
INSERT INTO employees (id, name, salary, team_id) VALUES (21, 'mahsa', 55000, 1);
INSERT INTO employees (id, name, salary, team_id) VALUES (22, 'niloufar', 22500, 8);
INSERT INTO employees (id, name, salary, team_id) VALUES (24, 'hamid', 12500, 8);
