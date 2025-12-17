#!/bin/bash
# Скрипт для створення візуалізацій метрик

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[*] Metrics Visualization Tool${NC}"
echo ""

# Перевірка чи встановлений matplotlib
python3 -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[!] Installing matplotlib...${NC}"
    pip3 install matplotlib
fi

# Режим 1: Візуалізація одного файлу
if [ "$1" == "-f" ] && [ -n "$2" ]; then
    echo -e "${GREEN}[+] Creating charts for: $2${NC}"
    python3 scripts/visualize_metrics.py -f "$2"

# Режим 2: Порівняння baseline vs attack
elif [ "$1" == "-c" ] && [ -n "$2" ] && [ -n "$3" ]; then
    echo -e "${GREEN}[+] Comparing baseline vs attack${NC}"
    echo "    Baseline: $2"
    echo "    Attack: $3"
    python3 scripts/visualize_metrics.py -b "$2" -a "$3"

# Режим 3: Автоматичне створення графіків для всіх файлів
elif [ "$1" == "-a" ]; then
    echo -e "${GREEN}[+] Creating charts for all metrics files${NC}"
    for file in results/*.json; do
        if [ -f "$file" ]; then
            echo -e "${YELLOW}Processing: $file${NC}"
            python3 scripts/visualize_metrics.py -f "$file"
        fi
    done

# Допомога
else
    echo "Usage:"
    echo "  $0 -f <metrics_file.json>              # Visualize single file"
    echo "  $0 -c <baseline.json> <attack.json>    # Compare baseline vs attack"
    echo "  $0 -a                                   # Visualize all files in results/"
    echo ""
    echo "Examples:"
    echo "  $0 -f results/attack_test1.json"
    echo "  $0 -c results/metrics_20251210_180437.json results/attack_test1.json"
    echo "  $0 -a"
    exit 1
fi

echo ""
echo -e "${GREEN}[+] Done! Charts saved to: results/charts/${NC}"
echo -e "${YELLOW}Tip: Open PNG files in results/charts/ to view graphs${NC}"
