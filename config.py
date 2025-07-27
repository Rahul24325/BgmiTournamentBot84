"""
Configuration settings for BGMI Tournament Bot
"""

import os
from datetime import timezone, timedelta

# Bot Configuration
BOT_TOKEN = "8341741465:AAG81VWIc84evKwBR1IIbwMoaHQJwgLXLsY"
ADMIN_ID = 5558853984
ADMIN_USERNAME = "@Owner_ji_bgmi"
CHANNEL_ID = -1002880573048
UPI_ID = "8435010927@ybl"

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://rahul7241146384:rahul7241146384@cluster0.qeaogc4.mongodb.net/")
DATABASE_NAME = "bgmi_tournament_bot"

# AI API Configuration
AI_API_KEY = os.getenv("AI_API_KEY", "d96a2478-7fde-4d76-a28d-b8172e561077")
AI_API_URL = "https://api.aimlapi.com/chat/completions"

# Timezone Configuration
IST = timezone(timedelta(hours=5, minutes=30))

# Tournament Types
TOURNAMENT_TYPES = {
    'solo': '🧍 SOLO',
    'duo': '👥 DUO', 
    'squad': '👨‍👩‍👧‍👦 SQUAD'
}

# Maps
BGMI_MAPS = [
    'Erangel',
    'Miramar', 
    'Sanhok',
    'Vikendi',
    'Livik',
    'Karakin'
]

# Prize Types
PRIZE_TYPES = {
    'kill_based': '💀 Kill-Based',
    'fixed_amount': '💰 Fixed Amount',
    'rank_based': '🏆 Rank-Based'
}

# Contact Information
SUPPORT_EMAILS = [
    "dumwalasquad.in@zohomail.in",
    "rahul72411463@gmail.com"
]

INSTAGRAM_HANDLE = "@ghostinside.me"
TELEGRAM_CHANNEL = "https://t.me/KyaTereSquadMeinDumHai"

# Status Messages
BOT_STATUS_MESSAGES = [
    "🔥 Lobby mein aag laga di!",
    "💀 Kill machine activated!",
    "👑 Squad ready for battle!",
    "🎮 Game time, warriors!",
    "⚡ Lightning fast responses!"
]

# Victory Animations
VICTORY_NUMBERS = {
    1: ["❶", "➊", "⓵", "🥇"],
    2: ["❷", "➋", "⓶", "🥈"], 
    3: ["❸", "➌", "⓷", "🥉"]
}

# Hashtags
HASHTAGS = {
    'solo': '#DumWalaSolo #LobbyCleaner',
    'duo': '#DumWaleDuo #KhatarnakJodi', 
    'squad': '#DumWalaSquad #SquadGoals'
}
