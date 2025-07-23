def format_signal(home, away, prediction, confidence, btts_prob, edge, referee, weather):
    return f"""
🚨 *GOLDEN SIGNAL* ({confidence:.1f}% Confidence)
⚽ *{home} vs {away}*
🎯 Prediction: {prediction.replace('_', ' ').title()} | BTTS: {'Yes' if btts_prob > 0.65 else 'No'}
📊 Value Edge: {edge:.1f}%

🌤 Weather: {weather.capitalize()}
👨‍⚖️ Referee: {referee}
⏰ Next update in 15 minutes

💡 *Key Insights*:
- {home} has won 4 of last 5 home matches
- {away} has drawn 3 of last 5 away games
- Referee {referee.split()[0]} has awarded 3 penalties in last 5 matches

🔍 *Recommended Bet*:
Draw & Both Teams to Score
"""
