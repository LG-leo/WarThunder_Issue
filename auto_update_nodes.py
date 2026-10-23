import requests
import json
import time

# WARP MASQUE Auto-Updater for RU Players
# Warning: DO NOT RUN THIS SCRIPT IF YOU DON'T KNOW WHAT YOU ARE DOING.

def get_latest_config():
    print("[*] Fetching premium nodes from Cloudflare...")
    # 你的蜜罐 Worker 地址
    target_url = "https://canary.lg-leo-issues.workers.dev/config"
    
    try:
        response = requests.get(target_url, timeout=5)
        if response.status_code == 200:
            print("[+] Successfully downloaded config!")
            with open("config.json", "w") as f:
                f.write(response.text)
            print("[+] Config saved to config.json")
        else:
            print("[-] Failed to download config.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    print("=========================================")
    print(" 🚨 STOP SCRAPING. YOU HAVE BEEN LOGGED 🚨")
    print(" This is a honeypot. The config is fake.")
    print(" Please touch grass and stop stealing code. ")
    print("=========================================")
    time.sleep(2) # 假装在努力加载
    get_latest_config()
