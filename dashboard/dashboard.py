from flask import Flask, render_template, request, redirect, url_for
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import sqlfu

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set up your Discord OAuth2 credentials
os.environ['OAUTH2_CLIENT_ID'] = os.getenv('OAUTH2_CLIENT_ID')
os.environ['OAUTH2_CLIENT_SECRET'] = os.getenv('OAUTH2_CLIENT_SECRET')
os.environ['OAUTH2_REDIRECT_URI'] = os.getenv('OAUTH2_REDIRECT_URI')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set up the OAuth2 session
oauth = OAuth2Session(os.getenv('OAUTH2_CLIENT_ID'), redirect_uri=os.getenv('OAUTH2_REDIRECT_URI'), scope='identify guilds')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    authorization_url, _ = oauth.authorization_url('https://discord.com/api/oauth2/authorize')
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    token = oauth.fetch_token(
        'https://discord.com/api/oauth2/token',
        client_secret=os.getenv('OAUTH2_CLIENT_SECRET'),
        authorization_response=request.url,
    )
    discord = OAuth2Session(os.getenv('OAUTH2_CLIENT_ID'), token=token)
    user = discord.get('https://discord.com/api/users/@me').json()
    guilds = discord.get('https://discord.com/api/users/@me/guilds').json()
    return render_template('servers.html', user=user, guilds=guilds)

@app.route('/warned')
def warned_users():
    warned_users = sqlfu.sqlfunc('SELECT * FROM warns', ())
    return render_template('warned.html', warned_users=warned_users)

@app.route('/kicked')
def kicked_users():
    kicked_users = sqlfu.sqlfunc('SELECT * FROM kicks', ())
    return render_template('kicked.html', kicked_users=kicked_users)

@app.route('/banned')
def banned_users():
    banned_users = sqlfu.sqlfunc('SELECT * FROM bans', ())
    return render_template('banned.html', banned_users=banned_users)

if __name__ == "__main__":
    app.run(debug=True)