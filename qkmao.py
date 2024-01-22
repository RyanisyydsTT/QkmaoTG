import json
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext
print("Thank you for using Qkmao link shortener, please make sure you have already changed the Telegram Token"
# Qkmao API endpoint URL for custom shortening
QKMAO_API_ENDPOINT_CUSTOM = "https://qkmao.cc/api/v2"

# Function to shorten a URL using the Qkmao API with custom slug
def shorten_url_custom(original_url, slug):
    endpoint = "{}?random".format(QKMAO_API_ENDPOINT_CUSTOM)

    payload = {"link": original_url}
    if slug:
        payload["slug"] = slug

    response = requests.post(endpoint, json=payload)

    try:
        print("Response from Qkmao API: {}".format(response.text))
        # Add this line for debugging

        # Check if the response is None or empty
        if not response.text:
            return 'Error: Empty response received from the API'

        # Attempt to parse the JSON response
        try:
            shortened_url_response = json.loads(response.text)
            print("Parsed JSON response: {}".format(shortened_url_response))

            # Check if the response contains an error
            if "error" in shortened_url_response:
                return 'Error: {}'.format(shortened_url_response["error"])

            # Extract the shortened URL from the response
            shortened_url = shortened_url_response.get("link", "Unknown")
            return shortened_url
        except json.JSONDecodeError as e:
            return 'Error: Failed to parse JSON response - {}'.format(e)

    except Exception as e:
        return f'Error: {e}'

# Function to handle /short command
def short(update: Update, context: CallbackContext) -> None:
    if context.args:
        original_url = context.args[0]
        slug = context.args[1] if len(context.args) > 1 else None

        shortened_url_response = shorten_url_custom(original_url, slug)

        # Send a concise message with the shortened URL
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'感謝您使用Qkmao.cc縮網址服務\n您的縮短連結：{shortened_url_response}')
    else:
        update.message.reply_text('請提供要縮短的URL。範例: /short https://example.com [optional_slug]')

# Function to handle /credit command
def credit(update: Update, context: CallbackContext) -> None:
    # Create an InlineKeyboardMarkup with two buttons
    keyboard = [
        [
            InlineKeyboardButton("Bot", url="https://github.com/RyanisyydsTT/QkmaoTG"),
            InlineKeyboardButton("Link Shortener", url="https://github.com/MagicTeaMC/MagicTeaMC"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Create an embedded message with the title 'Credits'
    update.message.reply_text(
        '感謝您使用Qkmao.cc縮網址服務\n'
        'Credits列表:',
        reply_markup=reply_markup
    )

def main() -> None:
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram Bot API token
    updater = Updater(token='FILL_YOU_TELEGRAM_TOKEN', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the /short command handler
    dp.add_handler(CommandHandler("short", short))

    # Register the /credit command handler
    dp.add_handler(CommandHandler("credit", credit))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
