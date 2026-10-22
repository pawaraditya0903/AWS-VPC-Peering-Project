output "vpc_a_id" {
  value = aws_vpc.vpc_a.id
}

output "vpc_b_id" {
  value = aws_vpc.vpc_b.id
}

output "peering_connection_id" {
  value = aws_vpc_peering_connection.peer.id
}

output "bastion_public_ip" {
  value = aws_instance.bastion.public_ip
}

output "bastion_instance_id" {
  value = aws_instance.bastion.id
}

output "app_a_instance_id" {
  value = aws_instance.app_a.id
}

output "app_b_instance_id" {
  value = aws_instance.app_b.id
}
