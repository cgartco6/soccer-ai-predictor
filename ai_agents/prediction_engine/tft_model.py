import tensorflow as tf
from tensorflow.keras.layers 
import Dense, LSTM, Attention, Concatenate

python ai_engine/scripts/load_historical_data.py
class TemporalFusionTransformer(tf.keras.Model):
    def _init_(self, num_features, hidden_units=128):
        super()._init_()
        # Encoder layers
        self.lstm_encoder = LSTM(hidden_units, return_sequences=True)
        self.attention = Attention()
        
        # Feature-specific processing
        self.team_dense = Dense(64, activation='relu')
        self.player_dense = Dense(64, activation='relu')
        self.env_dense = Dense(32, activation='relu')
        
        # Output heads
        self.outcome_head = Dense(3, activation='softmax')  # Win/Draw/Loss
        self.btts_head = Dense(1, activation='sigmoid')     # BTTS probability

    def call(self, inputs):
        # Input structure: [team_stats, player_stats, env_data]
        team_features = self.team_dense(inputs[0])
        player_features = self.player_dense(inputs[1])
        env_features = self.env_dense(inputs[2])
        
        # Temporal processing
        fused = Concatenate()([team_features, player_features, env_features])
        temporal = self.lstm_encoder(fused)
        context = self.attention([temporal, temporal])
        
        # Predictions
        outcome = self.outcome_head(context)
        btts = self.btts_head(context)
        return outcome, btts
