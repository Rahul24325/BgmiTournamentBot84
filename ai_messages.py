"""
AI-powered message generation for BGMI Tournament Bot
"""

import aiohttp
import asyncio
import random
from config import AI_API_KEY, AI_API_URL, VICTORY_NUMBERS, HASHTAGS
import logging

logger = logging.getLogger(__name__)

class AIMessageGenerator:
    def __init__(self):
        self.api_key = AI_API_KEY
        self.api_url = AI_API_URL
    
    async def generate_solo_winner_message(self, username, kills, damage):
        """Generate AI-powered solo winner message"""
        victory_symbol = random.choice(VICTORY_NUMBERS.get(1, ["❶"]))
        hashtag = HASHTAGS.get('solo', '#DumWalaSolo #LobbyCleaner')
        
        try:
            # Try AI generation first
            prompt = f"""Generate an exciting BGMI solo winner announcement for player @{username} with {kills} kills and {damage} damage. 
            Use Hindi-English mix style, gaming slang, and make it energetic. Include emojis and victory celebration.
            Keep it under 200 characters. Make it unique and catchy."""
            
            ai_message = await self.call_ai_api(prompt)
            
            if ai_message:
                return f"""{ai_message}

🎯 Player: @{username}
💀 Kills: {kills} | 🎯 Damage: {damage}
👑 Victory: {victory_symbol}

{hashtag}"""
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
        
        # Fallback to template messages
        templates = [
            f"🔥 Bhai @{username} ne lobby mein aag laga di!",
            f"💀 @{username} - The Ultimate Kill Machine!",
            f"👑 @{username} ne sabko school kar diya!",
            f"⚡ @{username} ka domination shuru!",
            f"🎯 @{username} - Lobby ka Badshah!"
        ]
        
        selected_template = random.choice(templates)
        
        return f"""{selected_template}

🎯 Player: @{username}
💀 Kills: {kills} | 🎯 Damage: {damage}  
👑 Victory: {victory_symbol}

{hashtag}"""
    
    async def generate_duo_winner_message(self, player1, player2, kills, damage):
        """Generate AI-powered duo winner message"""
        victory_symbol = random.choice(VICTORY_NUMBERS.get(1, ["❶"]))
        hashtag = HASHTAGS.get('duo', '#DumWaleDuo #KhatarnakJodi')
        
        try:
            prompt = f"""Generate an exciting BGMI duo winner announcement for players @{player1} and @{player2} with {kills} total kills and {damage} damage. 
            Use Hindi-English mix style, emphasize teamwork and partnership. Include emojis and celebration.
            Keep it under 200 characters. Make it unique."""
            
            ai_message = await self.call_ai_api(prompt)
            
            if ai_message:
                return f"""{ai_message}

🎯 Players: @{player1} & @{player2}
💀 Kills: {kills} | 💣 Damage: {damage}
👑 Victory Rank: {victory_symbol}

{hashtag}"""
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
        
        # Fallback templates
        templates = [
            f"🔥 @{player1} aur @{player2} ki deadly combination!",
            f"👥 @{player1} & @{player2} - Unstoppable Duo!",
            f"💪 @{player1} @{player2} ne teamwork dikhaya!",
            f"⚡ @{player1} @{player2} ka perfect sync!",
            f"🎯 @{player1} @{player2} - Dynamic Destroyers!"
        ]
        
        selected_template = random.choice(templates)
        
        return f"""{selected_template}

🎯 Players: @{player1} & @{player2}
💀 Kills: {kills} | 💣 Damage: {damage}
👑 Victory Rank: {victory_symbol}

{hashtag}"""
    
    async def generate_squad_winner_message(self, players, kills, damage):
        """Generate AI-powered squad winner message"""
        victory_symbol = random.choice(VICTORY_NUMBERS.get(1, ["❶"]))
        hashtag = HASHTAGS.get('squad', '#DumWalaSquad #SquadGoals')
        
        players_mention = ' '.join([f"@{player}" for player in players])
        
        try:
            prompt = f"""Generate an exciting BGMI squad winner announcement for team with players {', '.join(players)} with {kills} total kills and {damage} damage. 
            Use Hindi-English mix style, emphasize squad coordination and teamwork. Include emojis and celebration.
            Keep it under 200 characters. Make it energetic."""
            
            ai_message = await self.call_ai_api(prompt)
            
            if ai_message:
                return f"""{ai_message}

🧨 Winning Squad: Team Champions
🎯 Players: {players_mention}
💀 Total Kills: {kills} | 💣 Damage: {damage}
🚁 Victory: {victory_symbol}

{hashtag}"""
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
        
        # Fallback templates
        templates = [
            f"🔥 {players_mention} ka squad domination!",
            f"👨‍👩‍👧‍👦 {players_mention} - Ultimate Team!",
            f"💪 {players_mention} ne squad goals achieve kiye!",
            f"⚡ {players_mention} ka perfect coordination!",
            f"🎯 {players_mention} - Champion Squad!"
        ]
        
        selected_template = random.choice(templates)
        
        return f"""{selected_template}

🧨 Winning Squad: Team Champions
🎯 Players: {players_mention}
💀 Total Kills: {kills} | 💣 Damage: {damage}
🚁 Victory: {victory_symbol}

{hashtag}"""
    
    async def enhance_custom_message(self, custom_message):
        """Enhance custom message with AI"""
        try:
            prompt = f"""Enhance this BGMI tournament message with gaming emojis, Hindi-English mix style, and make it more exciting: "{custom_message}"
            Keep the original meaning but make it more energetic and engaging. Add relevant emojis."""
            
            ai_message = await self.call_ai_api(prompt)
            
            if ai_message:
                return ai_message
        except Exception as e:
            logger.error(f"AI enhancement failed: {e}")
        
        # Fallback - just add emojis to original message
        enhanced = f"🔥 {custom_message} 🔥\n\n#DumWalaSquad #BGMITournament"
        return enhanced
    
    async def call_ai_api(self, prompt):
        """Call AI API for message generation"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a creative BGMI tournament announcer who writes in Hindi-English mix style with gaming slang and enthusiasm.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 150,
                'temperature': 0.9
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        message = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                        return message
                    else:
                        logger.error(f"AI API error: {response.status}")
                        return None
        except asyncio.TimeoutError:
            logger.error("AI API timeout")
            return None
        except Exception as e:
            logger.error(f"AI API call failed: {e}")
            return None
    
    async def generate_tournament_announcement(self, tournament_data):
        """Generate AI-powered tournament announcement"""
        try:
            prompt = f"""Create an exciting BGMI tournament announcement for:
            Name: {tournament_data['name']}
            Type: {tournament_data['type']}
            Entry Fee: ₹{tournament_data['entry_fee']}
            Map: {tournament_data['map']}
            
            Use Hindi-English mix style, include emojis, make it engaging and encourage participation.
            Keep it under 300 characters."""
            
            ai_message = await self.call_ai_api(prompt)
            
            if ai_message:
                return ai_message
        except Exception as e:
            logger.error(f"Tournament announcement generation failed: {e}")
        
        # Fallback template
        type_emoji = {'solo': '🧍', 'duo': '👥', 'squad': '👨‍👩‍👧‍👦'}.get(tournament_data['type'], '🎮')
        
        return f"""🎮 **{tournament_data['name']}** 🎮

{type_emoji} **Tournament Alert!**
📍 Map: {tournament_data['map']}
💰 Entry: ₹{tournament_data['entry_fee']}
🏆 Big prizes waiting!

Join karo aur domination dikhao! 🔥

#DumWalaSquad #BGMITournament"""
    
    async def generate_room_details_message(self, tournament_name, room_id, password):
        """Generate AI-powered room details message"""
        try:
            prompt = f"""Create an exciting room details announcement for BGMI tournament "{tournament_name}" with room ID {room_id} and password {password}.
            Use Hindi-English mix style, include important instructions and motivational content.
            Keep it professional but energetic."""
            
            ai_message = await self.call_ai_api(prompt)
            
            if ai_message:
                return ai_message
        except Exception as e:
            logger.error(f"Room details generation failed: {e}")
        
        # Fallback template
        return f"""🎮 **ROOM DETAILS - {tournament_name}**

🏠 **Room ID:** `{room_id}`
🔑 **Password:** `{password}`

🔥 **Warriors, time to show your skills!**
⚡ Join room 5 minutes before start
📸 Screenshot your game ID
💪 Give your best performance!

All the best! #DumWalaSquad"""
