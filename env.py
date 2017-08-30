import os

# Telegram stuff
bot_key = os.environ.get('cronip_bot_key')
bot_url = os.environ.get('cronip_bot_url') + bot_key
chat_id = os.environ.get('cronip_chat_id')

# API auth
api_key = os.environ.get('cronip_api_key')
api_email = os.environ.get('cronip_api_email')

# Base API request stuff
base_url = os.environ.get('cronip_base_url')
zone_id = os.environ.get('cronip_zone_id')

dns_id = os.environ.get('cronip_dns_id')
