/* =====================
   Networking
===================== */

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}

/* =====================
   Security Groups
===================== */

output "alb_security_group_id" {
  value = module.security_groups.alb_sg_id
}

output "microservices_security_group_id" {
  value = module.security_groups.microservices_sg_id
}

output "db_security_group_id" {
  value = module.db_security_group.security_group_id
}

/* =====================
   Load Balancer & ASG
===================== */

output "alb_dns_name" {
  value = module.alb_asg.alb_dns_name
}

output "alb_arn" {
  value = module.alb_asg.alb_arn
}

output "autoscaling_group_name" {
  value = module.alb_asg.asg_name
}

output "launch_template_id" {
  value = module.alb_asg.launch_template_id
}

/* =====================
   Bastion Host
===================== */

output "bastion_instance_id" {
  value = module.bastion.instance_id
}

output "bastion_public_ip" {
  value = module.bastion.public_ip
}

/* =====================
   Database Host
===================== */

output "db_instance_id" {
  value = module.ec2_data_host.instance_id
}

output "db_private_ip" {
  value = module.ec2_data_host.private_ip
}

/* =====================
   Kafka
===================== */

output "kafka_instance_id" {
  value = module.kafka_ec2.instance_id
}

output "kafka_private_ip" {
  value = module.kafka_ec2.private_ip
}

/* =====================
   Observability
===================== */
