"""
Message templates for BGMI Tournament Bot
Consistent formatting and styling for all bot messages
"""

from config import *
from utils.helpers import get_ist_time, format_currency

class MessageTemplates:
    """Collection of message templates for the bot"""
    
    @staticmethod
    def welcome_message(user_first_name):
        """Welcome message for new users"""
        return f"""🚨 Oye {user_first_name}! Tere jaise player ka welcome hai is killer lobby mein! 🔥

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
    
    @staticmethod
    def force_join_message():
        """Message for users who haven't joined the channel"""
        return "❌ Abhi bhi channel join nahi kiya? 😠\n\nJaldi se join karo warna entry milegi hi nahi!"
    
    @staticmethod
    def main_menu_message(user_first_name, referral_code):
        """Main menu message after channel join"""
        return f"""🔥 Lobby Access Granted! 🔥

Ab kya plan hai bhai {user_first_name}?

Tera Personal Referral Code: `{referral_code}`
Dost ko bhej, aur FREE ENTRY pa!"""
    
    @staticmethod
    def admin_dashboard_message(current_time, live_tournament_count, next_match_in):
        """Admin dashboard welcome message"""
        return f"""👑 **Welcome, Boss!**
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
    
    @staticmethod
    def tournament_creation_start():
        """Start tournament creation message"""
        return "🎯 **Tournament Creation Started**\n\nSelect tournament type:"
    
    @staticmethod
    def tournament_creation_steps():
        """Tournament creation step messages"""
        return {
            'name': "🏆 Enter tournament name:",
            'date': "📅 Enter tournament date (DD/MM/YYYY):",
            'time': "🕘 Enter tournament time (HH:MM in 24-hour format):",
            'map': "📍 Select map:",
            'entry_fee': "💰 Enter entry fee amount:",
            'prize_type': "🎁 Select prize type:"
        }
    
    @staticmethod
    def tournament_created_success():
        """Tournament creation success message"""
        return "✅ **Tournament Created Successfully!**"
    
    @staticmethod
    def tournament_post_template(tournament_data, tournament_id):
        """Generate tournament announcement post"""
        type_emoji = TOURNAMENT_TYPES.get(tournament_data['type'], '🎮')
        date_str = tournament_data['datetime'].strftime('%d/%m/%Y')
        time_str = tournament_data['datetime'].strftime('%H:%M')
        
        return f"""🎮 **TOURNAMENT ALERT**

🏆 {tournament_data['name']}
🎯 Type: {type_emoji}
📅 Date: {date_str}
🕘 Time: {time_str}
📍 Map: {tournament_data['map']}
💰 Entry Fee: ₹{tournament_data['entry_fee']}
🎁 Prize: {tournament_data['prize_type']}

👇 Click to Join"""
    
    @staticmethod
    def payment_instructions(tournament_name, entry_fee, hours_remaining):
        """Payment instructions message"""
        return f"""💰 **PAYMENT INSTRUCTIONS**

🏆 **Tournament:** {tournament_name}
💸 **Entry Fee:** ₹{entry_fee}

📱 **UPI Payment Details:**
🆔 **UPI ID:** `{UPI_ID}`
💵 **Amount:** ₹{entry_fee}
📝 **Note:** {tournament_name} - @username

📋 **Payment Steps:**
1. 📱 Open any UPI app (PhonePe, GPay, Paytm)
2. 💰 Send ₹{entry_fee} to: `{UPI_ID}`
3. 📸 Take screenshot of payment confirmation
4. 📤 Send screenshot to @Owner_ji_bgmi
5. 🔢 Copy UTR/Transaction ID from screenshot
6. 📝 Use /paid command with UTR number
7. ⌛ Wait for admin confirmation

⚠️ **IMPORTANT:**
• Include tournament name in payment note
• Keep UTR number ready
• Payment must be completed 1 hour before tournament
• No refunds after room details are shared
• Contact @Owner_ji_bgmi if payment fails

🕘 **Payment Deadline:** {hours_remaining} hours remaining"""
    
    @staticmethod
    def payment_success(tournament_name, username, utr_number, amount):
        """Payment submission success message"""
        current_time = get_ist_time().strftime('%d/%m/%Y %H:%M')
        
        return f"""✅ **Payment Submitted Successfully!**

🎮 **Tournament:** {tournament_name}
👨‍💼 **Player:** @{username}
🔢 **UTR Number:** `{utr_number}`
💰 **Amount:** ₹{amount}
🕘 **Submitted:** {current_time}

⏳ **Status:** Pending Admin Verification

📋 **Next Steps:**
1. ✅ Payment submitted to admin queue
2. 🔍 Admin will verify your payment
3. ✅ You'll get confirmation notification
4. 🎮 Room details will be sent before tournament

⚠️ **Important:**
• Keep your phone active for notifications
• Join @KyaTereSquadMeinDumHai for updates
• Contact @Owner_ji_bgmi if delayed

🎯 **Get Ready!** Tournament prep starts now!"""
    
    @staticmethod
    def payment_confirmed(username):
        """Payment confirmation message for user"""
        return f"""✅ **Payment Confirmed!**

Your payment has been verified. You'll receive room details before the tournament starts.

🔥 Get ready to dominate!"""
    
    @staticmethod
    def admin_payment_notification(username, user_id, tournament_name, amount, utr_number):
        """Admin notification for new payment"""
        current_time = get_ist_time().strftime('%d/%m/%Y %H:%M')
        
        return f"""💰 **NEW PAYMENT RECEIVED**

👨‍💼 **Player:** @{username}
🆔 **User ID:** {user_id}
🎮 **Tournament:** {tournament_name}
💵 **Amount:** ₹{amount}
🔢 **UTR:** `{utr_number}`
🕘 **Time:** {current_time}

Use: `/confirm @{username}` to approve"""
    
    @staticmethod
    def room_details_template(tournament_name, room_id, password, tournament_time, map_name):
        """Room details message template"""
        return f"""🎮 **ROOM DETAILS - {tournament_name}**

🏠 **Room ID:** `{room_id}`
🔑 **Password:** `{password}`

📅 **Tournament:** {tournament_name}
🕘 **Time:** {tournament_time}
📍 **Map:** {map_name}

⚠️ **IMPORTANT:**
• Join 5 minutes before start time
• Screenshot your game ID before match
• No late entries allowed
• Follow all tournament rules

🔥 **All the best, warriors!**
#DumWalaSquad"""
    
    @staticmethod
    def terms_and_conditions():
        """Terms and conditions message"""
        return """📜 **TERMS & CONDITIONS**

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
    
    @staticmethod
    def help_message():
        """Help and support message"""
        return """📜 **HELP & SUPPORT**

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
    
    @staticmethod
    def whatsapp_status_template(referral_code, bot_username):
        """WhatsApp status sharing template"""
        return f"""📱 **WHATSAPP STATUS READY!**

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
    
    @staticmethod
    def invite_friends_message(referral_code, bot_username, referral_count, referral_bonus):
        """Invite friends message template"""
        return f"""👥 **INVITE FRIENDS & EARN FREE ENTRY!**

🎯 **Tera Referral Code:** `{referral_code}`

📲 **Share this link:**
https://t.me/{bot_username}?start={referral_code}

🎁 **BENEFITS:**
• Every friend joins = ₹25 bonus
• 2 friends = FREE tournament entry
• 5 friends = VIP tournament access
• 10 friends = Special cash reward

📈 **Your Stats:**
• Total Referrals: {referral_count}
• Earned Bonus: ₹{referral_bonus}

💬 **Copy & send this message:**

🔥 Bhai, BGMI tournament join kar!
Daily cash prizes aur kill rewards!
Mera referral code use kar: {referral_code}
Bot link: https://t.me/{bot_username}?start={referral_code}
#FreeEntry #BGMITournament"""
    
    @staticmethod
    def no_active_tournaments():
        """Message when no tournaments are active"""
        return """❌ **No Active Tournaments**

Abhi koi tournament live nahi hai bhai!

🔔 **Stay Updated:**
• Join channel for instant notifications
• Tournament announcements daily
• Early bird discounts available

📢 Channel: @KyaTereSquadMeinDumHai"""
    
    @staticmethod
    def collection_report(period, total_amount, total_payments, additional_info=""):
        """Financial collection report template"""
        avg_amount = total_amount // max(total_payments, 1)
        
        return f"""📊 **{period} Collection**

💰 **Total Amount:** ₹{total_amount:,}
📊 **Total Payments:** {total_payments}
💵 **Average per Payment:** ₹{avg_amount}

{additional_info}"""
    
    @staticmethod
    def error_messages():
        """Collection of error messages"""
        return {
            'access_denied': "❌ Access denied!",
            'tournament_not_found': "❌ Tournament not found!",
            'invalid_format': "❌ Invalid format!",
            'user_not_found': "❌ User not found!",
            'payment_failed': "❌ Payment submission failed!",
            'already_joined': "✅ Already joined this tournament!",
            'registration_closed': "❌ Tournament registration closed!",
            'invalid_utr': "❌ Invalid UTR format! UTR number should be exactly 12 digits.",
            'no_payments': "❌ No payments found!",
            'system_error': "⚠️ System error! Try again later."
        }
    
    @staticmethod
    def success_messages():
        """Collection of success messages"""
        return {
            'payment_confirmed': "✅ Payment confirmed!",
            'tournament_joined': "✅ Successfully joined tournament!",
            'room_details_sent': "✅ Room details sent to participants!",
            'winner_announced': "🎮 Winner announced successfully!"
        }

class TournamentMessages:
    """Specific tournament-related message templates"""
    
    @staticmethod
    def solo_tournament_template(name, date, time, map_name, entry_fee, prize_details):
        """Solo tournament creation template"""
        return f"""🎮 TOURNAMENT TYPE: 🧍 SOLO
🏆 {name}
📅 Date: {date}
🕘 Time: {time}
📍 Map: {map_name}
💰 Entry Fee: ₹{entry_fee}
🎁 Prize Pool: {prize_details}

🔽 JOIN & DETAILS 🔽
[✅ Join Now] [📜 Rules] [⚠️ Disclaimer]"""
    
    @staticmethod
    def duo_tournament_template(name, date, time, map_name, entry_fee, prize_details):
        """Duo tournament creation template"""
        return f"""🎮 TOURNAMENT TYPE: 👥 DUO
🏆 {name}
📅 Date: {date}
🕘 Time: {time}
📍 Map: {map_name}
💰 Entry Fee: ₹{entry_fee} per team
🎁 Prize Pool: {prize_details}

🔽 JOIN & DETAILS 🔽
[✅ Join Now] [📜 Rules] [⚠️ Disclaimer]"""
    
    @staticmethod
    def squad_tournament_template(name, date, time, map_name, entry_fee, prize_details):
        """Squad tournament creation template"""
        return f"""🎮 TOURNAMENT TYPE: 👨‍👩‍👧‍👦 SQUAD
🏆 {name}
📅 Date: {date}
🕘 Time: {time}
📍 Map: {map_name}
💰 Entry Fee: ₹{entry_fee} per squad
🎁 Prize Pool: {prize_details}

🔽 JOIN & DETAILS 🔽
[✅ Join Now] [📜 Rules] [⚠️ Disclaimer]"""

class WinnerMessages:
    """Winner announcement message templates"""
    
    @staticmethod
    def solo_winner_fallback(username, kills, damage, victory_symbol):
        """Fallback solo winner message"""
        return f"""🔥 Bhai @{username} ne lobby mein aag laga di!

🎯 Player: @{username}
💀 Kills: {kills} | 🎯 Damage: {damage}
👑 Victory: {victory_symbol}

#DumWalaSolo #LobbyCleaner"""
    
    @staticmethod
    def duo_winner_fallback(player1, player2, kills, damage, victory_symbol):
        """Fallback duo winner message"""
        return f"""🔥 @{player1} aur @{player2} ki deadly combination!

🎯 Players: @{player1} & @{player2}
💀 Kills: {kills} | 💣 Damage: {damage}
👑 Victory Rank: {victory_symbol}

#DumWaleDuo #KhatarnakJodi"""
    
    @staticmethod
    def squad_winner_fallback(players, kills, damage, victory_symbol):
        """Fallback squad winner message"""
        players_mention = ' '.join([f"@{player}" for player in players])
        
        return f"""🔥 {players_mention} ka squad domination!

🧨 Winning Squad: Team Champions
🎯 Players: {players_mention}
💀 Total Kills: {kills} | 💣 Damage: {damage}
🚁 Victory: {victory_symbol}

#DumWalaSquad #SquadGoals"""

class ValidationMessages:
    """Input validation messages"""
    
    @staticmethod
    def invalid_date_format():
        """Invalid date format message"""
        return "❌ Invalid date format! Use DD/MM/YYYY (e.g., 28/07/2025)"
    
    @staticmethod
    def invalid_time_format():
        """Invalid time format message"""
        return "❌ Invalid time format! Use HH:MM (e.g., 21:30)"
    
    @staticmethod
    def invalid_entry_fee():
        """Invalid entry fee message"""
        return "❌ Invalid entry fee! Enter a number (e.g., 50)"
    
    @staticmethod
    def invalid_utr_format():
        """Invalid UTR format message"""
        return """❌ **Invalid UTR Format!**

UTR number should be exactly 12 digits.
Check your payment app and try again.

Example: `/paid 123456789012`"""
    
    @staticmethod
    def paid_command_usage():
        """Correct usage for /paid command"""
        return """❌ **Invalid Format!**

Correct usage: `/paid YOUR_UTR_NUMBER`
Example: `/paid 123456789012`

📝 UTR number should be 12 digits from your payment app."""
