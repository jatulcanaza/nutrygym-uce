terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
/* VPC */
module "vpc" {
  source = "../../modules/vpc"

  project_name = var.project_name
  environment  = var.environment
}
/* Security Groups */
module "security_groups" {
  source        = "../../modules/security-groups"
  vpc_id        = module.vpc.vpc_id
  bastion_sg_id = module.bastion.bastion_sg_id
}
/*application load balancer and auto scaling group*/
module "alb_asg" {
  source = "../../modules/alb_asg"

  project_name = var.project_name
  environment  = var.environment

  vpc_id = module.vpc.vpc_id

  public_subnet_ids  = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids

  alb_sg_id           = module.security_groups.alb_sg_id
  microservices_sg_id = module.security_groups.microservices_sg_id

  db_private_ip    = module.ec2_data_host.private_ip
  kafka_private_ip = module.kafka_ec2.private_ip

  ami_id = var.ami_id

  instance_type    = var.instance_type
  desired_capacity = var.desired_capacity
  min_size         = var.min_size
  max_size         = var.max_size

  key_name = var.key_name
}

/* Database Host */
module "ec2_data_host" {
  source = "../../modules/ec2_data_host"

  name              = "nutrygym-qa-db"
  ami_id            = var.db_ami_id
  instance_type     = var.db_instance_type
  subnet_id         = module.vpc.private_subnet_ids[0]
  security_group_id = module.db_security_group.security_group_id
  key_name          = var.key_name
}
/* Database Security Group */
module "db_security_group" {
  source = "../../modules/security-groups/db"

  name          = "nutrygym-qa-db-sg"
  vpc_id        = module.vpc.vpc_id
  app_sg_id     = module.security_groups.microservices_sg_id
  bastion_sg_id = module.bastion.bastion_sg_id
  allowed_ports = [5432, 5433, 5434, 5435, 6379, 6380, 27017]
}

/* Bastion Host */
module "bastion" {
  source = "../../modules/bastion"

  name             = "nutrygym-qa-bastion"
  ami_id           = var.bastion_ami_id
  instance_type    = "t3.micro"
  subnet_id        = module.vpc.public_subnet_ids[0]
  vpc_id           = module.vpc.vpc_id
  key_name         = var.key_name
  allowed_ssh_cidr = var.admin_ip_cidr
}

module "kafka_ec2" {
  source = "../../modules/kafka_ec2"

  name              = "nutrygym-qa-kafka"
  ami_id            = var.kafka_ami_id
  instance_type     = "t3.small"
  subnet_id         = module.vpc.private_subnet_ids[0]
  security_group_id = module.security_groups.microservices_sg_id
  key_name          = var.key_name
}

module "observability" {
  source = "../../modules/observability"

  project_name = var.project_name
  environment  = var.environment
}
