# BGMI Tournament Management Bot - "Kya Tere Squad Mein Dum Hai?"

A comprehensive Telegram bot for managing BGMI (Battlegrounds Mobile India) tournaments with automated payment processing, admin dashboard, AI-powered announcements, and Render deployment ready.

## 🎮 Features

### Core Features
- **Force Channel Join**: Users must join official channel before accessing bot
- **8-Button Main Menu**: Clean interface with all essential features
- **Tournament Management**: Create Solo/Duo/Squad tournaments with detailed settings
- **Payment Integration**: UPI payment verification with UTR tracking
- **Admin Dashboard**: Complete control panel with financial tracking
- **AI-Powered Messages**: Unique winner announcements using AI
- **Referral System**: Personal referral codes with bonus rewards
- **Real-time Notifications**: Automated room details and announcements

### Admin Features
- Tournament creation with step-by-step flow
- Payment confirmation system
- Player management and participant lists
- Financial tracking (daily/weekly/monthly)
- Winner declaration with AI-generated messages
- Room details distribution
- Custom notifications and announcements

### User Features
- Tournament browsing and joining
- Payment submission with UTR verification
- Referral tracking and bonus system
- Match history and statistics
- WhatsApp status sharing for promotion
- Real-time payment status updates

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB Atlas account
- Telegram Bot Token
- AI API access (optional for enhanced messages)

## 🚀 Render Deployment (Recommended)

### Step 1: Environment Variables
Set these in your Render dashboard:

```bash
MONGODB_URI=mongodb+srv://rahul7241146384:rahul7241146384@cluster0.qeaogc4.mongodb.net/
AI_API_KEY=d96a2478-7fde-4d76-a28d-b8172e561077
ENVIRONMENT=production
PORT=5000
```

### Step 2: Render Service Configuration
- **Service Type**: Web Service
- **Build Command**: `pip install python-telegram-bot motor pymongo aiohttp python-dotenv`
- **Start Command**: `python main.py`
- **Environment**: Python 3.11+
- **Plan**: Starter (recommended) or Free

### Step 3: Deploy
1. Connect your GitHub repository to Render
2. Configure environment variables in Render dashboard
3. Deploy and monitor build logs
4. Test bot with `/start` command

### Alternative: Manual Setup
