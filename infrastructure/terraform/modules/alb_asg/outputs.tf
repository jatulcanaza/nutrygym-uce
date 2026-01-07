output "alb_dns_name" {
  description = "DNS público del ALB"
  value       = aws_lb.this.dns_name
}

output "asg_name" {
  description = "Nombre del Auto Scaling Group"
  value       = aws_autoscaling_group.this.name
}

output "target_group_arn" {
  description = "ARN del Target Group"
  value       = aws_lb_target_group.this.arn
}

output "app_sg_id" {
  description = "Security Group ID used by application instances"
  value       = var.microservices_sg_id
}
