variable "aws_region" {
  type        = string
  default     = "us-east-2"
  description = "AWS region where all resources will be created"
}



variable "project_name" {
  type        = string
  default     = "ecommerce-data-platform"
  description = "Name of the project used to name all resources"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Deployment environment - dev or prod"
}

variable "aws_account_id" {
  type        = string
  description = "Your AWS account ID"
}


