#!/bin/bash

# Update package lists
apt update && apt upgrade -y

# Install Python and pip
apt install -y python3 python3-pip

# Install required Python packages
pip3 install requests pyTelegramBotAPI

# Set up environment variables
echo "Enter your GitHub token:"
read -s GITHUB_TOKEN
echo "Enter your Telegram bot token:"
read -s TELEGRAM_BOT_TOKEN
echo "Enter your Telegram chat ID:"
read -s CHAT_ID

# Export tokens for use in the Python script
export GITHUB_TOKEN=$GITHUB_TOKEN
export TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
export CHAT_ID=$CHAT_ID

# Persist environment variables for future sessions in Codespaces
echo "export GITHUB_TOKEN=$GITHUB_TOKEN" >> ~/.bashrc
echo "export TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> ~/.bashrc
echo "export CHAT_ID=$CHAT_ID" >> ~/.bashrc

echo "Installation complete! Run 'source ~/.bashrc' to load tokens."
