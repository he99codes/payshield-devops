output "vpc_id" {
  description = "ID of PayShield isolated VPC"
  value       = aws_vpc.payshield_vpc.id
}

output "security_group_id" {
  description = "Kubernetes cluster security group ID"
  value       = aws_security_group.k8s_cluster_sg.id
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id]
}

output "maintainer_credit" {
  description = "Project author"
  value       = "he99codes (Priyanshu)"
}
