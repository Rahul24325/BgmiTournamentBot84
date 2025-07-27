"""
Database operations for BGMI Tournament Bot
"""

import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from config import MONGODB_URI, DATABASE_NAME, IST
from utils.helpers import get_ist_time
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]
        
        # Collections
        self.users = self.db.users
        self.tournaments = self.db.tournaments
        self.payments = self.db.payments
        self.referrals = self.db.referrals
        self.match_history = self.db.match_history
        
    async def save_user(self, user_data):
        """Save or update user data"""
        try:
            await self.users.update_one(
                {'user_id': user_data['user_id']},
                {'$set': user_data},
                upsert=True
            )
            logger.info(f"User {user_data['user_id']} saved successfully")
        except Exception as e:
            logger.error(f"Error saving user: {e}")
    
    async def get_user(self, user_id):
        """Get user data"""
        try:
            user = await self.users.find_one({'user_id': user_id})
            return user
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            return None
    
    async def save_tournament(self, tournament_data):
        """Save tournament data"""
        try:
            result = await self.tournaments.insert_one(tournament_data)
            logger.info(f"Tournament saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving tournament: {e}")
            return None
    
    async def get_tournament(self, tournament_id):
        """Get tournament by ID"""
        try:
            from bson import ObjectId
            tournament = await self.tournaments.find_one({'_id': ObjectId(tournament_id)})
            return tournament
        except Exception as e:
            logger.error(f"Error fetching tournament {tournament_id}: {e}")
            return None
    
    async def get_active_tournaments(self):
        """Get all active tournaments"""
        try:
            current_time = get_ist_time()
            tournaments = await self.tournaments.find({
                'status': 'upcoming',
                'datetime': {'$gte': current_time}
            }).sort('datetime', 1).to_list(length=10)
            return tournaments
        except Exception as e:
            logger.error(f"Error fetching active tournaments: {e}")
            return []
    
    async def join_tournament(self, tournament_id, user_id):
        """Add user to tournament participants"""
        try:
            from bson import ObjectId
            result = await self.tournaments.update_one(
                {'_id': ObjectId(tournament_id)},
                {'$addToSet': {'participants': user_id}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error joining tournament: {e}")
            return False
    
    async def save_payment(self, payment_data):
        """Save payment information"""
        try:
            result = await self.payments.insert_one(payment_data)
            logger.info(f"Payment saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving payment: {e}")
            return None
    
    async def get_payment(self, user_id, tournament_id=None):
        """Get payment information"""
        try:
            query = {'user_id': user_id}
            if tournament_id:
                query['tournament_id'] = tournament_id
            payment = await self.payments.find_one(query, sort=[('created_at', -1)])
            return payment
        except Exception as e:
            logger.error(f"Error fetching payment: {e}")
            return None
    
    async def confirm_payment(self, user_id, tournament_id=None):
        """Confirm user payment"""
        try:
            query = {'user_id': user_id}
            if tournament_id:
                query['tournament_id'] = tournament_id
            
            result = await self.payments.update_one(
                query,
                {'$set': {'confirmed': True, 'confirmed_at': get_ist_time()}},
                sort=[('created_at', -1)]
            )
            
            # Also update user status
            await self.users.update_one(
                {'user_id': user_id},
                {'$set': {'paid': True, 'confirmed': True}}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error confirming payment: {e}")
            return False
    
    async def add_referral(self, user_id, referral_code):
        """Add referral relationship"""
        try:
            # Extract referrer ID from code
            if referral_code.startswith('REF'):
                referrer_id = int(referral_code[3:])
                
                # Check if referrer exists
                referrer = await self.get_user(referrer_id)
                if referrer and referrer_id != user_id:
                    # Save referral
                    referral_data = {
                        'referrer_id': referrer_id,
                        'referred_id': user_id,
                        'referral_code': referral_code,
                        'created_at': get_ist_time(),
                        'bonus_given': False
                    }
                    
                    await self.referrals.insert_one(referral_data)
                    
                    # Update user with referrer info
                    await self.users.update_one(
                        {'user_id': user_id},
                        {'$set': {'referred_by': referrer_id}}
                    )
                    
                    logger.info(f"Referral added: {referrer_id} -> {user_id}")
                    return True
        except Exception as e:
            logger.error(f"Error adding referral: {e}")
        return False
    
    async def get_referrals(self, user_id):
        """Get referrals made by user"""
        try:
            referrals = await self.referrals.find({'referrer_id': user_id}).to_list(length=100)
            return referrals
        except Exception as e:
            logger.error(f"Error fetching referrals: {e}")
            return []
    
    async def get_user_tournaments(self, user_id):
        """Get tournaments user has participated in"""
        try:
            tournaments = await self.tournaments.find(
                {'participants': user_id}
            ).sort('datetime', -1).to_list(length=50)
            return tournaments
        except Exception as e:
            logger.error(f"Error fetching user tournaments: {e}")
            return []
    
    async def save_match_result(self, result_data):
        """Save match result"""
        try:
            result = await self.match_history.insert_one(result_data)
            logger.info(f"Match result saved with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving match result: {e}")
            return None
    
    async def get_daily_collection(self, date=None):
        """Get daily payment collection"""
        try:
            if not date:
                date = get_ist_time().date()
            
            start_date = datetime.combine(date, datetime.min.time()).replace(tzinfo=IST)
            end_date = start_date + timedelta(days=1)
            
            pipeline = [
                {
                    '$match': {
                        'confirmed': True,
                        'confirmed_at': {'$gte': start_date, '$lt': end_date}
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'total_amount': {'$sum': '$amount'},
                        'total_payments': {'$sum': 1}
                    }
                }
            ]
            
            result = await self.payments.aggregate(pipeline).to_list(length=1)
            if result:
                return result[0]
            return {'total_amount': 0, 'total_payments': 0}
        except Exception as e:
            logger.error(f"Error getting daily collection: {e}")
            return {'total_amount': 0, 'total_payments': 0}
    
    async def get_weekly_collection(self, start_date=None):
        """Get weekly payment collection"""
        try:
            if not start_date:
                today = get_ist_time().date()
                start_date = today - timedelta(days=today.weekday())
            
            start_datetime = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=IST)
            end_datetime = start_datetime + timedelta(days=7)
            
            pipeline = [
                {
                    '$match': {
                        'confirmed': True,
                        'confirmed_at': {'$gte': start_datetime, '$lt': end_datetime}
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'total_amount': {'$sum': '$amount'},
                        'total_payments': {'$sum': 1}
                    }
                }
            ]
            
            result = await self.payments.aggregate(pipeline).to_list(length=1)
            if result:
                return result[0]
            return {'total_amount': 0, 'total_payments': 0}
        except Exception as e:
            logger.error(f"Error getting weekly collection: {e}")
            return {'total_amount': 0, 'total_payments': 0}
    
    async def get_monthly_collection(self, year=None, month=None):
        """Get monthly payment collection"""
        try:
            current_date = get_ist_time()
            if not year:
                year = current_date.year
            if not month:
                month = current_date.month
            
            start_date = datetime(year, month, 1).replace(tzinfo=IST)
            if month == 12:
                end_date = datetime(year + 1, 1, 1).replace(tzinfo=IST)
            else:
                end_date = datetime(year, month + 1, 1).replace(tzinfo=IST)
            
            pipeline = [
                {
                    '$match': {
                        'confirmed': True,
                        'confirmed_at': {'$gte': start_date, '$lt': end_date}
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'total_amount': {'$sum': '$amount'},
                        'total_payments': {'$sum': 1}
                    }
                }
            ]
            
            result = await self.payments.aggregate(pipeline).to_list(length=1)
            if result:
                return result[0]
            return {'total_amount': 0, 'total_payments': 0}
        except Exception as e:
            logger.error(f"Error getting monthly collection: {e}")
            return {'total_amount': 0, 'total_payments': 0}
