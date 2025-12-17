#!/bin/bash
# Створює візуалізацію на AWS VM і завантажує результати

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    echo "Usage: $0 <metrics_file.json>"
    echo "Example: $0 results/attack_test1.json"
    exit 1
fi

METRICS_FILE=$1
FILENAME=$(basename "$METRICS_FILE")

echo -e "${YELLOW}[*] Creating visualization on AWS VM...${NC}"

# Отримати IP
cd terraform
VMCL2_IP=$(terraform output -json attacker_vms_public_ips | grep -oP '"\K[0-9.]+' | sed -n '2p')
KEY_PATH="$HOME/.ssh/id_rsa"
cd ..

echo -e "${GREEN}[+] Using VM: $VMCL2_IP${NC}"

# Копіювати файли на VM
echo -e "${YELLOW}[*] Uploading files...${NC}"
scp -o StrictHostKeyChecking=no -i "$KEY_PATH" "$METRICS_FILE" ubuntu@$VMCL2_IP:/home/ubuntu/scripts/
scp -o StrictHostKeyChecking=no -i "$KEY_PATH" scripts/visualize_metrics.py ubuntu@$VMCL2_IP:/home/ubuntu/scripts/

# Встановити matplotlib на VM і створити графіки
echo -e "${YELLOW}[*] Installing matplotlib and creating charts...${NC}"
ssh -o StrictHostKeyChecking=no -i "$KEY_PATH" ubuntu@$VMCL2_IP << 'ENDSSH'
cd /home/ubuntu/scripts
pip3 install matplotlib --user 2>/dev/null || sudo pip3 install matplotlib
python3 visualize_metrics.py -f *.json -o charts
ENDSSH

# Завантажити результати
echo -e "${YELLOW}[*] Downloading charts...${NC}"
mkdir -p results/charts
scp -o StrictHostKeyChecking=no -i "$KEY_PATH" -r ubuntu@$VMCL2_IP:/home/ubuntu/scripts/charts/* results/charts/

echo ""
echo -e "${GREEN}[+] Done! Charts saved to: results/charts/${NC}"
echo -e "${YELLOW}Tip: Open PNG files to view graphs${NC}"
ls -lh results/charts/*.png 2>/dev/null
