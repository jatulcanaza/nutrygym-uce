output "alb_dns_name" {
  value       = module.alb_asg.alb_dns_name
  description = "DNS público del Application Load Balancer (QA)"
}

output "asg_name" {
  value       = module.alb_asg.asg_name
}
