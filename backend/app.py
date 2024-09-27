from flask import Flask, redirect, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

@app.route('/login')
def login():
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    response_data = response.json()
    access_token = response_data['access_token']
    
    user_response = requests.get('https://discord.com/api/users/@me', headers={
        'Authorization': f'Bearer {access_token}'
    })
    user_data = user_response.json()
    
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)