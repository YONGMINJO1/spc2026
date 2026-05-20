from flask import Flask ,render_template, redirect, requests
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
client_redirect = os.getenv("NAVER_REDIRECT_URL")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/naver/callback')
def naver_callback():
    code = requests.args.get("code")
    state = requests.args.get("")

# @app.route('/login')
# def login():
    
#     auth_url = (

#     )

#     print(auth_url)

#     return redirect(auth_url)