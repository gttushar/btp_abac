-- Initial setup query
insert into user values(1, 'admin', 'admin', 'admin@iitkgp.ac.in', 'pbkdf2:sha256:150000$VrgqgfRJ$909e6663566b363f28acb758ed4808b87730e14f27491e444b0698e558b1667b');
insert into user_attributes values(1, 'user_type');
insert into user_aval values(1, 'admin');
insert into user_details values(1, 1, 'admin');
insert into operations values(1, 'read');
insert into operations values(2, 'write');
insert into operations values(3, 'modify');

-- List of all valid attributes
CREATE TABLE `env_attributes` ( env_attribute_id int PRIMARY KEY, `env_attribute` varchar(64));
CREATE TABLE `resource_attributes` ( resource_attribute_id int PRIMARY KEY, `resource_attribute` varchar(64));
CREATE TABLE `user_attributes` ( user_attribute_id int PRIMARY KEY, `user_attribute` varchar(64));

-- List of user values
CREATE TABLE `user_values` ( user_val_id int PRIMARY KEY, `user_val` varchar(64));
-- INSERT INTO `user_values` 
-- 	SELECT @rownum := @rownum + 1 AS user_val_id, t.user_val AS `user_val`
--   FROM (SELECT DISTINCT `user_val` FROM `user_aval` ORDER BY user_attribute_id, user_val) t, (SELECT @rownum := 0) r;

-- List of all valid attribute - value (aval) pairs
CREATE TABLE `env_aval` ( 
	env_attribute_id int, `env_val` varchar(64),  
	PRIMARY KEY (env_attribute_id,`env_val`),
	FOREIGN KEY (env_attribute_id) REFERENCES env_attributes(env_attribute_id));
CREATE TABLE `resource_aval` ( 
	resource_attribute_id int, `resource_val` varchar(64),  
	PRIMARY KEY (resource_attribute_id,`resource_val`),
	FOREIGN KEY (resource_attribute_id) REFERENCES resource_attributes(resource_attribute_id));
CREATE TABLE `user_aval` ( 
	user_attribute_id int, `user_val` varchar(64), 
	PRIMARY KEY (user_attribute_id,`user_val`),
	FOREIGN KEY (user_attribute_id) REFERENCES user_attributes(user_attribute_id));

-- User and user-avals
CREATE TABLE `user` (
	`user_id` int PRIMARY KEY,
	`user_name` varchar(64) NOT NULL,
	`login_name` varchar(64) NOT NULL,
	`password_hash` varchar(128) NOT NULL,
	`email` varchar(64) NOT NULL
);
CREATE TABLE `user_details` (
	`user_id` int,
	`user_attribute_id` int,
	`user_val` varchar(64) NOT NULL,
	PRIMARY KEY (`user_id`,`user_attribute_id`),
	FOREIGN KEY (`user_attribute_id`, `user_val`) REFERENCES user_aval(`user_attribute_id`, `user_val`)
);

-- Resource and resource-avals
CREATE TABLE `resource` (
	`resource_id` int PRIMARY KEY,
	`resource_name` varchar(128) NOT NULL
);
CREATE TABLE `resource_details` (
	`resource_id` int,
	`resource_attribute_id` int,
	`resource_val` varchar(64) NOT NULL,
	PRIMARY KEY (`resource_id`,`resource_attribute_id`),
	FOREIGN KEY (`resource_attribute_id`, `resource_val`) REFERENCES resource_aval(`resource_attribute_id`, `resource_val`)
);

-- Policy. Identified by policy_id and operation. Rules= AND of avals from respective subtables
CREATE TABLE operations (operation_id int PRIMARY KEY, operation_name varchar(16) NOT NULL);
CREATE TABLE policy ( 
	policy_id int PRIMARY KEY, operation_id int,
    FOREIGN KEY (operation_id) REFERENCES operations(operation_id)
);
CREATE TABLE policy_user_aval ( 
	policy_id int, `user_attribute_id` int, `user_val` varchar(64),
	PRIMARY KEY (policy_id, user_attribute_id, user_val),
	FOREIGN KEY (policy_id) REFERENCES policy(policy_id),
	FOREIGN KEY (user_attribute_id, user_val) REFERENCES user_aval(user_attribute_id, user_val)
);
CREATE TABLE policy_resource_aval ( 
	policy_id int, `resource_attribute_id` int, `resource_val` varchar(64),
	PRIMARY KEY (policy_id, resource_attribute, resource_val),
	FOREIGN KEY (policy_id) REFERENCES policy(policy_id),
	FOREIGN KEY (resource_attribute_id, resource_val) REFERENCES resource_aval(resource_attribute_id, resource_val)
);
CREATE TABLE policy_env_aval ( 
	policy_id int, `env_attribute_id` int, `env_val` varchar(64),
	PRIMARY KEY (policy_id, env_attribute_id, env_val),
	FOREIGN KEY (policy_id) REFERENCES policy(policy_id),
	FOREIGN KEY (env_attribute_id, env_val) REFERENCES env_aval(env_attribute_id, env_val)
);

CREATE TABLE `logs` (
	log_no int PRIMARY KEY,
	user_id int DEFAULT NULL, -- null for external user
	org_id int NOT NULL,
	resource_id int NOT NULL,
	operation_id int NOT NULL,
	decision char(1) NOT NULL,
	check (decision in ('y','n')),
	FOREIGN KEY (user_id) REFERENCES `user`(user_id),
	FOREIGN KEY (operation_id) REFERENCES `operations`(operation_id),
	FOREIGN KEY (resource_id) REFERENCES `resource`(resource_id),
	FOREIGN KEY (org_id) REFERENCES `org`(org_id)
);
-- Access time (day/night), access day(weekend/weekday), ip/subnet
CREATE TABLE logs_env (
	log_no int,
	env_attribute_id int,
	env_val varchar(64),
	PRIMARY KEY (log_no, env_attribute_id),
	FOREIGN KEY (env_attribute_id, env_val) REFERENCES env_aval(env_attribute_id, env_val)
);
CREATE TABLE logs_user_aval(
	log_no int,
	user_attribute_id int,
	user_val varchar(64),
	PRIMARY KEY (log_no, user_attribute_id),
	FOREIGN KEY (user_attribute_id, user_val) REFERENCES user_aval(user_attribute_id, user_val)
);

CREATE TABLE org ( 
	`org_id` int PRIMARY KEY,
	`org_name` varchar(64) NOT NULL,
	`public_key` varchar(128) NOT NULL
);