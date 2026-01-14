output "alb_sg_id" {
  description = "Security group ID for ALB"
  value       = aws_security_group.alb.id
}

output "microservices_sg_id" {
  description = "Security group ID for microservices"
  value       = aws_security_group.microservices.id
}
