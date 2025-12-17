#!/bin/bash
# Скрипт для запуску атаки на всіх 3 VM одночасно

# Кольори для виводу
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Отримуємо IP адреси з terraform output
echo -e "${YELLOW}[*] Getting VM IP addresses from Terraform...${NC}"
cd terraform

# Отримуємо IP через terraform output json (без jq)
IPS_JSON=$(terraform output -json attacker_vms_public_ips)
VMCL1_IP=$(echo $IPS_JSON | grep -oP '"\K[0-9.]+' | sed -n '1p')
VMCL2_IP=$(echo $IPS_JSON | grep -oP '"\K[0-9.]+' | sed -n '2p')
VMCL3_IP=$(echo $IPS_JSON | grep -oP '"\K[0-9.]+' | sed -n '3p')
KEY_PATH="$HOME/.ssh/id_rsa"

cd ..

echo -e "${GREEN}[+] Found VMs:${NC}"
echo "    VMCL-1: $VMCL1_IP"
echo "    VMCL-2: $VMCL2_IP"
echo "    VMCL-3: $VMCL3_IP"

# Параметри атаки (можна змінювати)
DURATION=${1:-120}  # Тривалість в секундах (за замовчуванням 120)
THREADS=${2:-200}   # Кількість потоків (за замовчуванням 200)
PACKETS=${3:-500}   # Пакетів на задачу (за замовчуванням 500)

echo -e "${YELLOW}[*] Attack parameters:${NC}"
echo "    Duration: ${DURATION}s"
echo "    Threads: ${THREADS}"
echo "    Packets per task: ${PACKETS}"
echo ""

# Запуск атаки на всіх VM
echo -e "${YELLOW}[*] Starting attack on VMCL-1...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL1_IP \
  "cd /home/ubuntu/scripts && nohup python3 attack.py -d $DURATION --threads $THREADS --packets $PACKETS > attack.log 2>&1 &" &

sleep 1

echo -e "${YELLOW}[*] Starting attack on VMCL-2...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP \
  "cd /home/ubuntu/scripts && nohup python3 attack.py -d $DURATION --threads $THREADS --packets $PACKETS > attack.log 2>&1 &" &

sleep 1

echo -e "${YELLOW}[*] Starting attack on VMCL-3...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL3_IP \
  "cd /home/ubuntu/scripts && nohup python3 attack.py -d $DURATION --threads $THREADS --packets $PACKETS > attack.log 2>&1 &" &

wait

echo ""
echo -e "${GREEN}[+] Attack started on all 3 VMs!${NC}"
echo -e "${GREEN}[+] Attack will run for ${DURATION} seconds${NC}"
echo ""
echo -e "${YELLOW}Tip: Use ./collect_metrics.sh to start collecting metrics${NC}"
echo -e "${YELLOW}Tip: Use ./stop_attack.sh to stop the attack early${NC}"
