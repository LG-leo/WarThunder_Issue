Caused by https://forum.warthunder.com/t/network-severe-packet-loss-high-ping-specifically-for-cloudflare-warp-as13335-udp-traffic/359265/3 ( [Network] Severe Packet Loss & High Ping Specifically for Cloudflare WARP (AS13335) UDP Traffic), i find a way to have a better connect to War Thunder 

--
1. cloudflareWarp will demo your real input IP, so you cannot and no any able to hide your IP when you using cloudflare(AS13335) flow.
2. you are no any able to try to use VPS to get lower prices.
---

The official WARP client is too fragile (Fail-Closed) when facing local ISP QoS and Fake_MITM injections. By extracting the MASQUE configuration locally and running it through Clash Verge Rev (Mihomo core), we can achieve 100% anti-interference, effectively ignoring Fake_MITM and RST packets, reducing Ping from 600-999ms to 330~480ms and PL from 20-55% to 1-10%.

For the past few weeks, playing War Thunder via Cloudflare WARP has been a nightmare. The official WARP client shows severe instability, with in-game Ping fluctuating wildly between 600ms and 999ms, and Packet Loss (PL) spiking to 20% - 55% in this month.

**TL;DR:** The official WARP client is too fragile (Fail-Closed) when facing local ISP QoS and Fake_MITM injections. By extracting the MASQUE configuration locally and running it through Clash Verge Rev (Mihomo core), we achieve 100% anti-interference. It ignores Fake_MITM and RST packets, reducing in-game Ping from 600-999ms to 330~480ms and Packet Loss (PL) from 20-55% to 1-10%.

---

### ⚠️ Important Disclaimer
This guide is a follow-up to my previous diagnostic post: *[Network] Severe Packet Loss & High Ping Specifically for Cloudflare WARP (AS13335) UDP Traffic*. 

Before we begin, please note:
1. **WARP is not an anonymity tool.** It does not hide your real IP in the way Tor does. Your real traffic may still be exposed in certain scenarios.
2. **Do NOT use this to bypass regional pricing.** Gaijin's Terms of Use strictly prohibit using VPNs/proxies to disguise your location for cheaper purchases. This guide is **ONLY** for improving connection quality and reducing latency.

---

### 🔍 The Problem
For the past few weeks, playing War Thunder via Cloudflare WARP has been a nightmare. The official client shows severe instability, with in-game Ping fluctuating wildly between 600ms and 999ms, and Packet Loss spiking to 20% - 55%. 

*Note: My testing showed the WARP tunnel itself is healthy (0.4% PL to 8.8.8.8). The issue is the "Last Mile" QoS throttling applied by Gaijin's upstream provider specifically to the Cloudflare AS13335 UDP network.*

---
### for Clash_Verge_rev

In fact, I found that in point-to-point connections and system proxies, the `timeout/error` error display problems are most likely to occur. TUN can demo the real `timeoout/error/connect`

As for the traffic graph, there have always been issues with it.(include all mode)

---
### 🛠️ Step-by-Step Guide

**Prerequisites:** 
Make sure you have installed **Git**, **Python 3**, and downloaded **Clash Verge Rev** from GitHub.

#### Step 1: Clone the repository
Open your Terminal (macOS/Linux) or PowerShell (Windows) and run:
```bash
git clone https://github.com/byJoey/warp-masque-actions.git
cd warp-masque-actions
```

#### Step 2: Create and activate a Python virtual environment
Choose the command block based on your OS:

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**Windows (CMD):**
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(Note: You will see `(venv)` in your terminal prompt. If you get an execution policy error in PowerShell, run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` as Administrator first.)*

#### Step 3: Download `usque` core
**macOS (Apple Silicon):**
```bash
VER=$(curl -sL https://api.github.com/repos/Diniboy1123/usque/releases/latest | grep '"tag_name":' | cut -d '"' -f 4 | sed 's/v//')
curl -sL -o usque.zip "https://github.com/Diniboy1123/usque/releases/download/v${VER}/usque_${VER}_darwin_arm64.zip"
unzip -oq usque.zip && chmod +x usque
```
*(For Intel Macs, replace `darwin_arm64` with `darwin_amd64`)*

**Windows (PowerShell):**
```powershell
$VER = (Invoke-RestMethod -Uri "https://api.github.com/repos/Diniboy1123/usque/releases/latest").tag_name -replace 'v', ''
Invoke-WebRequest -Uri "https://github.com/Diniboy1123/usque/releases/download/v${VER}/usque_${VER}_windows_amd64.zip" -OutFile "usque.zip"
Expand-Archive -Path "usque.zip" -DestinationPath "." -Force
```
*(For ARM Windows, replace `windows_amd64` with `windows_arm64`)*

**Linux (PC/Servers):**
```bash
VER=$(curl -sL https://api.github.com/repos/Diniboy1123/usque/releases/latest | grep '"tag_name":' | cut -d '"' -f 4 | sed 's/v//')
curl -sL -o usque.zip "https://github.com/Diniboy1123/usque/releases/download/v${VER}/usque_${VER}_linux_amd64.zip"
unzip -oq usque.zip && chmod +x usque
```

#### Step 4: Register WARP device (Generate Keys)
**macOS / Linux:**
```bash
./usque register -a -n "My-Local"
```
**Windows:**
```cmd
usque.exe register -a -n "My-Local"
```
*(Note: If successful, a `config.json` will be generated. If you get a `429` error, your IP is rate-limited by Cloudflare. Restart your router to get a new IP and try again.)*

#### Step 5: Generate the MASQUE Config
Create the output folder:
*   **macOS / Linux:** `mkdir -p dist`
*   **Windows:** `New-Item -ItemType Directory -Force -Path dist`

Run the generation script:
*   **macOS / Linux:** `python3 scripts/gen_masque.py config.json dist`
*   **Windows:** `python scripts/gen_masque.py config.json dist`
*(If it throws missing module errors, just run `pip install requests pyyaml`)*

#### Step 6: Import to Clash Verge Rev
1. Find the generated file: `dist/warp-masque.yaml` (contains 57 nodes).
2. Open **Clash Verge Rev**.
3. **[Important]** Go to Settings -> Clash Core, switch to **Alpha** (or Stable if your version supports MASQUE).
4. Go to "Profiles", drag and drop the `warp-masque.yaml` file into it.
5. Go to "Proxies", enable **TUN mode**, and test the latency.
6. **[Recommended]** Create a `url-test` (auto speed test) proxy group and put all 57 nodes inside. It will automatically switch to the fastest alive node if one gets QoS-throttled.

---

### 💡 Notes & Why this works
1. **Fail-Open Resilience:** The Mihomo core doesn't panic. When your ISP injects `Fake_MITM` or `RST` packets, Clash simply drops them and waits for the real response. It ignores the interference 100%.
2. **No DNS Pre-check:** The local YAML config hardcodes the IPs, completely bypassing DNS pollution.
3. **Refreshing IPs:** If most nodes get blocked over time, simply repeat **Step 4** and **Step 5** to register a new WARP device and generate a fresh batch of IPs.
4. **Terminal Warnings:** If you see `setlocale` warnings, you can ignore them or run `export LANG=en_US.UTF-8`.
