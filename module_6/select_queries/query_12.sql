-- 12 Оцінки студентів у певній групі з певного предмета на останньому занятті --
select  s."name" as student, 
		g2."name" as  group_name, 
		s2."name" as subject, 
		g.grade,
		g.grade_date as last_date
from grades g
join students s on s.id = g.student_id
join subjects s2 on s2.id = g.subject_id
join "groups" g2 on g2.id = s.group_id
where
	g2.id = 3 and
	s2."name" = 'Mathematic' and
	g.grade_date = (select max(g3.grade_date) from grades g3) 
group by s."name", g2."name", s2."name", g.grade, g.grade_date