from flask import Blueprint, jsonify, request
import json

bp = Blueprint('endpoints', __name__)

@bp.route('/signals', methods=['GET'])
def get_signals():
    try:
        with open('golden_signals.json') as f:
            signals = [json.loads(line) for line in f]
        return jsonify(signals[:10])  # Return last 10 signals
    except FileNotFoundError:
        return jsonify({"error": "No signals found"}), 404

@bp.route('/predict', methods=['POST'])
def predict_match():
    data = request.json
    # In production: Actual prediction logic
    return jsonify({
        "prediction": "draw",
        "confidence": 85.7,
        "btts_prob": 0.68,
        "value_edge": 22.3
    })
