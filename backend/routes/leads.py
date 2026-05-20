from flask import Blueprint, request, jsonify
from database import get_db
from automation.email_notify import send_lead_notification

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/api/leads', methods=['POST'])
def submit_lead():
    data = request.get_json()

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    lead_data = {
        'name': name,
        'email': email,
        'phone': data.get('phone', ''),
        'company': data.get('company', ''),
        'interest': data.get('interest', ''),
        'message': data.get('message', ''),
        'source': data.get('source', 'website')
    }

    try:
        conn = get_db()
        conn.execute('''
            INSERT INTO leads (name, email, phone, company, interest, message, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            lead_data['name'], lead_data['email'], lead_data['phone'],
            lead_data['company'], lead_data['interest'],
            lead_data['message'], lead_data['source']
        ))
        conn.commit()
        conn.close()

        # Automation: Form Submission → Email Notification
        send_lead_notification(lead_data)

        return jsonify({
            'success': True,
            'message': f"Thank you {name}! We'll contact you within 24 hours."
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@leads_bp.route('/api/leads', methods=['GET'])
def get_leads():
    """Admin: fetch all leads"""
    conn = get_db()
    leads = conn.execute(
        'SELECT * FROM leads ORDER BY created_at DESC'
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in leads])