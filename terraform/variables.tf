variable "aws_region" {
  description = "AWS регіон для розгортання"
  type        = string
  default     = "eu-central-1"
}

variable "target_server_instance_type" {
  description = "Тип інстансу для цільового сервера"
  type        = string
  default     = "t3.small"
}

variable "attacker_vm_instance_type" {
  description = "Тип інстансу для атакуючих VM"
  type        = string
  default     = "t3.micro"
}

variable "attacker_vm_count" {
  description = "Кількість атакуючих VM (за замовчуванням 3)"
  type        = number
  default     = 3
}

variable "project_name" {
  description = "Назва проекту"
  type        = string
  default     = "attack-simulation"
}

variable "github_repo" {
  description = "GitHub репозиторій зі скриптами"
  type        = string
  default     = "https://github.com/syurii10/magistr.git"
}

variable "allowed_ssh_cidr" {
  description = "CIDR блок для SSH доступу (обмежте до вашої IP для безпеки!)"
  type        = string
  default     = "0.0.0.0/0"  # УВАГА: Змініть на вашу IP!
}
