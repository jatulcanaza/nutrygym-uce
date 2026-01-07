variable "name" {
  description = "Name of the bastion host"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for bastion"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.micro"
}

variable "subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "key_name" {
  description = "SSH key name"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH"
  type        = string
}
