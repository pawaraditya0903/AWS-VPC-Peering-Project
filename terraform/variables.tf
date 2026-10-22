variable "aws_region" {
  description = "AWS Region to deploy resources"
  type        = string
  default     = "ap-south-1" # Mumbai (as suggested in page 2)
}

variable "key_name" {
  description = "Name of the EC2 key pair (e.g., ewb-lab)"
  type        = string
  default     = "ewb-lab"
}

variable "admin_ip" {
  description = "Your current public IPv4 in CIDR notation (e.g. 203.0.113.10/32)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "instance_type" {
  description = "EC2 instance size"
  type        = string
  default     = "t3.micro"
}
