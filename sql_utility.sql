select policy.policy_id, operations.operation_id, operations.operation_name, policy_user_aval.user_attribute_id, policy_user_aval.user_val, policy_resource_aval.resource_attribute_id, policy_resource_aval.resource_val from policy 
join operations on operations.operation_id = policy.operation_id
join policy_user_aval on policy_user_aval.policy_id = policy.policy_id
join policy_resource_aval on policy_resource_aval.policy_id = policy.policy_id
order by policy.policy_id, policy_user_aval.user_attribute_id, policy_resource_aval.resource_attribute_id;