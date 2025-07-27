"""
Admin-related handlers for BGMI Tournament Bot
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from config import *
from utils.helpers import is_admin, get_ist_time
from utils.ai_messages import AIMessageGenerator
import logging

logger = logging.getLogger(__name__)

class AdminHandlers:
    def __init__(self, db):
        self.db = db
        self.ai_generator = AIMessageGenerator()
    
    async def show_admin_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin dashboard"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        current_time = get_ist_time().strftime('%d/%m/%Y %H:%M IST')
        active_tournaments = await self.db.get_active_tournaments()
        live_tournament_count = len(active_tournaments)
        
        # Calculate next match time
        next_match_in = "No upcoming matches"
        if active_tournaments:
            next_tournament = active_tournaments[0]
            next_match_time = next_tournament.get('datetime')
            if next_match_time:
                time_diff = next_match_time - get_ist_time()
                if time_diff.total_seconds() > 0:
                    minutes = int(time_diff.total_seconds() / 60)
                    next_match_in = f"{minutes} minutes"
        
        dashboard_msg = f"""👑 **Welcome, Boss!**
"Tere aane se system bhi alert ho gaya hai!"

🕐 **Login Time:** `{current_time}`
📢 **Live Tournaments:** `{live_tournament_count}`
📈 **Next Match In:** `{next_match_in}`

🛠 **ADMIN PANEL:**
/createtournament - 🎯 New tournament
/sendroom - 📤 Send room details
/confirm - ✅ Approve players
/listplayers - 📋 Participant list
/declarewinners - 🏆 Announce winners
/clear - 🧹 Edit/remove entries
/today - 📅 Today's collection
/thisweek - 📈 Weekly collection
/thismonth - 📊 Monthly collection
/squad - 👑 Squad victory
/duo - 🔥 Duo victory
/solo - 🧍 Solo victory
/special - 💥 Custom notifications

Sab kuch tere haath mein hai Bhai... aur haath garam hai! 🔥"""

        keyboard = [
            [InlineKeyboardButton("🎯 Create Tournament", callback_data="admin_create_tournament")],
            [InlineKeyboardButton("📋 List Players", callback_data="admin_list_players")],
            [InlineKeyboardButton("💰 Today's Collection", callback_data="admin_today_collection")],
            [InlineKeyboardButton("📊 Financial Reports", callback_data="admin_financial_reports")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                dashboard_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                dashboard_msg, 
                reply_markup=reply_markup, 
                parse_mode='Markdown'
            )
    
    async def create_tournament_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /createtournament command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        # Start tournament creation process
        context.user_data['state'] = 'creating_tournament'
        context.user_data['tournament_data'] = {}
        context.user_data['creation_step'] = 'type'
        
        keyboard = [
            [InlineKeyboardButton("🧍 SOLO", callback_data="tournament_type_solo")],
            [InlineKeyboardButton("👥 DUO", callback_data="tournament_type_duo")],
            [InlineKeyboardButton("👨‍👩‍👧‍👦 SQUAD", callback_data="tournament_type_squad")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎯 **Tournament Creation Started**\n\nSelect tournament type:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def process_tournament_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_text):
        """Process tournament creation steps"""
        step = context.user_data.get('creation_step')
        tournament_data = context.user_data.get('tournament_data', {})
        
        if step == 'name':
            tournament_data['name'] = message_text
            context.user_data['creation_step'] = 'date'
            await update.message.reply_text("📅 Enter tournament date (DD/MM/YYYY):")
            
        elif step == 'date':
            try:
                tournament_date = datetime.strptime(message_text, '%d/%m/%Y').date()
                tournament_data['date'] = tournament_date
                context.user_data['creation_step'] = 'time'
                await update.message.reply_text("🕘 Enter tournament time (HH:MM in 24-hour format):")
            except ValueError:
                await update.message.reply_text("❌ Invalid date format! Use DD/MM/YYYY (e.g., 28/07/2025)")
                return
                
        elif step == 'time':
            try:
                tournament_time = datetime.strptime(message_text, '%H:%M').time()
                tournament_data['time'] = tournament_time
                context.user_data['creation_step'] = 'map'
                
                # Show map selection
                keyboard = []
                for i in range(0, len(BGMI_MAPS), 2):
                    row = []
                    for j in range(2):
                        if i + j < len(BGMI_MAPS):
                            map_name = BGMI_MAPS[i + j]
                            row.append(InlineKeyboardButton(map_name, callback_data=f"map_{map_name.lower()}"))
                    keyboard.append(row)
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("📍 Select map:", reply_markup=reply_markup)
                return
            except ValueError:
                await update.message.reply_text("❌ Invalid time format! Use HH:MM (e.g., 21:30)")
                return
                
        elif step == 'entry_fee':
            try:
                entry_fee = int(message_text)
                tournament_data['entry_fee'] = entry_fee
                context.user_data['creation_step'] = 'prize_type'
                
                keyboard = [
                    [InlineKeyboardButton("💀 Kill-Based", callback_data="prize_kill_based")],
                    [InlineKeyboardButton("💰 Fixed Amount", callback_data="prize_fixed_amount")],
                    [InlineKeyboardButton("🏆 Rank-Based", callback_data="prize_rank_based")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("🎁 Select prize type:", reply_markup=reply_markup)
                return
            except ValueError:
                await update.message.reply_text("❌ Invalid entry fee! Enter a number (e.g., 50)")
                return
        
        context.user_data['tournament_data'] = tournament_data
    
    async def finish_tournament_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Complete tournament creation and save to database"""
        tournament_data = context.user_data.get('tournament_data', {})
        
        # Combine date and time for datetime field
        tournament_datetime = datetime.combine(
            tournament_data['date'], 
            tournament_data['time']
        ).replace(tzinfo=IST)
        
        # Prepare final tournament data
        final_tournament_data = {
            'name': tournament_data['name'],
            'type': tournament_data['type'],
            'datetime': tournament_datetime,
            'map': tournament_data['map'],
            'entry_fee': tournament_data['entry_fee'],
            'prize_type': tournament_data['prize_type'],
            'prize_details': tournament_data.get('prize_details', ''),
            'participants': [],
            'status': 'upcoming',
            'created_at': get_ist_time(),
            'created_by': update.effective_user.id
        }
        
        # Save to database
        tournament_id = await self.db.save_tournament(final_tournament_data)
        
        if tournament_id:
            # Generate tournament post
            tournament_post = self.generate_tournament_post(final_tournament_data, tournament_id)
            
            await update.callback_query.edit_message_text(
                f"✅ **Tournament Created Successfully!**\n\n{tournament_post}",
                parse_mode='Markdown'
            )
            
            # Clear user state
            context.user_data.clear()
        else:
            await update.callback_query.edit_message_text("❌ Error creating tournament!")
    
    def generate_tournament_post(self, tournament_data, tournament_id):
        """Generate formatted tournament post"""
        type_emoji = TOURNAMENT_TYPES.get(tournament_data['type'], '🎮')
        date_str = tournament_data['datetime'].strftime('%d/%m/%Y')
        time_str = tournament_data['datetime'].strftime('%H:%M')
        
        post = f"""🎮 **TOURNAMENT ALERT**

🏆 {tournament_data['name']}
🎯 Type: {type_emoji}
📅 Date: {date_str}
🕘 Time: {time_str}
📍 Map: {tournament_data['map']}
💰 Entry Fee: ₹{tournament_data['entry_fee']}
🎁 Prize: {tournament_data['prize_type']}

👇 Click to Join"""
        
        return post
    
    async def send_room_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sendroom command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        # Get active tournaments
        tournaments = await self.db.get_active_tournaments()
        
        if not tournaments:
            await update.message.reply_text("❌ No active tournaments found!")
            return
        
        if len(tournaments) == 1:
            # Only one tournament, proceed directly
            tournament = tournaments[0]
            context.user_data['selected_tournament'] = str(tournament['_id'])
            context.user_data['state'] = 'sending_room'
            await update.message.reply_text(
                f"📤 **Sending room details for:** {tournament['name']}\n\n"
                "Please provide room details in this format:\n"
                "Room ID: 123456\n"
                "Password: abc123"
            )
        else:
            # Multiple tournaments, let admin choose
            keyboard = []
            for tournament in tournaments:
                name = tournament['name']
                date = tournament['datetime'].strftime('%d/%m')
                button_text = f"{name} - {date}"
                callback_data = f"select_tournament_{tournament['_id']}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "📤 **Select tournament to send room details:**",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def process_room_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_text):
        """Process room details input"""
        tournament_id = context.user_data.get('selected_tournament')
        
        if not tournament_id:
            await update.message.reply_text("❌ No tournament selected!")
            return
        
        # Parse room details
        lines = message_text.strip().split('\n')
        room_data = {}
        
        for line in lines:
            if 'room id' in line.lower() or 'id:' in line.lower():
                room_data['room_id'] = line.split(':')[-1].strip()
            elif 'password' in line.lower() or 'pass:' in line.lower():
                room_data['password'] = line.split(':')[-1].strip()
        
        if not room_data.get('room_id') or not room_data.get('password'):
            await update.message.reply_text(
                "❌ Invalid format! Please use:\n"
                "Room ID: 123456\n"
                "Password: abc123"
            )
            return
        
        # Get tournament and send to participants
        tournament = await self.db.get_tournament(tournament_id)
        if not tournament:
            await update.message.reply_text("❌ Tournament not found!")
            return
        
        # Send room details to all confirmed participants
        confirmed_participants = []
        for user_id in tournament.get('participants', []):
            user = await self.db.get_user(user_id)
            if user and user.get('confirmed', False):
                confirmed_participants.append(user_id)
        
        if not confirmed_participants:
            await update.message.reply_text("❌ No confirmed participants found!")
            return
        
        # Prepare room details message
        room_msg = f"""🎮 **ROOM DETAILS - {tournament['name']}**

🏠 **Room ID:** `{room_data['room_id']}`
🔑 **Password:** `{room_data['password']}`

📅 **Tournament:** {tournament['name']}
🕘 **Time:** {tournament['datetime'].strftime('%H:%M')}
📍 **Map:** {tournament['map']}

⚠️ **IMPORTANT:**
• Join 5 minutes before start time
• Screenshot your game ID before match
• No late entries allowed
• Follow all tournament rules

🔥 **All the best, warriors!**
#DumWalaSquad"""
        
        # Send to all participants
        sent_count = 0
        for user_id in confirmed_participants:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=room_msg,
                    parse_mode='Markdown'
                )
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send room details to {user_id}: {e}")
        
        await update.message.reply_text(
            f"✅ Room details sent to {sent_count} participants!"
        )
        
        # Clear user state
        context.user_data.clear()
    
    async def confirm_payment_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /confirm command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /confirm @username")
            return
        
        username = context.args[0].replace('@', '')
        
        # Find user by username
        user = await self.db.users.find_one({'username': username})
        if not user:
            await update.message.reply_text(f"❌ User @{username} not found!")
            return
        
        # Confirm payment
        success = await self.db.confirm_payment(user['user_id'])
        
        if success:
            await update.message.reply_text(f"✅ Payment confirmed for @{username}")
            
            # Notify user
            try:
                await context.bot.send_message(
                    chat_id=user['user_id'],
                    text="✅ **Payment Confirmed!**\n\nYour payment has been verified. You'll receive room details before the tournament starts.\n\n🔥 Get ready to dominate!",
                    parse_mode='Markdown'
                )
            except:
                pass
        else:
            await update.message.reply_text(f"❌ Failed to confirm payment for @{username}")
    
    async def list_players_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /listplayers command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        tournaments = await self.db.get_active_tournaments()
        
        if not tournaments:
            await update.message.reply_text("❌ No active tournaments!")
            return
        
        for tournament in tournaments:
            participants = tournament.get('participants', [])
            
            if not participants:
                await update.message.reply_text(f"❌ No participants in {tournament['name']}")
                continue
            
            msg = f"📋 **{tournament['name']} - Participants**\n\n"
            
            confirmed_count = 0
            pending_count = 0
            
            for i, user_id in enumerate(participants, 1):
                user = await self.db.get_user(user_id)
                if user:
                    username = user.get('username', 'Unknown')
                    status = "✅" if user.get('confirmed', False) else "⏳"
                    msg += f"{i}. @{username} {status}\n"
                    
                    if user.get('confirmed', False):
                        confirmed_count += 1
                    else:
                        pending_count += 1
            
            msg += f"\n📊 **Summary:**\n"
            msg += f"✅ Confirmed: {confirmed_count}\n"
            msg += f"⏳ Pending: {pending_count}\n"
            msg += f"📝 Total: {len(participants)}"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def today_collection_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /today command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        collection = await self.db.get_daily_collection()
        today = get_ist_time().strftime('%d/%m/%Y')
        
        msg = f"""📅 **Today's Collection ({today})**

💰 **Total Amount:** ₹{collection['total_amount']}
📊 **Total Payments:** {collection['total_payments']}
💵 **Average per Payment:** ₹{collection['total_amount'] // max(collection['total_payments'], 1)}

🔥 **Boss, paisa aa raha hai!**"""
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def week_collection_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /thisweek command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        collection = await self.db.get_weekly_collection()
        
        msg = f"""📈 **This Week's Collection**

💰 **Total Amount:** ₹{collection['total_amount']}
📊 **Total Payments:** {collection['total_payments']}
💵 **Daily Average:** ₹{collection['total_amount'] // 7}

📊 **Week Performance:** {"🔥 Excellent!" if collection['total_amount'] > 5000 else "💪 Good progress!"}"""
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def month_collection_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /thismonth command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        collection = await self.db.get_monthly_collection()
        current_date = get_ist_time()
        month_name = current_date.strftime('%B %Y')
        
        msg = f"""📊 **{month_name} Collection**

💰 **Total Amount:** ₹{collection['total_amount']}
📊 **Total Payments:** {collection['total_payments']}
💵 **Daily Average:** ₹{collection['total_amount'] // max(current_date.day, 1)}

🎯 **Monthly Target:** {"🎊 Target achieved!" if collection['total_amount'] > 50000 else f"₹{50000 - collection['total_amount']} to go!"}"""
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def solo_winner_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /solo command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /solo @username kills damage")
            return
        
        username = context.args[0].replace('@', '')
        kills = context.args[1]
        damage = context.args[2]
        
        # Generate AI-powered winner message
        winner_msg = await self.ai_generator.generate_solo_winner_message(username, kills, damage)
        
        await update.message.reply_text(f"🎮 **Solo Winner Announced!**\n\n{winner_msg}", parse_mode='Markdown')
    
    async def duo_winner_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /duo command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        if len(context.args) < 4:
            await update.message.reply_text("Usage: /duo @player1 @player2 total_kills damage")
            return
        
        player1 = context.args[0].replace('@', '')
        player2 = context.args[1].replace('@', '')
        kills = context.args[2]
        damage = context.args[3]
        
        # Generate AI-powered winner message
        winner_msg = await self.ai_generator.generate_duo_winner_message(player1, player2, kills, damage)
        
        await update.message.reply_text(f"🎮 **Duo Winners Announced!**\n\n{winner_msg}", parse_mode='Markdown')
    
    async def squad_winner_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /squad command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        if len(context.args) < 6:
            await update.message.reply_text("Usage: /squad @p1 @p2 @p3 @p4 total_kills damage")
            return
        
        players = [arg.replace('@', '') for arg in context.args[:4]]
        kills = context.args[4]
        damage = context.args[5]
        
        # Generate AI-powered winner message
        winner_msg = await self.ai_generator.generate_squad_winner_message(players, kills, damage)
        
        await update.message.reply_text(f"🎮 **Squad Winners Announced!**\n\n{winner_msg}", parse_mode='Markdown')
    
    async def special_notification_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /special command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /special Your custom message here")
            return
        
        custom_message = ' '.join(context.args)
        
        # Generate AI-enhanced notification
        enhanced_msg = await self.ai_generator.enhance_custom_message(custom_message)
        
        await update.message.reply_text(f"💥 **Special Notification**\n\n{enhanced_msg}", parse_mode='Markdown')
    
    async def declare_winners_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /declarewinners command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        # Show tournament selection for winner declaration
        tournaments = await self.db.get_active_tournaments()
        
        if not tournaments:
            await update.message.reply_text("❌ No active tournaments to declare winners!")
            return
        
        keyboard = []
        for tournament in tournaments:
            name = tournament['name']
            date = tournament['datetime'].strftime('%d/%m')
            button_text = f"{name} - {date}"
            callback_data = f"declare_winner_{tournament['_id']}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🏆 **Select tournament to declare winners:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def clear_entries_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command"""
        if not is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Access denied!")
            return
        
        await update.message.reply_text("🧹 **Clear Entries Feature**\n\nThis feature is under development. Contact developer for manual entry removal.")
