import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers import (
    start_command,
    help_command,
    calculate_command,
    handle_message,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def main():
    """Start the Telegram bot."""

    application = Application.builder().token(BOT_TOKEN).build()

    # Bot commands
    application.add_handler(
        CommandHandler("start", start_command)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("calculate", calculate_command)
    )

    # Normal text messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    logger.info("QuickMath bot is starting...")

    # Start Telegram polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
