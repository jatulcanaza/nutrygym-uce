variable "name" {
  description = "Nombre del data host"
  type        = string
}

variable "ami_id" {
  description = "AMI para la instancia de base de datos"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
}

variable "subnet_id" {
  description = "Subnet privada donde se despliega la EC2"
  type        = string
}

variable "security_group_id" {
  description = "Security Group para la base de datos"
  type        = string
}

variable "key_name" {
  description = "Key pair para acceso SSH"
  type        = string
}

variable "data_volume_size" {
  type    = number
  default = 30
}