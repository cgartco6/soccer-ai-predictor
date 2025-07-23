from flask import Flask, jsonify
from endpoints import bp as endpoints_bp

app = Flask(__name__)
app.register_blueprint(endpoints_bp)

@app.route('/')
def status():
    return jsonify({
        "status": "active",
        "system": "SoccerAI Prediction API",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
