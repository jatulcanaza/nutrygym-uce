output "public_ip" {
  description = "Public IP of bastion host"
  value       = aws_instance.this.public_ip
}

output "security_group_id" {
  description = "Security group ID of bastion"
  value       = aws_security_group.bastion.id
}
