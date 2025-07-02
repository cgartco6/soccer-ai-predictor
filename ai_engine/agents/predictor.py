import tensorflow as tf
import numpy as np
import joblib

class PredictionEngine:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.scaler = joblib.load('models/scaler.pkl')
        
    def predict(self, matches):
        predictions = []
        for match in matches:
            # Preprocess features
            features = self._extract_features(match)
            scaled_features = self.scaler.transform([features])
            
            # Generate prediction
            outcome_prob, btts_prob = self.model.predict(scaled_features)
            
            predictions.append({
                'match': match,
                'outcome': self._decode_outcome(outcome_prob),
                'outcome_confidence': float(np.max(outcome_prob)),
                'btts_prob': float(btts_prob[0][0]),
                'value_edge': self._calculate_value_edge(outcome_prob, match['odds'])
            })
        return predictions
    
    def _calculate_value_edge(self, probabilities, bookmaker_odds):
        true_odds = 1 / probabilities
        best_market_odds = max(bookmaker_odds.values())
        return (true_odds / best_market_odds - 1) * 100
    
    def _decode_outcome(self, probs):
        outcomes = ['home_win', 'draw', 'away_win']
        return outcomes[np.argmax(probs)]
