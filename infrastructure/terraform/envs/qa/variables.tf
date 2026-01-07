variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "nutrygym-uce"
}

variable "environment" {
  type    = string
  default = "qa"
}

variable "ami_id" {
  description = "AMI Amazon Linux 2023"
  type        = string
  default     = "ami-0c02fb55956c7d316"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "desired_capacity" {
  type    = number
  default = 2
}

variable "min_size" {
  type    = number
  default = 1
}

variable "max_size" {
  type    = number
  default = 3
}

variable "db_ami_id" {
  type = string
}

variable "db_instance_type" {
  type = string
}

variable "key_name" {
  type = string
}

variable "bastion_ami_id" {
  description = "AMI for bastion host"
  type        = string
}

variable "admin_ip_cidr" {
  description = "Admin public IP in CIDR format"
  type        = string
}
variable "kafka_ami_id" {
  description = "AMI ID for Kafka EC2 instance"
  type        = string
}
