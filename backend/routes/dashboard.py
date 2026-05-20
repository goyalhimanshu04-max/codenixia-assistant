from flask import Blueprint, jsonify
from database import get_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    conn = get_db()

    total_leads = conn.execute('SELECT COUNT(*) as count FROM leads').fetchone()['count']
    total_chats = conn.execute('SELECT COUNT(*) as count FROM chat_logs').fetchone()['count']

    recent_leads = conn.execute(
        'SELECT * FROM leads ORDER BY created_at DESC LIMIT 5'
    ).fetchall()

    interests = conn.execute('''
        SELECT interest, COUNT(*) as count 
        FROM leads 
        WHERE interest != ''
        GROUP BY interest 
        ORDER BY count DESC
    ''').fetchall()

    daily_leads = conn.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM leads
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        LIMIT 7
    ''').fetchall()

    conn.close()

    return jsonify({
        'total_leads': total_leads,
        'total_chats': total_chats,
        'recent_leads': [dict(r) for r in recent_leads],
        'interests': [dict(i) for i in interests],
        'daily_leads': [dict(d) for d in daily_leads]
    })