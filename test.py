#!/usr/bin/env python3
import requests
import socket
import random
import time
import threading
import os

# === CONFIGURATION ===
TARGET_IP = "10.0.0.250"      # Honeypot IP address
TARGET_PORTS = [22, 80, 443]  # Common open ports
THREADS = 10                  # Number of concurrent threads
DURATION = 120                # Duration of traffic (seconds)

def send_tcp_packets():
    """Simulate TCP connection attempts."""
    for _ in range(100):
        port = random.choice(TARGET_PORTS)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((TARGET_IP, port))
            s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            s.close()
        except:
            pass

def send_http_requests():
    """Trigger Suricata web signatures with HTTP requests."""
    urls = [
        f"http://{TARGET_IP}/login",
        f"http://{TARGET_IP}/admin",
        f"http://{TARGET_IP}/phpmyadmin",
        f"http://{TARGET_IP}/wp-login.php",
    ]
    for _ in range(50):
        try:
            requests.get(random.choice(urls), timeout=1)
        except:
            pass

import platform
import subprocess

def send_icmp_pings():
    """Send ping requests (cross-platform)."""
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    for _ in range(10):
        try:
            subprocess.run(["ping", count_flag, "1", TARGET_IP],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        except:
            pass

def run_traffic():
    """Run a mix of TCP, HTTP, and ICMP traffic in parallel."""
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=random.choice([
            send_tcp_packets, send_http_requests, send_icmp_pings
        ]))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    print(f"[+] Sending traffic to {TARGET_IP} for {DURATION} seconds...")
    end_time = time.time() + DURATION
    while time.time() < end_time:
        run_traffic()
    print("[+] Done! Traffic generation complete.")
