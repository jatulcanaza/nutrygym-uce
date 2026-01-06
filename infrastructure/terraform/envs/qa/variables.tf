variable "aws_region" {
  description = "AWS region for QA environment"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "nutrygym-uce"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "qa"
}
