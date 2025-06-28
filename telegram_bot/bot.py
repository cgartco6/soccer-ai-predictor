import telegram
from telegram.ext import Updater, CommandHandler
from message_templates import golden_signal_template

class PredictionBot:
    def _init_(self, token, channel_id):
        self.bot = telegram.Bot(token=token)
        self.channel_id = channel_id
        self.updater = Updater(token, use_context=True)
        
        # Register handlers
        self.updater.dispatcher.add_handler(
            CommandHandler('start', self.start)
        )
    
    def start_polling(self):
        self.updater.start_polling()
    
    def send_golden_signal(self, prediction):
        """Send formatted prediction to Telegram channel"""
        message = golden_signal_template(
            match=prediction['match'],
            confidence=prediction['confidence'],
            prediction=prediction['outcome'],
            btts_prob=prediction['btts_prob'],
            edge=prediction['value_edge'],
            odds=prediction['bookmaker_odds']
        )
        self.bot.send_message(
            chat_id=self.channel_id,
            text=message,
            parse_mode='MarkdownV2'
        )
    
    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚽ SoccerAI Prediction System Active - Golden Signals will be sent automatically"
        )

# Message template (message_templates.py)
def golden_signal_template(match, confidence, prediction, btts_prob, edge, odds):
    return f"""
🚨 GOLDEN SIGNAL ({confidence}% AI Confidence)
⚽ {match['home']} vs {match['away']}
🎯 Prediction: {prediction} | BTTS: {'Yes' if btts_prob > 0.65 else 'No'}
📊 Value Edge: {edge}% vs market

🔍 Key Factors:
• Injuries: {match['injury_impact']}% squad value affected
• Form: {match['home']} {match['home_form']} | {match['away']} {match['away_form']}
• Referee: {match['referee']} ({match['ref_stats']['avg_cards']} cards/game)

💰 Odds Comparison:
{Hollywoodbets}: {odds['Hollywoodbets']}
{Betway}: {odds['Betway']}
AI True Value: {odds['true_value']}
"""
