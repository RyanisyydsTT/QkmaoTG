import json
import logging
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Qkmao API endpoint URL for custom shortening
QKMAO_API_ENDPOINT_CUSTOM = "https://qkmao.cc/api/v2"

# Function to shorten a URL using the Qkmao API with custom slug
def shorten_url(original_url, slug=None):
    endpoint = QKMAO_API_ENDPOINT_CUSTOM

    payload = {"link": original_url}
    if slug:
        payload["slug"] = slug

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses

        shortened_url_response = response.json()

        # Check if the response contains an error
        if "error" in shortened_url_response:
            return 'Error: {}'.format(shortened_url_response["error"])

        shortened_url = shortened_url_response.get("link", "Unknown")
        return shortened_url
    except requests.RequestException as e:
        logger.error("Request to Qkmao API failed: %s", e)
        return 'Error: Failed to shorten URL'

# Function to handle /short command
def short(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please provide the URL to shorten.")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.strip()

    # If user wants a random slug
    if user_input.lower() == "{rando}":
        shortened_url_response = shorten_url(context.user_data['original_url'])
        update.message.reply_text(f"Your shortened URL: {shortened_url_response}")
    else:
        # Assume user input is the desired slug
        slug = user_input
        shortened_url_response = shorten_url(context.user_data['original_url'], slug)
        update.message.reply_text(f"Your shortened URL with custom slug '{slug}': {shortened_url_response}")

def main() -> None:
    updater = Updater(token='YOUR_TELEGRAM_TOKEN', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("short", short))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
