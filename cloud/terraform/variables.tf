variable "aws_region" {
  description = "The AWS region to deploy in"
  type        = string
  default     = "eu-west-1"
}

variable "ami_id" {
  description = "The AMI ID to use for the instance"
  type        = string
  default     = "ami-0a636034c582e2138"
}

variable "instance_type" {
  description = "The instance type to use"
  type        = string
  default     = "c6g.2xlarge"
}
