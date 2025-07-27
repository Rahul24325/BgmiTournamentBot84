"""
Tournament-related handlers for BGMI Tournament Bot
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from config import *
from utils.helpers import get_ist_time
import logging

logger = logging.getLogger(__name__)

class TournamentHandlers:
    def __init__(self, db):
        self.db = db
    
    async def show_active_tournaments(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all active tournaments"""
        tournaments = await self.db.get_active_tournaments()
        
        if not tournaments:
            no_tournaments_msg = """❌ **No Active Tournaments**

Abhi koi tournament live nahi hai bhai!

🔔 **Stay Updated:**
• Join channel for instant notifications
• Tournament announcements daily
• Early bird discounts available

📢 Channel: @KyaTereSquadMeinDumHai"""

            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/KyaTereSquadMeinDumHai")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                no_tournaments_msg,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            return
        
        # Show tournaments
        tournaments_msg = "🎮 **ACTIVE TOURNAMENTS**\n\n"
        keyboard = []
        
        for i, tournament in enumerate(tournaments, 1):
            name = tournament['name']
            type_emoji = TOURNAMENT_TYPES.get(tournament['type'], '🎮')
            date_str = tournament['datetime'].strftime('%d/%m/%Y')
            time_str = tournament['datetime'].strftime('%H:%M')
            map_name = tournament['map']
            entry_fee = tournament['entry_fee']
            participants_count = len(tournament.get('participants', []))
            
            tournaments_msg += f"""**{i}. {name}**
{type_emoji} | 📅 {date_str} | 🕘 {time_str}
📍 {map_name} | 💰 ₹{entry_fee}
👥 Joined: {participants_count}

"""
            
            # Add join button
            tournament_id = str(tournament['_id'])
            keyboard.append([
                InlineKeyboardButton(
                    f"✅ Join {name}", 
                    callback_data=f"join_tournament_{tournament_id}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            tournaments_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def join_tournament(self, update: Update, context: ContextTypes.DEFAULT_TYPE, tournament_id):
        """Handle tournament joining"""
        user = update.effective_user
        
        # Get tournament details
        tournament = await self.db.get_tournament(tournament_id)
        if not tournament:
            await update.callback_query.answer("❌ Tournament not found!")
            return
        
        # Check if user already joined
        if user.id in tournament.get('participants', []):
            await update.callback_query.answer("✅ Already joined this tournament!")
            return
        
        # Check if tournament is still open
        if tournament['datetime'] <= get_ist_time():
            await update.callback_query.answer("❌ Tournament registration closed!")
            return
        
        # Show tournament details and join confirmation
        type_emoji = TOURNAMENT_TYPES.get(tournament['type'], '🎮')
        date_str = tournament['datetime'].strftime('%d/%m/%Y')
        time_str = tournament['datetime'].strftime('%H:%M')
        
        tournament_details = f"""🎮 **TOURNAMENT DETAILS**

🏆 **{tournament['name']}**
🎯 **Type:** {type_emoji}
📅 **Date:** {date_str}
🕘 **Time:** {time_str}
📍 **Map:** {tournament['map']}
💰 **Entry Fee:** ₹{tournament['entry_fee']}
🎁 **Prize:** {tournament.get('prize_type', 'TBA')}

👥 **Current Participants:** {len(tournament.get('participants', []))}

💳 **Payment Details:**
UPI ID: `{UPI_ID}`
Amount: ₹{tournament['entry_fee']}

**Payment Process:**
1. Pay ₹{tournament['entry_fee']} to UPI: {UPI_ID}
2. Send payment screenshot to @Owner_ji_bgmi
3. Use /paid command with UTR number
4. Wait for admin confirmation
5. Receive room details before match

⚠️ **Important Rules:**
• No refunds after room details shared
• Be online 10 minutes before match
• Follow all tournament rules
• Cheating = Permanent ban"""

        keyboard = [
            [InlineKeyboardButton("💰 Proceed to Payment", callback_data=f"pay_tournament_{tournament_id}")],
            [InlineKeyboardButton("📜 Rules & Terms", callback_data="terms_conditions")],
            [InlineKeyboardButton("🔙 Back to Tournaments", callback_data="active_tournament")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            tournament_details,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_tournament_rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE, tournament_id):
        """Show tournament specific rules"""
        tournament = await self.db.get_tournament(tournament_id)
        if not tournament:
            await update.callback_query.answer("❌ Tournament not found!")
            return
        
        rules_msg = f"""📜 **{tournament['name']} - RULES**

🎮 **GAME RULES:**
• Tournament Type: {TOURNAMENT_TYPES.get(tournament['type'], 'Unknown')}
• Map: {tournament['map']}
• Mode: {tournament['type'].upper()}
• Time Limit: Standard BGMI rules

🏆 **SCORING:**
• Kill Points: 1 point per kill
• Placement Points: Based on final rank
• Bonus: Survival time consideration

⚠️ **RESTRICTIONS:**
• No emulators allowed
• No teaming (except in team modes)
• No hacking/cheating tools
• No stream sniping

💰 **PRIZE DISTRIBUTION:**
{tournament.get('prize_details', 'Will be announced')}

🚨 **DISQUALIFICATION:**
• Using prohibited software
• Teaming in solo mode
• Toxic behavior
• Not following admin instructions

📞 **SUPPORT:**
Contact @Owner_ji_bgmi for any issues during the tournament."""

        keyboard = [
            [InlineKeyboardButton("✅ Accept & Join", callback_data=f"join_tournament_{tournament_id}")],
            [InlineKeyboardButton("🔙 Back to Tournament", callback_data=f"join_tournament_{tournament_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            rules_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def process_tournament_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE, tournament_id):
        """Process actual tournament joining"""
        user = update.effective_user
        
        # Add user to tournament participants
        success = await self.db.join_tournament(tournament_id, user.id)
        
        if success:
            # Get tournament for confirmation message
            tournament = await self.db.get_tournament(tournament_id)
            
            confirmation_msg = f"""✅ **Successfully Joined!**

🎮 **Tournament:** {tournament['name']}
👨‍💼 **Player:** @{user.username or user.first_name}
🆔 **Player ID:** {user.id}

📋 **Next Steps:**
1. 💰 Pay entry fee: ₹{tournament['entry_fee']}
2. 📸 Send screenshot to @Owner_ji_bgmi
3. 📝 Use /paid command with UTR
4. ⌛ Wait for confirmation
5. 🎮 Receive room details

⏰ **Payment Deadline:** 1 hour before tournament

🔔 **Stay Updated:**
Join @KyaTereSquadMeinDumHai for announcements"""

            keyboard = [
                [InlineKeyboardButton("💰 Pay Now", callback_data=f"pay_tournament_{tournament_id}")],
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/KyaTereSquadMeinDumHai")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                confirmation_msg,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.callback_query.answer("❌ Failed to join tournament!")
    
    async def show_tournament_leaderboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE, tournament_id):
        """Show tournament leaderboard"""
        tournament = await self.db.get_tournament(tournament_id)
        if not tournament:
            await update.callback_query.answer("❌ Tournament not found!")
            return
        
        participants = tournament.get('participants', [])
        
        if not participants:
            leaderboard_msg = f"""📊 **{tournament['name']} - LEADERBOARD**

❌ No participants yet!

Be the first to join and lead the board! 🏆"""
        else:
            leaderboard_msg = f"""📊 **{tournament['name']} - LEADERBOARD**

🏆 **Current Participants:**

"""
            
            for i, user_id in enumerate(participants, 1):
                user = await self.db.get_user(user_id)
                if user:
                    username = user.get('username', 'Unknown')
                    status = "✅ Confirmed" if user.get('confirmed', False) else "⏳ Pending"
                    leaderboard_msg += f"{i}. @{username} - {status}\n"
            
            leaderboard_msg += f"\n📈 **Total Registered:** {len(participants)}"
            leaderboard_msg += f"\n💰 **Prize Pool:** ₹{len(participants) * tournament['entry_fee']}"
        
        keyboard = [
            [InlineKeyboardButton("✅ Join Tournament", callback_data=f"join_tournament_{tournament_id}")],
            [InlineKeyboardButton("🔙 Back to Tournaments", callback_data="active_tournament")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            leaderboard_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
