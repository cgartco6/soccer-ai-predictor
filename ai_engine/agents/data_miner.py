import requests
import yaml
import os
import random
from datetime import datetime

class DataMiner:
    def __init__(self):
        with open('../config/bookmakers.yml') as f:
            self.config = yaml.safe_load(f)
        
    def get_todays_matches(self):
        # In production: Fetch from real APIs
        # For demo: Generate mock data
        return [self._mock_match_data(i) for i in range(10)]
    
    def _mock_match_data(self, match_id):
        teams = ["Arsenal", "Chelsea", "Liverpool", "Man City", "Man Utd", "Tottenham"]
        referees = ["M. Oliver", "A. Taylor", "P. Tierney", "C. Pawson"]
        weather = ["sunny", "cloudy", "rainy", "stormy"]
        
        return {
            'match_id': match_id,
            'home_team': random.choice(teams),
            'away_team': random.choice(teams),
            'date': datetime.now().strftime("%Y-%m-%d"),
            'odds': {
                'home_win': round(random.uniform(1.5, 4.0), 2),
                'draw': round(random.uniform(3.0, 5.0), 2),
                'away_win': round(random.uniform(2.0, 5.0), 2)
            },
            'weather': random.choice(weather),
            'referee': random.choice(referees),
            'home_form': random.randint(3, 15),  # Points from last 5 matches
            'away_form': random.randint(3, 15),
            'injuries': random.randint(0, 4)
        }
