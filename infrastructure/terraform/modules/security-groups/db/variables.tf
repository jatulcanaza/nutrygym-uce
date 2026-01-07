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

variable "db_port" {
  description = "Puerto de la base de datos"
  type        = number
}
