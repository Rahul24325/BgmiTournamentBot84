"""
Helper utilities for BGMI Tournament Bot
"""

from datetime import datetime, timezone, timedelta
from config import ADMIN_ID, IST
import logging

logger = logging.getLogger(__name__)

def is_admin(user_id):
    """Check if user is admin"""
    return user_id == ADMIN_ID

def get_ist_time():
    """Get current time in IST"""
    return datetime.now(IST)

def format_datetime(dt, format_str='%d/%m/%Y %H:%M'):
    """Format datetime to string"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)
    return dt.strftime(format_str)

def parse_datetime(date_str, time_str):
    """Parse date and time strings to datetime object"""
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        dt = datetime.combine(date_obj, time_obj).replace(tzinfo=IST)
        return dt
    except ValueError as e:
        logger.error(f"Error parsing datetime: {e}")
        return None

def calculate_time_difference(future_time, current_time=None):
    """Calculate time difference in a readable format"""
    if current_time is None:
        current_time = get_ist_time()
    
    if future_time <= current_time:
        return "Tournament has started"
    
    diff = future_time - current_time
    
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days} days, {hours} hours"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    else:
        return f"{minutes} minutes"

def validate_utr_number(utr):
    """Validate UTR number format"""
    return utr.isdigit() and len(utr) == 12

def generate_referral_link(bot_username, referral_code):
    """Generate referral link"""
    return f"https://t.me/{bot_username}?start={referral_code}"

def format_currency(amount):
    """Format currency amount"""
    return f"₹{amount:,}"

def truncate_text(text, max_length=50):
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_tournament_status_emoji(status):
    """Get emoji for tournament status"""
    status_emojis = {
        'upcoming': '⏳',
        'live': '🔴',
        'completed': '✅',
        'cancelled': '❌'
    }
    return status_emojis.get(status, '❓')

def get_payment_status_emoji(confirmed):
    """Get emoji for payment status"""
    return "✅" if confirmed else "⏳"

def sanitize_username(username):
    """Sanitize username for display"""
    if not username:
        return "Unknown"
    return username.replace('@', '')

def calculate_prize_pool(participants, entry_fee):
    """Calculate total prize pool"""
    return len(participants) * entry_fee

def get_tournament_type_emoji(tournament_type):
    """Get emoji for tournament type"""
    type_emojis = {
        'solo': '🧍',
        'duo': '👥',
        'squad': '👨‍👩‍👧‍👦'
    }
    return type_emojis.get(tournament_type, '🎮')

def format_participant_count(count):
    """Format participant count with emoji"""
    if count == 0:
        return "❌ No participants"
    elif count < 10:
        return f"👥 {count} players"
    elif count < 50:
        return f"🔥 {count} players"
    else:
        return f"🚀 {count} players"

def validate_tournament_time(tournament_datetime):
    """Validate if tournament time is in the future"""
    current_time = get_ist_time()
    return tournament_datetime > current_time

def get_next_tournament_time(tournaments):
    """Get the next upcoming tournament time"""
    if not tournaments:
        return None
    
    current_time = get_ist_time()
    upcoming = [t for t in tournaments if t['datetime'] > current_time]
    
    if not upcoming:
        return None
    
    return min(upcoming, key=lambda x: x['datetime'])['datetime']

def format_match_history_entry(tournament, index):
    """Format a match history entry"""
    status_emoji = get_tournament_status_emoji(tournament.get('status', 'unknown'))
    name = truncate_text(tournament.get('name', 'Unknown Tournament'), 30)
    date = format_datetime(tournament.get('datetime', get_ist_time()), '%d/%m/%Y')
    
    return f"{index}. {status_emoji} {name} - {date}"

def calculate_referral_bonus(referral_count, bonus_per_referral=25):
    """Calculate total referral bonus"""
    return referral_count * bonus_per_referral

def get_free_entries_available(referral_bonus, entry_fee=50):
    """Calculate free entries available from referral bonus"""
    return referral_bonus // entry_fee

def format_leaderboard_entry(index, username, status):
    """Format leaderboard entry"""
    status_text = "✅ Confirmed" if status else "⏳ Pending"
    return f"{index}. @{sanitize_username(username)} - {status_text}"

def generate_tournament_hashtags(tournament_type):
    """Generate hashtags for tournament type"""
    base_hashtags = "#DumWalaSquad #BGMITournament"
    
    type_hashtags = {
        'solo': "#SoloChampion #LobbyCleaner",
        'duo': "#DuoMasters #KhatarnakJodi",
        'squad': "#SquadGoals #TeamWork"
    }
    
    specific_hashtags = type_hashtags.get(tournament_type, "#Gaming")
    return f"{specific_hashtags} {base_hashtags}"

def validate_payment_amount(amount, expected_amount):
    """Validate payment amount"""
    return amount == expected_amount

def get_time_until_tournament(tournament_datetime):
    """Get human readable time until tournament"""
    current_time = get_ist_time()
    
    if tournament_datetime <= current_time:
        return "Tournament has started"
    
    time_diff = tournament_datetime - current_time
    
    if time_diff.days > 0:
        return f"{time_diff.days} days remaining"
    
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m remaining"
    else:
        return f"{minutes} minutes remaining"

def create_tournament_summary(tournament):
    """Create a summary of tournament details"""
    type_emoji = get_tournament_type_emoji(tournament['type'])
    participants_count = len(tournament.get('participants', []))
    prize_pool = calculate_prize_pool(tournament.get('participants', []), tournament['entry_fee'])
    time_until = get_time_until_tournament(tournament['datetime'])
    
    return {
        'type_emoji': type_emoji,
        'participants_count': participants_count,
        'prize_pool': prize_pool,
        'time_until': time_until,
        'formatted_datetime': format_datetime(tournament['datetime'])
    }

class MessageFormatter:
    """Class for formatting messages consistently"""
    
    @staticmethod
    def success(message):
        return f"✅ **{message}**"
    
    @staticmethod
    def error(message):
        return f"❌ **{message}**"
    
    @staticmethod
    def warning(message):
        return f"⚠️ **{message}**"
    
    @staticmethod
    def info(message):
        return f"ℹ️ **{message}**"
    
    @staticmethod
    def loading(message):
        return f"⏳ **{message}**"

def log_user_action(user_id, action, details=None):
    """Log user actions for debugging"""
    logger.info(f"User {user_id} performed action: {action}" + (f" - {details}" if details else ""))

def safe_int_conversion(value, default=0):
    """Safely convert value to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def chunk_list(lst, chunk_size):
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def generate_unique_tournament_id():
    """Generate unique tournament ID"""
    import uuid
    return str(uuid.uuid4())[:8].upper()
