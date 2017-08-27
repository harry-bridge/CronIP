import os

# Telegram stuff
bot_key = os.environ.get('bot_key')
bot_url = os.environ.get('bot_url') + bot_key
chat_id = os.environ.get('chat_id')

# API auth
api_key = os.environ.get('api_key')
api_email = os.environ.get('api_email')

# Base API request stuff
base_url = os.environ.get('base_url')
zone_id = os.environ.get('zone_id')

dns_id = os.environ.get('dns_id')
