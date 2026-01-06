output "alb_sg_id" {
  value = aws_security_group.alb.id
}

output "microservices_sg_id" {
  value = aws_security_group.microservices.id
}

output "db_sg_id" {
  value = aws_security_group.db.id
}
