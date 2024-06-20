provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "deployer" {
  key_name   = "${uuid()}"
  public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEwiM3yyAlCZN2RwYqbYcimGwwCH/H1FvTq+TrmKy1S+ emmanuel.orozco@adeo.com"
}

resource "aws_security_group" "flask_server_upspeak_sg" {
  name        = "flask_server_upspeak_sg"
  description = "Allow SSH and HTTP traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8001
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "flask_server" {
  ami           = var.ami_id
  instance_type = var.instance_type

  key_name      = aws_key_pair.deployer.key_name

  root_block_device {
    volume_size = 8  # Size in GB
    volume_type = "gp2"
  }

  tags = {
    Name = "FlaskServerInstance"
  }

  # Security group to allow SSH and HTTP access
  vpc_security_group_ids = [aws_security_group.flask_server_upspeak_sg.id]
}

# Define the Elastic IP resource
resource "aws_eip" "flask_server_eip" {
  vpc = true
}

# Associate the Elastic IP with the instance
resource "aws_eip_association" "flask_server_eip_assoc" {
  instance_id   = aws_instance.flask_server.id
  allocation_id = aws_eip.flask_server_eip.id
}

output "instance_id" {
  value = aws_instance.flask_server.id
}

output "elastic_ip" {
  value = aws_eip.flask_server_eip.public_ip
}
