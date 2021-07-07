-- Section1
Insert into Player(id, team, age)
Select t.id, 'Chelsea', 24
From (
	select id from Person where id not in (
		select id from Player
		union
		select id from Coach
		union
		select id from Refree
	)
) as t
-- Section2
Select id, name
From Person
Where id in (
	select c.id
	from Coach as c
	left join Player as p
	on p.id=c.id
	where p.team != c.team
)
-- Section3
Alter Table Player
ADD FOREIGN KEY (team) REFERENCES Team(name) ON DELETE CASCADE