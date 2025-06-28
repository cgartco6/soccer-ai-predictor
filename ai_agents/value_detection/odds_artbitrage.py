def detect_value(prediction_prob, bookmaker_odds):
    """
    Calculate value edge over bookmaker odds
    :param prediction_prob: AI-predicted probability (0-1)
    :param bookmaker_odds: Decimal odds from bookmaker
    :return: Value percentage edge
    """
    bookmaker_implied_prob = 1 / bookmaker_odds
    value_edge = (prediction_prob - bookmaker_implied_prob) / bookmaker_implied_prob
    return max(0, value_edge) * 100  # Return positive edge only

def find_arbitrage(bookmaker_odds):
    """
    Identify cross-bookmaker arbitrage opportunities
    :param bookmaker_odds: Dict of {'Hollywoodbets': 2.10, 'Betway': 2.30, ...}
    """
    inverse_sum = sum(1/odd for odd in bookmaker_odds.values())
    if inverse_sum < 1:
        profit_percent = (1 - inverse_sum) * 100
        return {
            'opportunity': True,
            'profit_percent': round(profit_percent, 2),
            'optimal_stakes': calculate_stakes(bookmaker_odds)
        }
    return {'opportunity': False}

def calculate_stakes(odds_dict, total_stake=100):
    """Calculate optimal stake distribution for arbitrage"""
    total_inverse = sum(1/odd for odd in odds_dict.values())
    return {bookmaker: round((1/odd) / total_inverse * total_stake, 2) 
            for bookmaker, odd in odds_dict.items()}
