"""
User-related handlers for BGMI Tournament Bot
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import *
from utils.helpers import get_ist_time
import logging

logger = logging.getLogger(__name__)

class UserHandlers:
    def __init__(self, db):
        self.db = db
    
    async def show_terms_conditions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show terms and conditions"""
        terms_msg = """📜 **TERMS & CONDITIONS**

**🎮 GAME RULES:**
1. ❌ No emulators allowed
2. ❌ No teaming/hacking/cheating
3. 🎯 Kill + Rank = Points calculation
4. ⏰ Be punctual - Late entries not allowed
5. 📱 Only mobile devices permitted
6. 🎤 Voice chat allowed within squad

**💰 PAYMENT RULES:**
1. 💸 Entry fee must be paid before room details
2. 🧾 Screenshot proof required for payment
3. 🔢 UTR number mandatory for verification
4. ❌ No refunds after room details shared
5. ✅ Payment confirmation by admin required

**⚠️ DISCLAIMER:**
1. 🚫 No refunds for technical issues
2. 📶 Not responsible for network/lag issues
3. 🔌 Not responsible for device disconnection
4. 🚨 Cheaters will be permanently banned
5. ⚖️ Admin decisions are final
6. 🎮 By joining, you accept all risks

**📧 SUPPORT:**
dumwalasquad.in@zohomail.in
@Owner_ji_bgmi"""

        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            terms_msg, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
    
    async def show_invite_friends(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show invite friends options"""
        user = update.effective_user
        referral_code = f"REF{user.id}"
        bot_username = context.bot.username
        
        invite_msg = f"""👥 **INVITE FRIENDS & EARN FREE ENTRY!**

🎯 **Tera Referral Code:** `{referral_code}`

📲 **Share this link:**
https://t.me/{bot_username}?start={referral_code}

🎁 **BENEFITS:**
• Every friend joins = ₹25 bonus
• 2 friends = FREE tournament entry
• 5 friends = VIP tournament access
• 10 friends = Special cash reward

📈 **Your Stats:**
• Total Referrals: {await self.get_referral_count(user.id)}
• Earned Bonus: ₹{await self.get_referral_bonus(user.id)}

💬 **Copy & send this message:**

🔥 Bhai, BGMI tournament join kar!
Daily cash prizes aur kill rewards!
Mera referral code use kar: {referral_code}
Bot link: https://t.me/{bot_username}?start={referral_code}
#FreeEntry #BGMITournament"""

        keyboard = [
            [InlineKeyboardButton("📋 Copy Referral Link", 
                                url=f"https://t.me/{bot_username}?start={referral_code}")],
            [InlineKeyboardButton("📊 Check Referrals", callback_data="referrals")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            invite_msg, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
    
    async def generate_whatsapp_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate WhatsApp status message"""
        user = update.effective_user
        referral_code = f"REF{user.id}"
        bot_username = context.bot.username
        
        status_msg = f"""📱 **WHATSAPP STATUS READY!**

Copy & post this as your WhatsApp status:

---

🎮 BGMI TOURNAMENTS LIVE!
🔥 Daily Cash 💰 | 💀 Kill Rewards | 👑 VIP Matches
💥 FREE ENTRY with my code 👉 {referral_code}
📲 Click & Join:
https://t.me/{bot_username}?start={referral_code}
⚡ Limited Slots! Fast join karo!

#BGMI #EarnWithKills #DumWalaSquad

---

Post karne ke baad screenshot bhej @Owner_ji_bgmi ko!
Extra bonus milega! 🎁"""

        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            status_msg, 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
    
    async def show_referrals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's referrals"""
        user = update.effective_user
        referrals = await self.db.get_referrals(user.id)
        
        total_referrals = len(referrals)
        total_bonus = total_referrals * 25  # ₹25 per referral
        
        referral_msg = f"""📊 **YOUR REFERRAL STATS**

👥 **Total Referrals:** {total_referrals}
💰 **Total Bonus Earned:** ₹{total_bonus}
🎁 **Free Entries Available:** {total_bonus // 50}

📈 **Recent Referrals:**"""

        if referrals:
            for i, ref in enumerate(referrals[-5:], 1):  # Show last 5
                try:
                    referred_user = await self.db.get_user(ref['referred_id'])
                    username = referred_user.get('username', 'Unknown') if referred_user else 'Unknown'
                    date = ref['created_at'].strftime('%d/%m/%Y')
                    referral_msg += f"\n{i}. @{username} - {date}"
                except:
                    referral_msg += f"\n{i}. User - {ref['created_at'].strftime('%d/%m/%Y')}"
        else:
            referral_msg += "\n❌ No referrals yet!"

        referral_msg += f"""

🎯 **EARN MORE:**
• Share your referral code: `REF{user.id}`
• Get ₹25 per successful referral
• 2 referrals = 1 FREE tournament entry!"""

        keyboard = [
            [InlineKeyboardButton("👥 Invite Friends", callback_data="invite_friends")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                referral_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                referral_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
    
    async def show_match_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's match history"""
        user = update.effective_user
        tournaments = await self.db.get_user_tournaments(user.id)
        
        history_msg = f"""📜 **YOUR MATCH HISTORY**

👨‍💼 Player: @{user.username or user.first_name}
🎮 Total Matches: {len(tournaments)}

📈 **Recent Tournaments:**"""

        if tournaments:
            for i, tournament in enumerate(tournaments[:10], 1):  # Show last 10
                name = tournament.get('name', 'Unknown Tournament')
                date = tournament.get('datetime', get_ist_time()).strftime('%d/%m/%Y')
                status = tournament.get('status', 'unknown')
                
                status_emoji = {
                    'upcoming': '⏳',
                    'live': '🔴',
                    'completed': '✅',
                    'cancelled': '❌'
                }.get(status, '❓')
                
                history_msg += f"\n{i}. {status_emoji} {name} - {date}"
        else:
            history_msg += "\n❌ No matches played yet!"

        history_msg += """

🎯 **PERFORMANCE STATS:**
• Win Rate: Calculating...
• Avg Kills: Calculating...
• Total Earnings: Calculating...

🎮 Join more tournaments to build your stats!"""

        keyboard = [
            [InlineKeyboardButton("🎮 Active Tournaments", callback_data="active_tournament")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                history_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                history_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        help_msg = """📜 **HELP & SUPPORT**

🎮 **BOT COMMANDS:**
• /start - Main menu access
• /paid - Submit payment proof
• /referrals - Check your referrals
• /matchhistory - View match history
• /help - Show this help menu

💰 **PAYMENT PROCESS:**
1. Join tournament
2. Pay entry fee to UPI: 8435010927@ybl
3. Send screenshot to @Owner_ji_bgmi
4. Use /paid command with UTR number
5. Wait for admin confirmation

🎯 **TOURNAMENT JOINING:**
1. Check active tournaments
2. Click "Join Now"
3. Complete payment
4. Wait for room details
5. Join room and play!

📧 **CONTACT SUPPORT:**
• Email: dumwalasquad.in@zohomail.in
• Email: rahul72411463@gmail.com
• Telegram: @Owner_ji_bgmi
• Instagram: @ghostinside.me

🔗 **USEFUL LINKS:**
• Official Channel: @KyaTereSquadMeinDumHai
• Bot Updates: Check channel regularly

⚠️ **REMEMBER:**
• Be respectful in chat
• Follow all tournament rules
• No cheating/hacking
• Admin decisions are final"""

        keyboard = [
            [InlineKeyboardButton("📧 Contact Admin", url="https://t.me/Owner_ji_bgmi")],
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/KyaTereSquadMeinDumHai")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                help_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                help_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
    
    async def get_referral_count(self, user_id):
        """Get total referral count for user"""
        try:
            referrals = await self.db.get_referrals(user_id)
            return len(referrals)
        except:
            return 0
    
    async def get_referral_bonus(self, user_id):
        """Calculate total referral bonus"""
        try:
            count = await self.get_referral_count(user_id)
            return count * 25  # ₹25 per referral
        except:
            return 0
    
    # Command handlers
    async def referrals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /referrals command"""
        await self.show_referrals(update, context)
    
    async def match_history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /matchhistory command"""
        await self.show_match_history(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await self.show_help(update, context)
