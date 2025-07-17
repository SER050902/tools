import ipaddress
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

def get_local_network_cidr():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    net = ipaddress.IPv4Network(local_ip + '/24', strict=False)
    print(f"📡 检测到本机 IP：{local_ip}，推测网段：{net}")
    return str(net)

def ping_ip(ip):
    system = platform.system()
    if system == "Windows":
        command = ["ping", "-n", "1", "-w", "500", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL)
        return str(ip) if result.returncode == 0 else None
    except Exception:
        return None

def scan_network(network_cidr, max_threads=100):
    print(f"\n🔍 正在扫描网络：{network_cidr}")
    net = ipaddress.ip_network(network_cidr, strict=False)
    alive_ips = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(ping_ip, ip): ip for ip in net.hosts()}

        for future in as_completed(futures):
            ip = future.result()
            if ip:
                print(f"✅ 在线：{ip}")
                alive_ips.append(ip)

    print("\n📋 扫描完成，在线设备如下：")
    for ip in alive_ips:
        print(ip)
    print(f"\n共发现在线 IP：{len(alive_ips)} 台")

if __name__ == "__main__":
    cidr = get_local_network_cidr()
    scan_network(cidr)
