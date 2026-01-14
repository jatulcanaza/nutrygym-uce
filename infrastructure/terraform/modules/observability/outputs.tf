output "app_log_group_name" {
  value = aws_cloudwatch_log_group.app.name
}

output "infra_log_group_name" {
  value = aws_cloudwatch_log_group.infra.name
}
