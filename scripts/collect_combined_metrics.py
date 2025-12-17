#!/usr/bin/env python3
"""
Combined Metrics Collection Script
Збирає метрики з target server (CPU/RAM) і вимірює response time з клієнта
"""
import psutil
import time
import requests
import json
import sys
import argparse
from datetime import datetime
import subprocess

def collect_local_metrics():
    """Збирає системні метрики CPU та RAM локальної машини"""
    return {
        'local_cpu_percent': psutil.cpu_percent(interval=0.5),
        'local_ram_percent': psutil.virtual_memory().percent,
        'local_ram_used_mb': psutil.virtual_memory().used / (1024 * 1024),
        'local_ram_total_mb': psutil.virtual_memory().total / (1024 * 1024)
    }

def collect_remote_server_metrics(server_ip, ssh_key):
    """Збирає метрики CPU/RAM з віддаленого сервера через SSH"""
    try:
        # Виконуємо команду на віддаленому сервері для отримання метрик
        cmd = f"ssh -o StrictHostKeyChecking=no -i {ssh_key} ubuntu@{server_ip} \"python3 -c 'import psutil; print(psutil.cpu_percent(interval=0.5)); print(psutil.virtual_memory().percent); print(psutil.virtual_memory().used / (1024*1024)); print(psutil.virtual_memory().total / (1024*1024))'\""

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return {
                'server_cpu_percent': float(lines[0]),
                'server_ram_percent': float(lines[1]),
                'server_ram_used_mb': float(lines[2]),
                'server_ram_total_mb': float(lines[3]),
                'server_metrics_success': True
            }
        else:
            return {
                'server_cpu_percent': None,
                'server_ram_percent': None,
                'server_ram_used_mb': None,
                'server_ram_total_mb': None,
                'server_metrics_success': False,
                'server_error': result.stderr
            }
    except Exception as e:
        return {
            'server_cpu_percent': None,
            'server_ram_percent': None,
            'server_ram_used_mb': None,
            'server_ram_total_mb': None,
            'server_metrics_success': False,
            'server_error': str(e)
        }

def measure_response_time(url, timeout=5):
    """Вимірює час відгуку HTTP запиту"""
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        end = time.time()
        return {
            'response_time_ms': (end - start) * 1000,
            'status_code': response.status_code,
            'request_success': True
        }
    except requests.exceptions.RequestException as e:
        return {
            'response_time_ms': None,
            'status_code': None,
            'request_success': False,
            'request_error': str(e)
        }

def collect_combined_metrics(url, server_ip, ssh_key, interval=5, duration=60, output_file='combined_metrics.json'):
    """Збирає комбіновані метрики протягом певного часу"""
    print(f"[*] Starting combined metrics collection for {duration} seconds")
    print(f"[*] Target URL: {url}")
    print(f"[*] Target Server IP: {server_ip}")
    print(f"[*] Interval: {interval} seconds")
    print(f"[*] Output: {output_file}")
    print()

    metrics_data = []
    start_time = time.time()
    end_time = start_time + duration

    try:
        while time.time() < end_time:
            timestamp = datetime.now().isoformat()

            # Локальні метрики (клієнт)
            local_metrics = collect_local_metrics()

            # Метрики віддаленого сервера
            server_metrics = collect_remote_server_metrics(server_ip, ssh_key)

            # Час відгуку сервера
            response_metrics = measure_response_time(url)

            # Об'єднання всіх метрик
            combined = {
                'timestamp': timestamp,
                'elapsed_time': time.time() - start_time,
                **local_metrics,
                **server_metrics,
                **response_metrics
            }

            metrics_data.append(combined)

            # Виведення в консоль
            status = "OK" if response_metrics['request_success'] else "FAIL"
            resp_time = f"{response_metrics['response_time_ms']:.2f}ms" if response_metrics['response_time_ms'] else "N/A"

            server_cpu = f"{server_metrics['server_cpu_percent']:.1f}%" if server_metrics['server_cpu_percent'] is not None else "N/A"
            server_ram = f"{server_metrics['server_ram_percent']:.1f}%" if server_metrics['server_ram_percent'] is not None else "N/A"

            print(f"[{timestamp}]")
            print(f"  Server: CPU={server_cpu} RAM={server_ram} | Response={resp_time} Status={status}")
            print(f"  Client: CPU={local_metrics['local_cpu_percent']:.1f}% RAM={local_metrics['local_ram_percent']:.1f}%")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[!] Metrics collection stopped by user")

    # Зберігання результатів
    with open(output_file, 'w') as f:
        json.dump(metrics_data, f, indent=2)

    print(f"\n[+] Metrics saved to {output_file}")
    print(f"[+] Total samples collected: {len(metrics_data)}")

    # Статистика
    if metrics_data:
        successful_requests = sum(1 for m in metrics_data if m.get('request_success'))
        successful_server_metrics = sum(1 for m in metrics_data if m.get('server_metrics_success'))

        print(f"\n=== Statistics ===")
        print(f"Successful requests: {successful_requests}/{len(metrics_data)}")
        print(f"Successful server metrics: {successful_server_metrics}/{len(metrics_data)}")

        # Server CPU/RAM статистика
        server_cpus = [m['server_cpu_percent'] for m in metrics_data if m.get('server_cpu_percent') is not None]
        if server_cpus:
            print(f"\nServer Metrics:")
            print(f"  Avg CPU: {sum(server_cpus) / len(server_cpus):.1f}%")
            print(f"  Max CPU: {max(server_cpus):.1f}%")
            print(f"  Min CPU: {min(server_cpus):.1f}%")

        # Response time статистика
        response_times = [m['response_time_ms'] for m in metrics_data if m.get('response_time_ms')]
        if response_times:
            print(f"\nResponse Time:")
            print(f"  Avg: {sum(response_times) / len(response_times):.2f}ms")
            print(f"  Max: {max(response_times):.2f}ms")
            print(f"  Min: {min(response_times):.2f}ms")

        # Client metrics статистика
        local_cpus = [m['local_cpu_percent'] for m in metrics_data]
        print(f"\nClient Metrics:")
        print(f"  Avg CPU: {sum(local_cpus) / len(local_cpus):.1f}%")

def main():
    parser = argparse.ArgumentParser(description='Collect combined metrics from server and client')
    parser.add_argument('-u', '--url', type=str, required=True, help='Target URL to monitor')
    parser.add_argument('-s', '--server-ip', type=str, required=True, help='Target server IP for SSH')
    parser.add_argument('-k', '--ssh-key', type=str, required=True, help='Path to SSH private key')
    parser.add_argument('-i', '--interval', type=int, default=5, help='Collection interval in seconds (default: 5)')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Total duration in seconds (default: 60)')
    parser.add_argument('-o', '--output', type=str, default='combined_metrics.json', help='Output file (default: combined_metrics.json)')

    args = parser.parse_args()

    collect_combined_metrics(
        url=args.url,
        server_ip=args.server_ip,
        ssh_key=args.ssh_key,
        interval=args.interval,
        duration=args.duration,
        output_file=args.output
    )

if __name__ == "__main__":
    main()
