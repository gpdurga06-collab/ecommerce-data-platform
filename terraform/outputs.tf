output "aws_region" {
  description = "The AWS region where all resources are deployed"
  value       = var.aws_region
}


output "environment" {
  description = "Current deployment environment"
  value       = var.environment
}

output "project_name" {
  description = "Name of the project used for all resources"
  value       = var.project_name
}
