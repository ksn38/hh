delete from py040121 where val < 10;
create table py151120 (id serial, tag varchar, val float);
delete from py151120 where val < 10;
create table pyres040121 (id serial, tag varchar, val float);
delete from pyres040121 where val < 100;
create table pyres151120 (id serial, tag varchar, val float);
delete from pyres151120 where val < 100;

create table ds040121 (id serial, tag varchar, val float);
delete from ds040121 where val < 10;
create table ds151120 (id serial, tag varchar, val float);
delete from ds151120 where val < 10;
create table dsres040121 (id serial, tag varchar, val float);
delete from dsres040121 where val < 70;
create table dsres151120 (id serial, tag varchar, val float);
delete from dsres151120 where val < 70;

create table js040121 (id serial, tag varchar, val float);
delete from js040121 where val < 10;
create table js151120 (id serial, tag varchar, val float);
delete from js151120 where val < 10;
create table jsres040121 (id serial, tag varchar, val float);
delete from jsres040121 where val < 50;
create table jsres151120 (id serial, tag varchar, val float);
delete from jsres151120 where val < 50;

create table php040121 (id serial, tag varchar, val float);
delete from php040121 where val < 10;
create table php151120 (id serial, tag varchar, val float);
delete from php151120 where val < 10;
create table phpres040121 (id serial, tag varchar, val float);
delete from phpres040121 where val < 50;
create table phpres151120 (id serial, tag varchar, val float);
delete from phpres151120 where val < 50;

create table js200720 (id serial, tag varchar, val float);
delete from js200720 where val < 10;
create table js101020 (id serial, tag varchar, val float);
delete from js101020 where val < 10;


select p.tag, round((p.val/(select max(val) from py040121))*100) from py040121 p;
select p.tag, round((p.val/(select max(val) from py040121))*100) from py151120 p;

select p.tag, round((p.val/(select max(val) from py040121))*100) as rang, 
round(((p.val/(select max(val) from py040121))/(p2.val/(select max(val) from py151120)) - 1)*100) as r_r_old
from py040121 p 
left join py151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from pyres040121))*100) as rang, 
round(((p.val/(select max(val) from pyres040121))/(p2.val/(select max(val) from pyres151120)) - 1)*100) as r_r_old
from pyres040121 p 
left join pyres151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from ds040121))*100) as rang, 
round(((p.val/(select max(val) from ds040121))/(p2.val/(select max(val) from ds151120)) - 1)*100) as r_r_old
from ds040121 p 
left join ds151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from dsres040121))*100) as rang, 
round(((p.val/(select max(val) from dsres040121))/(p2.val/(select max(val) from dsres151120)) - 1)*100) as r_r_old
from dsres040121 p 
left join dsres151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from js040121))*100) as rang, 
round(((p.val/(select max(val) from js040121))/(p2.val/(select max(val) from js151120)) - 1)*100) as r_r_old
from js040121 p 
left join js151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from jsres040121))*100) as rang, 
round(((p.val/(select max(val) from jsres040121))/(p2.val/(select max(val) from jsres151120)) - 1)*100) as r_r_old
from jsres040121 p 
left join jsres151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from php040121))*100) as rang, 
round(((p.val/(select max(val) from php040121))/(p2.val/(select max(val) from php151120)) - 1)*100) as r_r_old
from php040121 p 
left join php151120 p2 
on p.tag = p2.tag order by rang desc;

select p.tag, round((p.val/(select max(val) from phpres040121))*100) as rang, 
round(((p.val/(select max(val) from phpres040121))/(p2.val/(select max(val) from phpres151120)) - 1)*100) as r_r_old
from phpres040121 p 
left join phpres151120 p2 
on p.tag = p2.tag order by rang desc;

truncate js040121;
truncate js151120;

create view top200720 as
select 'Angular' as name, sum(val) from js200720 j where tag like 'Angular%'
union
select 'React' as name, sum(val) from js200720 j where tag like 'React%'
union
select 'Vue' as name, sum(val) from js200720 j where tag like 'Vue%'
union
select 'jQuery' as name, sum(val) from js200720 j where tag like 'jQuery';

create view top101020 as
select 'Angular' as name, sum(val) from js101020 j where tag like 'Angular%'
union
select 'React' as name, sum(val) from js101020 j where tag like 'React%'
union
select 'Vue' as name, sum(val) from js101020 j where tag like 'Vue%'
union
select 'jQuery' as name, sum(val) from js101020 j where tag like 'jQuery';

create view top151120 as
select 'Angular' as name, sum(val) from js151120 j where tag like 'Angular%'
union
select 'React' as name, sum(val) from js151120 j where tag like 'React%'
union
select 'Vue' as name, sum(val) from js151120 j where tag like 'Vue%'
union
select 'jQuery' as name, sum(val) from js151120 j where tag like 'jQuery';

drop view if exists top040121;
create view top040121 as
select 'Angular' as name, sum(val) from js040121 j where tag like 'Angular%'
union
select 'React' as name, sum(val) from js040121 j where tag like 'React%'
union
select 'Vue' as name, sum(val) from js040121 j where tag like 'Vue%'
union
select 'jQuery' as name, sum(val) from js040121 j where tag like 'jQuery';

select t1.name, round((t4.sum/(select max(t4.sum) from top200720 t4))*100) as date_200720,
round((t3.sum/(select max(t3.sum) from top101020 t3))*100) as date_101020, 
round((t2.sum/(select max(t2.sum) from top151120 t2))*100) as date_151120, 
round((t1.sum/(select max(t1.sum) from top040121 t1))*100)  as date_040121 from top040121 t1
left join top151120 t2
on t1.name = t2.name
left join top101020 t3
on t1.name = t3.name
left join top200720 t4
on t1.name = t4.name;

select * from top040121 t1;
select * from js040121 t1 order by tag;

