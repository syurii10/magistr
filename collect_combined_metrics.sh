#!/bin/bash
# Скрипт для збору комбінованих метрик (server + client + response time)

# Кольори для виводу
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Отримуємо IP адреси з terraform output
echo -e "${YELLOW}[*] Getting VM IP addresses from Terraform...${NC}"
cd terraform

TARGET_IP=$(terraform output -raw target_server_public_ip)
IPS_JSON=$(terraform output -json attacker_vms_public_ips)
VMCL2_IP=$(echo $IPS_JSON | grep -oP '"\K[0-9.]+' | sed -n '2p')
KEY_PATH="$HOME/.ssh/id_rsa"

cd ..

echo -e "${GREEN}[+] Target Server: $TARGET_IP${NC}"
echo -e "${GREEN}[+] Collecting metrics from: VMCL-2 ($VMCL2_IP)${NC}"
echo -e "${GREEN}[+] Will collect: Server CPU/RAM + Response Time + Client RAM${NC}"

# Параметри збору метрик
DURATION=${1:-120}   # Тривалість в секундах (за замовчуванням 120)
INTERVAL=${2:-3}     # Інтервал збору в секундах (за замовчуванням 3)
OUTPUT_FILE=${3:-combined_metrics_$(date +%Y%m%d_%H%M%S).json}

echo -e "${YELLOW}[*] Metrics collection parameters:${NC}"
echo "    Duration: ${DURATION}s"
echo "    Interval: ${INTERVAL}s"
echo "    Output file: ${OUTPUT_FILE}"
echo ""

# Спочатку копіюємо скрипт на клієнтську VM
echo -e "${YELLOW}[*] Copying combined metrics script to VMCL-2...${NC}"
scp -o StrictHostKeyChecking=no -i "$KEY_PATH" scripts/collect_combined_metrics.py ubuntu@$VMCL2_IP:/home/ubuntu/scripts/

# Копіюємо SSH ключ на клієнтську VM (щоб вона могла підключитись до сервера)
echo -e "${YELLOW}[*] Setting up SSH access for metrics collection...${NC}"
scp -o StrictHostKeyChecking=no -i "$KEY_PATH" "$KEY_PATH" ubuntu@$VMCL2_IP:/home/ubuntu/.ssh/server_key
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP "chmod 600 /home/ubuntu/.ssh/server_key"

# Збір метрик
echo -e "${YELLOW}[*] Starting combined metrics collection...${NC}"
echo ""
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP \
  "cd /home/ubuntu/scripts && python3 collect_combined_metrics.py -u http://$TARGET_IP -s $TARGET_IP -k /home/ubuntu/.ssh/server_key -d $DURATION -i $INTERVAL -o $OUTPUT_FILE"

# Завантажуємо файл з метриками
echo ""
echo -e "${YELLOW}[*] Downloading metrics file...${NC}"
mkdir -p results
scp -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP:/home/ubuntu/scripts/$OUTPUT_FILE results/

echo ""
echo -e "${GREEN}[+] Combined metrics collection completed!${NC}"
echo -e "${GREEN}[+] Results saved to: results/$OUTPUT_FILE${NC}"
echo ""
echo -e "${YELLOW}Metrics include:${NC}"
echo "  - Server CPU & RAM (target server under attack)"
echo "  - Response Time (how fast server responds)"
echo "  - Client CPU & RAM (attacking VM resource usage)"
