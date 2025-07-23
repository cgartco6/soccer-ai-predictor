from flask import Blueprint, jsonify
import requests

signals_bp = Blueprint('signals', __name__)

@signals_bp.route('/golden_signals', methods=['GET'])
def get_golden_signals():
    try:
        response = requests.get('http://ai-engine:5000/current_signals')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@signals_bp.route('/send_to_telegram/<signal_id>', methods=['POST'])
def send_signal_to_telegram(signal_id):
    # Implementation to forward signal to Telegram
    return jsonify({'status': 'sent', 'signal_id': signal_id})
