import telegram
from telegram.ext import Updater
from templates import golden_signal_template

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@your_channel"

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_signal(signal):
    message = golden_signal_template(
        match=signal['match'],
        confidence=signal['outcome_confidence'],
        prediction=signal['outcome'],
        btts_prob=signal['btts_prob'],
        edge=signal['value_edge']
    )
    
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode='MarkdownV2'
    )

def start_polling():
    updater = Updater(TELEGRAM_TOKEN)
    updater.start_polling()
    
    # Add command handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))

def start_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⚽ SoccerAI Prediction System Active - Signals will arrive automatically"
    )

if __name__ == "__main__":
    start_polling()
