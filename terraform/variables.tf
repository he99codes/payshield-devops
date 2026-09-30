variable "aws_region" {
  description = "AWS deployment region for PayShield FinTech infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Target deployment environment"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project domain identifier"
  type        = string
  default     = "payshield-fintech"
}

variable "maintainer" {
  description = "Project maintainer GitHub handle"
  type        = string
  default     = "he99codes"
}

variable "vpc_cidr" {
  description = "VPC CIDR block for secure isolated network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance sizing for pipeline nodes"
  type        = string
  default     = "t3.medium"
}
