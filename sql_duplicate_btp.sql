-- create duplicate database (run on cmd)
-- mysqldump yourFirstDatabase -u username -p > yourDatabase.sql
-- mysql yourSecondDatabase -u username -p< yourDatabase.sql
-- example
-- mysqldump btp -u username -p > btp.sql
-- mysql duplicatebtp -u username -p < btp.sql
create database duplicatebtp;
create database tempbtp;
use tempbtp;
create table dummy(id int);
use duplicatebtp;
select * from user; 
delete from user where user_id >= 100;
update user_aval set user_attribute_id = 2 where user_val = 'SchoolOfBasicSciences';
select * from user_details;
select * from user_attributes;
select * from user_aval;
select * from user_values;
insert into user_details values 
select * from resource; 
select * from resource_details; 
select * from policy;
delete from policy where policy_id >= 100;
delete from policy_user_aval where policy_id >= 100;
delete from policy_resource_aval where policy_id >= 100;
delete from policy_env_aval where policy_id >= 100;
select * from policy_user_aval order by policy_id; 
select * from org; 
update org set org_name = 'Imperial College London' where org_id = 2;
update org set org_name = 'Stanford University' where org_id = 2;



SET GLOBAL FOREIGN_KEY_CHECKS=0;
SET GLOBAL FOREIGN_KEY_CHECKS=1;