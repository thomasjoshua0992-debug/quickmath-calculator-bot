import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Make sure the token exists
if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is missing. "
        "Please add BOT_TOKEN to your environment variables."
    )
