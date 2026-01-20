variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Entorno (qa | prod)"
  type        = string
}

variable "vpc_id" {
  description = "ID de la VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "Lista de subnets públicas para el ALB"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Lista de subnets privadas para el ASG"
  type        = list(string)
}

variable "alb_sg_id" {
  description = "Security Group del Application Load Balancer"
  type        = string
}

variable "microservices_sg_id" {
  description = "Security Group de los microservicios"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.micro"
}

variable "desired_capacity" {
  description = "Cantidad deseada de instancias"
  type        = number
}

variable "min_size" {
  description = "Cantidad mínima de instancias"
  type        = number
}

variable "max_size" {
  description = "Cantidad máxima de instancias"
  type        = number
}

variable "ami_id" {
  description = "AMI para las instancias EC2"
  type        = string
}
variable "key_name" {
  description = "Key pair name for SSH access to ASG instances"
  type        = string
}
