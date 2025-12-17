output "target_server_public_ip" {
  description = "Публічний IP цільового сервера"
  value       = aws_instance.target_server.public_ip
}

output "target_server_private_ip" {
  description = "Приватний IP цільового сервера (для внутрішніх запитів)"
  value       = aws_instance.target_server.private_ip
}

output "attacker_vms_public_ips" {
  description = "Публічні IP всіх атакуючих VM"
  value       = aws_instance.attacker_vms[*].public_ip
}

output "attacker_vms_private_ips" {
  description = "Приватні IP всіх атакуючих VM"
  value       = aws_instance.attacker_vms[*].private_ip
}

output "vpc_id" {
  description = "ID VPC"
  value       = aws_vpc.main.id
}

output "target_server_url" {
  description = "URL цільового сервера для тестування"
  value       = "http://${aws_instance.target_server.public_ip}"
}

output "ssh_commands" {
  description = "Команди для SSH підключення"
  value = {
    target_server = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_instance.target_server.public_ip}"
    attacker_vms = [
      for idx, ip in aws_instance.attacker_vms[*].public_ip :
      "ssh -i ~/.ssh/id_rsa ubuntu@${ip}  # Attacker VM ${idx + 1}"
    ]
  }
}

output "infrastructure_summary" {
  description = "Загальна інформація про інфраструктуру"
  value = {
    region             = var.aws_region
    target_server_type = var.target_server_instance_type
    attacker_vm_type   = var.attacker_vm_instance_type
    attacker_vm_count  = var.attacker_vm_count
    total_instances    = 1 + var.attacker_vm_count
  }
}
