resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  key_name      = var.key_name

  vpc_security_group_ids = [var.security_group_id]

  associate_public_ip_address = false

  user_data = <<EOF
#!/bin/bash
yum update -y
amazon-linux-extras enable java-openjdk11
yum install -y java-11-openjdk
echo "Kafka host ready"
EOF

  tags = {
    Name = var.name
  }
}
