from flask import Blueprint, request, jsonify
from google import genai
import os
import uuid
from dotenv import load_dotenv
from database import get_db

load_dotenv()

chat_bp = Blueprint('chat', __name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI Business Assistant for Codenixia — a tech company offering software development, 
AI automation, and digital transformation services.

You help users with:
- Information about Codenixia's services (web dev, mobile apps, AI solutions, cloud)
- Course and training program queries
- Pricing and package information
- General business automation queries
- Lead qualification questions

Always be professional, helpful, and concise. If asked something outside business scope,
politely redirect to business topics. End responses with a helpful follow-up question.

Pricing (approximate):
- Web Development: ₹50,000 – ₹5,00,000
- Mobile App: ₹80,000 – ₹8,00,000  
- AI Automation: ₹1,00,000 – ₹10,00,000
- Training Programs: ₹15,000 – ₹50,000

Always suggest users fill the contact form for detailed quotes.
"""

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    session_id = data.get('session_id', str(uuid.uuid4()))

    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        bot_reply = response.text.strip()

        # Log to database
        conn = get_db()
        conn.execute(
            'INSERT INTO chat_logs (session_id, user_message, bot_response) VALUES (?, ?, ?)',
            (session_id, user_message, bot_reply)
        )
        conn.commit()
        conn.close()

        return jsonify({
            'reply': bot_reply,
            'session_id': session_id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500