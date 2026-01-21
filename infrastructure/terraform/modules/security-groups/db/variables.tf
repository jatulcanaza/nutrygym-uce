/*BD*/
variable "vpc_id" {
  description = "VPC donde se crea el security group"
  type        = string
}

variable "name" {
  description = "Nombre del security group"
  type        = string
}

variable "app_sg_id" {
  description = "Security Group del ASG de microservicios"
  type        = string
}


variable "allowed_ports" {
  description = "List of allowed ports from app SG"
  type        = list(number)
}
variable "bastion_sg_id" {
  description = "Security Group ID of the Bastion host"
  type        = string
}
