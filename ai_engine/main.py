from agents.data_miner import DataMiner
from agents.predictor import PredictionEngine
from agents.validator import SignalValidator
import time
import os
import json

class SoccerAIPredictor:
    def __init__(self):
        self.data_miner = DataMiner()
        self.predictor = PredictionEngine(model_path='models/tft_model.h5')
        self.validator = SignalValidator()
        
    def run(self):
        print("⚽ Starting SoccerAI Prediction Engine")
        while True:
            try:
                print("\n" + "="*50)
                print(f"🚀 Prediction Cycle: {time.ctime()}")
                
                # Step 1: Get match data
                matches = self.data_miner.get_todays_matches()
                print(f"📥 Fetched {len(matches)} matches")
                
                # Step 2: Generate predictions
                raw_predictions = self.predictor.predict(matches)
                print(f"🧠 Generated {len(raw_predictions)} predictions")
                
                # Step 3: Validate signals
                golden_signals = self.validator.filter_signals(
                    raw_predictions, 
                    min_confidence=0.92,
                    min_edge=0.15
                )
                print(f"💎 Found {len(golden_signals)} golden signals")
                
                # Step 4: Output signals
                self.output_signals(golden_signals)
                
                # Step 5: Wait for next cycle
                time.sleep(900)  # 15 minutes
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                time.sleep(300)  # Retry after 5 minutes
            
    def output_signals(self, signals):
        # Save to database
        self.save_to_db(signals)
        
        # Send to Telegram
        from telegram_bot import send_signal
        for signal in signals:
            send_signal(signal)
    
    def save_to_db(self, signals):
        # Database integration would go here
        with open('golden_signals.json', 'a') as f:
            for signal in signals:
                f.write(json.dumps(signal) + '\n')

if __name__ == "__main__":
    predictor = SoccerAIPredictor()
    predictor.run()
