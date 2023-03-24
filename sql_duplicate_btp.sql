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
select * from user_details;
select * from resource; 
select * from resource_details; 
select * from policy;
delete from policy where policy_id >= 100;
delete from policy_user_aval where policy_id >= 100;
delete from policy_resource_aval where policy_id >= 100;
delete from policy_env_aval where policy_id >= 100;
select * from policy_env_aval; 
show tables;



SET GLOBAL FOREIGN_KEY_CHECKS=0;
SET GLOBAL FOREIGN_KEY_CHECKS=1;