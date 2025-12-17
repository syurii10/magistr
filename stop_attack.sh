#!/bin/bash
# Скрипт для зупинки атаки на всіх VM

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
echo ""

# Зупинка атаки на всіх VM
echo -e "${YELLOW}[*] Stopping attack on VMCL-1...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL1_IP \
  "pkill -f attack.py" &

echo -e "${YELLOW}[*] Stopping attack on VMCL-2...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP \
  "pkill -f attack.py" &

echo -e "${YELLOW}[*] Stopping attack on VMCL-3...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL3_IP \
  "pkill -f attack.py" &

wait

echo ""
echo -e "${GREEN}[+] Attack stopped on all VMs!${NC}"
