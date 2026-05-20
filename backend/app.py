from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

from database import init_db
from routes.chat import chat_bp
from routes.leads import leads_bp
from routes.dashboard import dashboard_bp

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = os.getenv('SECRET_KEY', 'codenixia-secret-2026')
CORS(app)

# Register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(leads_bp)
app.register_blueprint(dashboard_bp)

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('../frontend', 'dashboard.html')

if __name__ == '__main__':
    init_db()
    print("🚀 Codenixia AI Assistant running at http://localhost:5000")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)