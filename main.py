#!/usr/bin/env python3
"""
BGMI Tournament Management Bot
Main entry point for the Telegram bot
"""

import os
import logging
import asyncio
from datetime import datetime, timezone, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import *
from database import Database
from handlers.user_handlers import UserHandlers
from handlers.admin_handlers import AdminHandlers
from handlers.tournament_handlers import TournamentHandlers
from handlers.payment_handlers import PaymentHandlers
from utils.helpers import is_admin, get_ist_time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BGMITournamentBot:
    def __init__(self):
        self.db = Database()
        self.user_handlers = UserHandlers(self.db)
        self.admin_handlers = AdminHandlers(self.db)
        self.tournament_handlers = TournamentHandlers(self.db)
        self.payment_handlers = PaymentHandlers(self.db)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with force channel join"""
        user = update.effective_user
        
        # Save user to database
        await self.db.save_user({
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'paid': False,
            'confirmed': False,
            'balance': 0,
            'referral_code': f"REF{user.id}",
            'joined_at': get_ist_time(),
            'referred_by': None
        })

        # Check if referred by someone
        if context.args:
            referral_code = context.args[0]
            if referral_code.startswith('REF'):
                await self.db.add_referral(user.id, referral_code)

        welcome_msg = f"""🚨 Oye {user.first_name}! Tere jaise player ka welcome hai is killer lobby mein! 🔥

Yaha kill count bolta hai, aur noobs chup rehte hain! 😎

👑 Game jeetne ka sirf ek rasta – Kya Tere Squad Mein Dum Hai? join karo, squad banao, aur kill machine ban jao!

💸 Paisa nahi?
👉 Toh bhai referral bhej! Dost ko bula, aur FREE ENTRY kama!
🤑 Referral se naam bhi banega aur game bhi chalega!

📧 Need help? Contact support:
🔹 dumwalasquad.in@zohomail.in
🔹 rahul72411463@gmail.com
🔹 @Owner_ji_bgmi

📢 Channel join karna mandatory hai warna result miss ho jayega:
👉 Official Channel – Kya Tere Squad Mein Dum Hai?

📸 Insta pe bhi connect ho ja bhai:
👉 @ghostinside.me

💬 Respect dega toh squad respect degi... warna bot bhi ban kar dega 🤨

#DumWalaSquad #ReferAurJeet #GhostInsideMe"""

        # Check channel membership
        try:
            member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
            if member.status in ["member", "administrator", "creator"]:
                await self.show_main_menu(update, context)
            else:
                keyboard = [
                    [InlineKeyboardButton("✅ Join Channel", url="https://t.me/KyaTereSquadMeinDumHai")],
                    [InlineKeyboardButton("✅ I've Joined", callback_data="check_membership")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(welcome_msg, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Membership check error: {e}")
            keyboard = [
                [InlineKeyboardButton("✅ Join Channel", url="https://t.me/KyaTereSquadMeinDumHai")],
                [InlineKeyboardButton("✅ I've Joined", callback_data="check_membership")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

    async def check_membership(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check if user has joined the channel"""
        query = update.callback_query
        await query.answer()
        user = query.from_user
        
        try:
            member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
            if member.status in ["member", "administrator", "creator"]:
                await self.show_main_menu(update, context)
            else:
                await query.edit_message_text(
                    text="❌ Abhi bhi channel join nahi kiya? 😠\n\nJaldi se join karo warna entry milegi hi nahi!",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Join Channel", url="https://t.me/KyaTereSquadMeinDumHai")],
                        [InlineKeyboardButton("✅ I've Joined", callback_data="check_membership")]
                    ])
                )
        except Exception as e:
            logger.error(f"Membership recheck error: {e}")
            await query.edit_message_text("⚠️ System error! Try again later.")

    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show the main 8-button menu"""
        user = update.effective_user
        referral_code = f"REF{user.id}"
        
        # Admin check
        if user.id == ADMIN_ID:
            await self.admin_handlers.show_admin_dashboard(update, context)
            return
        
        menu_msg = f"""🔥 Lobby Access Granted! 🔥

Ab kya plan hai bhai {user.first_name}?

Tera Personal Referral Code: `{referral_code}`
Dost ko bhej, aur FREE ENTRY pa!"""

        keyboard = [
            [InlineKeyboardButton("🎮 Active Tournament", callback_data="active_tournament")],
            [InlineKeyboardButton("📜 Terms & Condition", callback_data="terms_conditions")],
            [InlineKeyboardButton("👥 Invite Friends", callback_data="invite_friends")],
            [InlineKeyboardButton("📱 Share WhatsApp Status", callback_data="whatsapp_status")],
            [InlineKeyboardButton("📜 Referrals", callback_data="referrals")],
            [InlineKeyboardButton("📜 Match History", callback_data="match_history")],
            [InlineKeyboardButton("📜 Help", callback_data="help")],
            [InlineKeyboardButton("💰 Payment Status", callback_data="payment_status")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(menu_msg, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(menu_msg, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callback queries"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "check_membership":
            await self.check_membership(update, context)
        elif data == "active_tournament":
            await self.tournament_handlers.show_active_tournaments(update, context)
        elif data == "terms_conditions":
            await self.user_handlers.show_terms_conditions(update, context)
        elif data == "invite_friends":
            await self.user_handlers.show_invite_friends(update, context)
        elif data == "whatsapp_status":
            await self.user_handlers.generate_whatsapp_status(update, context)
        elif data == "referrals":
            await self.user_handlers.show_referrals(update, context)
        elif data == "match_history":
            await self.user_handlers.show_match_history(update, context)
        elif data == "help":
            await self.user_handlers.show_help(update, context)
        elif data == "payment_status":
            await self.payment_handlers.show_payment_status(update, context)
        elif data == "back_to_menu":
            await self.show_main_menu(update, context)
        elif data.startswith("join_tournament_"):
            tournament_id = data.split("_")[2]
            await self.tournament_handlers.join_tournament(update, context, tournament_id)
        elif data.startswith("pay_tournament_"):
            tournament_id = data.split("_")[2]
            await self.payment_handlers.show_payment_instructions(update, context, tournament_id)

    def setup_handlers(self, app):
        """Setup all command and callback handlers"""
        # Basic commands
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CallbackQueryHandler(self.handle_callback_query))
        
        # User commands
        app.add_handler(CommandHandler("paid", self.payment_handlers.paid_command))
        app.add_handler(CommandHandler("referrals", self.user_handlers.referrals_command))
        app.add_handler(CommandHandler("matchhistory", self.user_handlers.match_history_command))
        app.add_handler(CommandHandler("help", self.user_handlers.help_command))
        
        # Admin commands
        app.add_handler(CommandHandler("createtournament", self.admin_handlers.create_tournament_command))
        app.add_handler(CommandHandler("sendroom", self.admin_handlers.send_room_command))
        app.add_handler(CommandHandler("confirm", self.admin_handlers.confirm_payment_command))
        app.add_handler(CommandHandler("listplayers", self.admin_handlers.list_players_command))
        app.add_handler(CommandHandler("declarewinners", self.admin_handlers.declare_winners_command))
        app.add_handler(CommandHandler("clear", self.admin_handlers.clear_entries_command))
        app.add_handler(CommandHandler("today", self.admin_handlers.today_collection_command))
        app.add_handler(CommandHandler("thisweek", self.admin_handlers.week_collection_command))
        app.add_handler(CommandHandler("thismonth", self.admin_handlers.month_collection_command))
        app.add_handler(CommandHandler("solo", self.admin_handlers.solo_winner_command))
        app.add_handler(CommandHandler("duo", self.admin_handlers.duo_winner_command))
        app.add_handler(CommandHandler("squad", self.admin_handlers.squad_winner_command))
        app.add_handler(CommandHandler("special", self.admin_handlers.special_notification_command))
        
        # Message handlers
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_messages))

    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user = update.effective_user
        message = update.message.text
        
        # Check if user is in a conversation state
        user_state = context.user_data.get('state')
        
        if user_state == 'waiting_utr':
            await self.payment_handlers.process_utr_number(update, context, message)
        elif user_state == 'creating_tournament':
            await self.admin_handlers.process_tournament_creation(update, context, message)
        elif user_state == 'sending_room':
            await self.admin_handlers.process_room_details(update, context, message)
        else:
            # Default response
            await update.message.reply_text("Use /start to access the main menu!")

def main():
    """Main function to run the bot"""
    # Create bot instance
    bot = BGMITournamentBot()
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Setup handlers
    bot.setup_handlers(app)
    
    # For now, use polling for both production and development
    # Webhook can be configured later on Render
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
