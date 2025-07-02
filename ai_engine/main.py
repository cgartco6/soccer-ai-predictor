from agents.data_miner import DataMiner
from agents.predictor import PredictionEngine
from agents.validator import SignalValidator
import time

class SoccerAIPredictor:
    def __init__(self):
        self.data_miner = DataMiner()
        self.predictor = PredictionEngine(model_path='models/tft_model.h5')
        self.validator = SignalValidator()
        
    def run(self):
        while True:
            # Step 1: Collect fresh data
            matches = self.data_miner.get_todays_matches()
            
            # Step 2: Generate predictions
            raw_predictions = self.predictor.predict(matches)
            
            # Step 3: Validate signals
            golden_signals = self.validator.filter_signals(
                raw_predictions, 
                min_confidence=0.92,
                min_edge=0.15
            )
            
            # Step 4: Output signals
            self.send_to_telegram(golden_signals)
            
            # Step 5: Wait for next cycle
            time.sleep(900)  # 15 minutes
            
    def send_to_telegram(self, signals):
        from telegram_bot import send_signal
        for signal in signals:
            send_signal(signal)

if __name__ == "__main__":
    predictor = SoccerAIPredictor()
    predictor.run()
