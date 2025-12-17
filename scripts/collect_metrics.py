#!/usr/bin/env python3
"""
Metrics Collection Script
Збирає метрики: CPU, RAM, response time
"""
import psutil
import time
import requests
import json
import sys
import argparse
from datetime import datetime

def collect_system_metrics():
    """Збирає системні метрики CPU та RAM"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'ram_percent': psutil.virtual_memory().percent,
        'ram_used_mb': psutil.virtual_memory().used / (1024 * 1024),
        'ram_total_mb': psutil.virtual_memory().total / (1024 * 1024)
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
            'success': True
        }
    except requests.exceptions.RequestException as e:
        return {
            'response_time_ms': None,
            'status_code': None,
            'success': False,
            'error': str(e)
        }

def collect_metrics(url, interval=5, duration=60, output_file='metrics.json'):
    """Збирає метрики протягом певного часу"""
    print(f"[*] Starting metrics collection for {duration} seconds")
    print(f"[*] Target: {url}")
    print(f"[*] Interval: {interval} seconds")
    print(f"[*] Output: {output_file}")

    metrics_data = []
    start_time = time.time()
    end_time = start_time + duration

    try:
        while time.time() < end_time:
            timestamp = datetime.now().isoformat()

            # Системні метрики
            system_metrics = collect_system_metrics()

            # Час відгуку сервера
            response_metrics = measure_response_time(url)

            # Об'єднання метрик
            metrics = {
                'timestamp': timestamp,
                'elapsed_time': time.time() - start_time,
                **system_metrics,
                **response_metrics
            }

            metrics_data.append(metrics)

            # Виведення в консоль
            status = "OK" if response_metrics['success'] else "FAIL"
            resp_time = f"{response_metrics['response_time_ms']:.2f}ms" if response_metrics['response_time_ms'] else "N/A"
            print(f"[{timestamp}] CPU: {system_metrics['cpu_percent']:.1f}% | "
                  f"RAM: {system_metrics['ram_percent']:.1f}% | "
                  f"Response: {resp_time} | Status: {status}")

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
        successful_requests = sum(1 for m in metrics_data if m.get('success'))
        avg_cpu = sum(m['cpu_percent'] for m in metrics_data) / len(metrics_data)
        avg_ram = sum(m['ram_percent'] for m in metrics_data) / len(metrics_data)

        response_times = [m['response_time_ms'] for m in metrics_data if m.get('response_time_ms')]
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            max_response = max(response_times)
            min_response = min(response_times)

            print(f"\n=== Statistics ===")
            print(f"Successful requests: {successful_requests}/{len(metrics_data)}")
            print(f"Avg CPU: {avg_cpu:.1f}%")
            print(f"Avg RAM: {avg_ram:.1f}%")
            print(f"Avg Response Time: {avg_response:.2f}ms")
            print(f"Min Response Time: {min_response:.2f}ms")
            print(f"Max Response Time: {max_response:.2f}ms")

def main():
    parser = argparse.ArgumentParser(description='Collect system and HTTP response metrics')
    parser.add_argument('-u', '--url', type=str, required=True, help='Target URL to monitor')
    parser.add_argument('-i', '--interval', type=int, default=5, help='Collection interval in seconds (default: 5)')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Total duration in seconds (default: 60)')
    parser.add_argument('-o', '--output', type=str, default='metrics.json', help='Output file (default: metrics.json)')

    args = parser.parse_args()

    collect_metrics(
        url=args.url,
        interval=args.interval,
        duration=args.duration,
        output_file=args.output
    )

if __name__ == "__main__":
    main()
