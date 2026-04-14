## 🦊 Sniffox v1.8
**Advanced Network Discovery & Real-time DNS Sniffing Tool**

Sniffox is a high-performance penetration testing tool built for network reconnaissance. It helps ethical hackers and security researchers identify active devices on a network and monitor live traffic metadata through DNS sniffing.

---

## 🚀 What is Sniffox?
Sniffox uses an enhanced Nmap engine to perform multi-pass ARP scans, ensuring that even low-power or hidden devices are detected. Once a target is selected, it executes an ARP spoofing attack to intercept traffic and logs every website the target attempts to visit.

## ✨ Features
* **Extreme Scan Engine:** Performs 6 consecutive scan passes for maximum accuracy.
* **Auto-Network Detection:** Instantly detects Local IP, Default Gateway, and Network Interface.
* **Live DNS Interception:** Real-time logging of URLs visited by the target.
* **Aggressive UI:** Professional fox-themed ASCII art with high-visibility color schemes.
* **One-Click Setup:** Easy dependency management with `requirements.txt`.

---

## 🖥️ Tested On
* ✅ **Kali Linux**
* ✅ **Parrot Security OS**
* ✅ **Ubuntu**
* ✅ **Termux** (Requires Root)

---

## 📥 Installation & Usage

### 
1. Install System Requirements
```bash
sudo apt-get update && sudo apt-get install python3 nmap -y


2. Setup & Install Dependencies
Bash
git clone https://github.com/cyberlatchofficial-ctrl/Sniffox.git
cd Sniffox
sudo pip install -r requirements.txt --break-system-packages


3. Run the Tool
Bash
sudo python3 sniffox.py

---

## 📋 Change Log
* **v1.8:** Added Extreme Scan Engine (6x Scan) & UI improvements.
* **v1.7:** Improved network interface detection.

---

## ⚠️ Disclaimer
**Educational Purposes Only.**
Unauthorized use of Sniffox against networks or devices without explicit permission is illegal. The developer is not responsible for any misuse. Use responsibly to learn and secure networks.

---
**Developed with ❤️ by Cyberlatchofficial**
