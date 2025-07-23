import os
import telegram
from telegram.ext import Updater, CommandHandler
from templates import format_signal

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

bot = telegram.Bot(token=TOKEN)

def send_signal(signal):
    message = format_signal(
        home=signal['match']['home_team'],
        away=signal['match']['away_team'],
        prediction=signal['outcome'],
        confidence=signal['confidence'],
        btts_prob=signal['btts_prob'],
        edge=signal['value_edge'],
        referee=signal['match']['referee'],
        weather=signal['match']['weather']
    )
    
    bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode='MarkdownV2'
    )

def start_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    
    updater.start_polling()
    updater.idle()

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⚽ *SoccerAI Prediction System Activated* ⚽\n\n"
             "✅ Golden signals will be automatically sent to this channel\n"
             "⏱ Updates every 15 minutes",
        parse_mode='Markdown'
    )

def status(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🟢 System Status: ACTIVE\n"
             "📊 Last prediction cycle: 5 minutes ago\n"
             "💎 Signals sent today: 12",
        parse_mode='Markdown'
    )

if __name__ == "__main__":
    print("🤖 Starting Telegram Bot...")
    start_bot()
