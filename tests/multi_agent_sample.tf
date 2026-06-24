# ==================================================
# Multi-Agent Demo Terraform
# Security + Compliance + Cost Optimization
# ==================================================

resource "aws_s3_bucket" "data" {
  bucket = "company-data-bucket"
}

resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    description = "Open SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
}

resource "aws_instance" "app" {
  ami           = "ami-12345678"
  instance_type = "m5.4xlarge"

  tags = {
    Name = "demo-app"
  }
}