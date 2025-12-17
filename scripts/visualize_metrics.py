#!/usr/bin/env python3
"""
Metrics Visualization Script
Створює графіки з JSON метрик для аналізу атак
"""
import json
import sys
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def load_metrics(file_path):
    """Завантажує метрики з JSON файлу"""
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_timestamps(metrics):
    """Конвертує ISO timestamps в datetime об'єкти"""
    timestamps = []
    for m in metrics:
        try:
            timestamps.append(datetime.fromisoformat(m['timestamp']))
        except:
            timestamps.append(None)
    return timestamps

def plot_combined_metrics(metrics_file, output_dir='results/charts'):
    """Створює комплексні графіки з метрик"""

    # Створити директорію для графіків
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Завантажити метрики
    print(f"[*] Loading metrics from {metrics_file}")
    metrics = load_metrics(metrics_file)

    if not metrics:
        print("[!] No metrics found in file")
        return

    print(f"[+] Loaded {len(metrics)} samples")

    # Парсинг даних
    timestamps = parse_timestamps(metrics)
    elapsed_times = [m.get('elapsed_time', 0) for m in metrics]

    # Server metrics
    server_cpu = [m.get('server_cpu_percent') for m in metrics]
    server_ram = [m.get('server_ram_percent') for m in metrics]

    # Client metrics
    local_cpu = [m.get('local_cpu_percent') for m in metrics]
    local_ram = [m.get('local_ram_percent') for m in metrics]

    # Response time
    response_times = [m.get('response_time_ms') for m in metrics]

    # Визначити чи є server метрики
    has_server_metrics = any(x is not None for x in server_cpu)
    has_response_time = any(x is not None for x in response_times)

    base_name = Path(metrics_file).stem

    # === Графік 1: CPU Usage (Server + Client) ===
    if has_server_metrics:
        plt.figure(figsize=(14, 6))
        plt.plot(elapsed_times, server_cpu, 'r-', linewidth=2, label='Server CPU', marker='o', markersize=4)
        plt.plot(elapsed_times, local_cpu, 'b-', linewidth=2, label='Client CPU', marker='s', markersize=4)
        plt.xlabel('Time (seconds)', fontsize=12)
        plt.ylabel('CPU Usage (%)', fontsize=12)
        plt.title('CPU Usage: Server vs Client During Attack', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        plt.tight_layout()
        output_file = f"{output_dir}/{base_name}_cpu_comparison.png"
        plt.savefig(output_file, dpi=150)
        print(f"[+] Saved: {output_file}")
        plt.close()

    # === Графік 2: RAM Usage ===
    if has_server_metrics:
        plt.figure(figsize=(14, 6))
        plt.plot(elapsed_times, server_ram, 'g-', linewidth=2, label='Server RAM', marker='o', markersize=4)
        plt.plot(elapsed_times, local_ram, 'm-', linewidth=2, label='Client RAM', marker='s', markersize=4)
        plt.xlabel('Time (seconds)', fontsize=12)
        plt.ylabel('RAM Usage (%)', fontsize=12)
        plt.title('RAM Usage: Server vs Client During Attack', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        plt.tight_layout()
        output_file = f"{output_dir}/{base_name}_ram_comparison.png"
        plt.savefig(output_file, dpi=150)
        print(f"[+] Saved: {output_file}")
        plt.close()

    # === Графік 3: Response Time ===
    if has_response_time:
        plt.figure(figsize=(14, 6))
        plt.plot(elapsed_times, response_times, 'orange', linewidth=2, marker='o', markersize=4)
        plt.xlabel('Time (seconds)', fontsize=12)
        plt.ylabel('Response Time (ms)', fontsize=12)
        plt.title('Server Response Time During Attack', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        output_file = f"{output_dir}/{base_name}_response_time.png"
        plt.savefig(output_file, dpi=150)
        print(f"[+] Saved: {output_file}")
        plt.close()

        # Логарифмічна шкала для response time (якщо великі варіації)
        if max([x for x in response_times if x]) > 100:
            plt.figure(figsize=(14, 6))
            plt.semilogy(elapsed_times, response_times, 'orange', linewidth=2, marker='o', markersize=4)
            plt.xlabel('Time (seconds)', fontsize=12)
            plt.ylabel('Response Time (ms, log scale)', fontsize=12)
            plt.title('Server Response Time During Attack (Logarithmic Scale)', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3, which='both')
            plt.tight_layout()
            output_file = f"{output_dir}/{base_name}_response_time_log.png"
            plt.savefig(output_file, dpi=150)
            print(f"[+] Saved: {output_file}")
            plt.close()

    # === Графік 4: Dashboard (всі метрики разом) ===
    if has_server_metrics and has_response_time:
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('Attack Simulation Metrics Dashboard', fontsize=16, fontweight='bold')

        # Server CPU
        axes[0, 0].plot(elapsed_times, server_cpu, 'r-', linewidth=2, marker='o', markersize=3)
        axes[0, 0].set_title('Server CPU Usage', fontweight='bold')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('CPU (%)')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim(0, 100)

        # Server RAM
        axes[0, 1].plot(elapsed_times, server_ram, 'g-', linewidth=2, marker='o', markersize=3)
        axes[0, 1].set_title('Server RAM Usage', fontweight='bold')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('RAM (%)')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim(0, 100)

        # Response Time
        axes[1, 0].plot(elapsed_times, response_times, 'orange', linewidth=2, marker='o', markersize=3)
        axes[1, 0].set_title('Response Time', fontweight='bold')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Response Time (ms)')
        axes[1, 0].grid(True, alpha=0.3)

        # Client metrics
        axes[1, 1].plot(elapsed_times, local_cpu, 'b-', linewidth=2, label='Client CPU', marker='s', markersize=3)
        axes[1, 1].plot(elapsed_times, local_ram, 'm-', linewidth=2, label='Client RAM', marker='^', markersize=3)
        axes[1, 1].set_title('Client (Attacker VM) Metrics', fontweight='bold')
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Usage (%)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_ylim(0, 100)

        plt.tight_layout()
        output_file = f"{output_dir}/{base_name}_dashboard.png"
        plt.savefig(output_file, dpi=150)
        print(f"[+] Saved: {output_file}")
        plt.close()

    # === Графік 5: Статистика (box plots) ===
    if has_server_metrics:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Attack Impact Statistics', fontsize=16, fontweight='bold')

        # CPU Box Plot
        cpu_data = [
            [x for x in server_cpu if x is not None],
            [x for x in local_cpu if x is not None]
        ]
        axes[0].boxplot(cpu_data, labels=['Server CPU', 'Client CPU'])
        axes[0].set_ylabel('CPU Usage (%)', fontsize=12)
        axes[0].set_title('CPU Usage Distribution', fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')

        # Response Time Box Plot
        if has_response_time:
            response_data = [x for x in response_times if x is not None]
            axes[1].boxplot([response_data], labels=['Response Time'])
            axes[1].set_ylabel('Response Time (ms)', fontsize=12)
            axes[1].set_title('Response Time Distribution', fontweight='bold')
            axes[1].grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        output_file = f"{output_dir}/{base_name}_statistics.png"
        plt.savefig(output_file, dpi=150)
        print(f"[+] Saved: {output_file}")
        plt.close()

    print(f"\n[+] All charts saved to: {output_dir}/")

def compare_baseline_and_attack(baseline_file, attack_file, output_dir='results/charts'):
    """Порівнює baseline і attack метрики"""

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"[*] Loading baseline: {baseline_file}")
    baseline = load_metrics(baseline_file)

    print(f"[*] Loading attack: {attack_file}")
    attack = load_metrics(attack_file)

    # Response times
    baseline_response = [m.get('response_time_ms') for m in baseline if m.get('response_time_ms')]
    attack_response = [m.get('response_time_ms') for m in attack if m.get('response_time_ms')]

    # === Графік порівняння ===
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Baseline vs Attack Comparison', fontsize=16, fontweight='bold')

    # Response Time Box Plot
    axes[0].boxplot([baseline_response, attack_response], labels=['Baseline', 'Under Attack'])
    axes[0].set_ylabel('Response Time (ms)', fontsize=12)
    axes[0].set_title('Response Time Comparison', fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')

    # Bar chart з середніми значеннями
    avg_baseline = sum(baseline_response) / len(baseline_response)
    avg_attack = sum(attack_response) / len(attack_response)

    axes[1].bar(['Baseline', 'Under Attack'], [avg_baseline, avg_attack], color=['green', 'red'], alpha=0.7)
    axes[1].set_ylabel('Average Response Time (ms)', fontsize=12)
    axes[1].set_title('Average Response Time Comparison', fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')

    # Додати текст з відсотком збільшення
    increase = ((avg_attack - avg_baseline) / avg_baseline) * 100
    axes[1].text(1, avg_attack * 0.5, f'+{increase:.0f}%', ha='center', fontsize=14, fontweight='bold', color='red')

    plt.tight_layout()
    output_file = f"{output_dir}/baseline_vs_attack_comparison.png"
    plt.savefig(output_file, dpi=150)
    print(f"[+] Saved: {output_file}")
    plt.close()

    print(f"\n=== Comparison Statistics ===")
    print(f"Baseline avg response time: {avg_baseline:.2f}ms")
    print(f"Attack avg response time: {avg_attack:.2f}ms")
    print(f"Increase: {increase:.0f}%")

def main():
    parser = argparse.ArgumentParser(description='Visualize attack simulation metrics')
    parser.add_argument('-f', '--file', type=str, help='Metrics JSON file to visualize')
    parser.add_argument('-b', '--baseline', type=str, help='Baseline metrics file for comparison')
    parser.add_argument('-a', '--attack', type=str, help='Attack metrics file for comparison')
    parser.add_argument('-o', '--output', type=str, default='results/charts', help='Output directory for charts')

    args = parser.parse_args()

    if args.file:
        plot_combined_metrics(args.file, args.output)
    elif args.baseline and args.attack:
        compare_baseline_and_attack(args.baseline, args.attack, args.output)
        # Також створити окремі графіки для кожного
        plot_combined_metrics(args.baseline, args.output)
        plot_combined_metrics(args.attack, args.output)
    else:
        print("Error: Specify either -f FILE or -b BASELINE -a ATTACK")
        sys.exit(1)

if __name__ == "__main__":
    main()
