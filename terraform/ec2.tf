# AMI для Ubuntu
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Цільовий сервер (який атакуємо)
resource "aws_instance" "target_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.target_server_instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.servers.id]
  key_name               = aws_key_pair.main.key_name

  user_data = <<-EOF
#!/bin/bash
set -e

              # Оновлення системи
              apt-get update
              apt-get install -y python3-pip git python3-psutil python3-requests

              # Клонування репозиторію зі скриптами
              cd /home/ubuntu
              if [ ! -d "scripts" ]; then
                git clone ${var.github_repo} scripts || echo "Git clone failed, will use local scripts"
              fi

              if [ -d "scripts" ]; then
                cd scripts
                git pull origin master || true
                chown -R ubuntu:ubuntu /home/ubuntu/scripts
              fi

              # Запуск CPU-intensive сервера як systemd service
              cat > /etc/systemd/system/target-server.service <<'SERVICE'
[Unit]
Description=Target HTTP Server for Load Testing
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/ubuntu/scripts
ExecStart=/usr/bin/python3 /home/ubuntu/scripts/target_server.py 80
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE

              # Запуск сервісу
              systemctl daemon-reload
              systemctl enable target-server
              systemctl start target-server

              # Встановлення залежностей для збору метрик
              pip3 install psutil

              echo "Target server setup completed" > /home/ubuntu/setup_complete.txt
              EOF

  tags = {
    Name = "vmser"
    Role = "target"
    Type = var.target_server_instance_type
  }

  monitoring = true
}

# Атакуючі VM (3 віртуальні машини)
resource "aws_instance" "attacker_vms" {
  count = var.attacker_vm_count

  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.attacker_vm_instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.servers.id]
  key_name               = aws_key_pair.main.key_name

  user_data = <<-EOF
#!/bin/bash
set -e

              # Оновлення системи
              apt-get update
              apt-get install -y python3-pip git python3-psutil python3-requests

              # Клонування репозиторію зі скриптами
              cd /home/ubuntu
              if [ ! -d "scripts" ]; then
                git clone ${var.github_repo} scripts || echo "Git clone failed, will use local scripts"
              fi

              if [ -d "scripts" ]; then
                cd scripts
                git pull origin master || true
                chown -R ubuntu:ubuntu /home/ubuntu/scripts
              fi

              # Встановлення залежностей
              pip3 install requests psutil

              # Зберігаємо IP цільового сервера для зручності
              echo "${aws_instance.target_server.private_ip}" > /home/ubuntu/target_ip.txt

              chown -R ubuntu:ubuntu /home/ubuntu

              echo "Attacker VM ${count.index + 1} setup completed" > /home/ubuntu/setup_complete.txt
              EOF

  tags = {
    Name = "vmcl-${count.index + 1}"
    Role = "attacker"
    VMID = count.index + 1
  }

  depends_on = [aws_instance.target_server]
}
