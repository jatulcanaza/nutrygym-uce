resource "aws_security_group" "bastion" {
  name        = "${var.name}-sg"
  description = "Bastion security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from admin IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.name}-sg"
  }
}

resource "aws_instance" "this" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  key_name               = var.key_name
  associate_public_ip_address = true

  vpc_security_group_ids = [
    aws_security_group.bastion.id
  ]

  tags = {
    Name = var.name
  }
}
