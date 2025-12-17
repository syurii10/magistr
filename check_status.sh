#!/bin/bash
# Скрипт для перевірки статусу атаки на всіх VM

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
TARGET_IP=$(terraform output -raw target_server_public_ip)
KEY_PATH="$HOME/.ssh/id_rsa"

cd ..

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}          ATTACK STATUS CHECK               ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""

# Перевірка VMCL-1
echo -e "${YELLOW}[VMCL-1]${NC} $VMCL1_IP"
ATTACK_PID=$(ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL1_IP "pgrep -f attack.py" 2>/dev/null)
if [ -n "$ATTACK_PID" ]; then
    echo -e "  Status: ${GREEN}RUNNING${NC} (PID: $ATTACK_PID)"
    ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL1_IP "tail -n 3 /home/ubuntu/scripts/attack.log 2>/dev/null" | sed 's/^/  /'
else
    echo -e "  Status: ${RED}STOPPED${NC}"
fi
echo ""

# Перевірка VMCL-2
echo -e "${YELLOW}[VMCL-2]${NC} $VMCL2_IP"
ATTACK_PID=$(ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP "pgrep -f attack.py" 2>/dev/null)
if [ -n "$ATTACK_PID" ]; then
    echo -e "  Status: ${GREEN}RUNNING${NC} (PID: $ATTACK_PID)"
    ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP "tail -n 3 /home/ubuntu/scripts/attack.log 2>/dev/null" | sed 's/^/  /'
else
    echo -e "  Status: ${RED}STOPPED${NC}"
fi
echo ""

# Перевірка VMCL-3
echo -e "${YELLOW}[VMCL-3]${NC} $VMCL3_IP"
ATTACK_PID=$(ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL3_IP "pgrep -f attack.py" 2>/dev/null)
if [ -n "$ATTACK_PID" ]; then
    echo -e "  Status: ${GREEN}RUNNING${NC} (PID: $ATTACK_PID)"
    ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL3_IP "tail -n 3 /home/ubuntu/scripts/attack.log 2>/dev/null" | sed 's/^/  /'
else
    echo -e "  Status: ${RED}STOPPED${NC}"
fi
echo ""

# Перевірка Target Server (Apache)
echo -e "${YELLOW}[TARGET SERVER]${NC} $TARGET_IP"
SERVER_STATUS=$(ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$TARGET_IP "sudo systemctl is-active apache2" 2>/dev/null)
if [ "$SERVER_STATUS" = "active" ]; then
    echo -e "  Apache Server: ${GREEN}RUNNING${NC}"
    CPU_USAGE=$(ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$TARGET_IP "top -bn1 | grep 'Cpu(s)' | awk '{print \$2}'" 2>/dev/null)
    echo -e "  CPU Usage: ${CPU_USAGE}%"
else
    echo -e "  Apache Server: ${RED}STOPPED${NC}"
fi
echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
