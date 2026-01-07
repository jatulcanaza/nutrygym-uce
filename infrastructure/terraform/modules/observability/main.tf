resource "aws_cloudwatch_log_group" "app" {
  name              = "/${var.project_name}/${var.environment}/application"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "infra" {
  name              = "/${var.project_name}/${var.environment}/infrastructure"
  retention_in_days = 30
}
