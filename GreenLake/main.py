from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from deviceApp import device_bp
from subscriptionApp import subscription_bp
from userbaseApp import userbase_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

# ─── Register blueprints ──────────────────────────────────────────────────────
app.register_blueprint(device_bp)
app.register_blueprint(subscription_bp)
app.register_blueprint(userbase_bp)

# ─── Serve frontend pages ─────────────────────────────────────────────────────
@app.route('/')
def home():
    return send_from_directory(BASE_DIR, 'GreenLakeTools.html')

@app.route('/GreenLakeTools.html')
def greenlake_tools():
    return send_from_directory(BASE_DIR, 'GreenLakeTools.html')

@app.route('/DeviceManagement.html')
def device_management():
    return send_from_directory(BASE_DIR, 'DeviceManagement.html')

@app.route('/Subscriptionmanagement.html')
def subscription_management():
    return send_from_directory(BASE_DIR, 'Subscriptionmanagement.html')

@app.route('/UserManagement.html')
def user_management():
    return send_from_directory(BASE_DIR, 'UserManagement.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)