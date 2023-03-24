-- create duplicate database (run on cmd)
-- mysqldump yourFirstDatabase -u username -p > yourDatabase.sql
-- mysql yourSecondDatabase -u username -p< yourDatabase.sql
-- example
-- mysqldump btp -u username -p > btp.sql
-- mysql duplicatebtp -u username -p < btp.sql

use btp;
select * from user_attributes;
select * from user_aval; -- where user_attribute_id = 3;
select * from user;
select * from user_details order by user_id, user_attribute_id;

insert into user_aval values(2, 'School');

delete from policy_user_aval where policy_id > 5;
delete from policy_resource_aval where policy_id > 5;
delete from policy where policy_id > 5;
insert into policy values(6, 2);
insert into policy_user_aval values(6, 2, 'ME');
insert into policy_resource_aval values(6, 2, 'ME');
insert into policy values(7, 1);
insert into policy_user_aval values(7, 5, 'School');
insert into policy_resource_aval values(7, 2, 'ME');
insert into policy_env_aval values(7, 3, '1');
delete from policy_env_aval;
insert into policy values(8, 3);
insert into policy_user_aval values(8, 5, 'SchoolOfEngineering');
insert into policy_user_aval values(8, 3, 'AssistantDean');
insert into policy_resource_aval values(8, 2, 'ME');

select * from policy join operations on policy.operation_id = operations.operation_id;
select * from policy_user_aval;
select * from policy_resource_aval;
select * from policy_env_aval;
select * from policy;
select * from operations;

select * from env_attributes;
select * from env_attributes join env_aval on env_attributes.env_attribute_id = env_aval.env_attribute_id;
insert into env_attributes values (3, 'otp_required');
update env_attributes set env_attribute = 'office_hours' where env_attribute_id = 2;