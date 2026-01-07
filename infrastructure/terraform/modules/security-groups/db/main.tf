resource "aws_security_group" "db" {
  name        = var.name
  description = "Security group for database host"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Allow DB access from application layer"
    from_port       = var.db_port
    to_port         = var.db_port
    protocol        = "tcp"
    security_groups = [var.app_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.name
  }
}
