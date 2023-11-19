from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/bot-status', methods=['GET'])
def bot_status():
    # Get your bot's status here and return it as a response
    return jsonify({'status': 'Online'})

if __name__ == '__main__':
    app.run(port=5000)