"""
Study Wars - টেলিগ্রাম মিনি অ্যাপ ব্যাকএন্ড সার্ভার
Railway/Render এর জন্য production-ready
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import random
import logging

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask অ্যাপ সেটআপ
app = Flask(__name__, template_folder='templates')
CORS(app)

# ═══════════════════════════════════════════════════════════════════════════
# কনফিগুরেশন
# ═══════════════════════════════════════════════════════════════════════════

# Environment variables থেকে PORT পড়া
PORT = int(os.getenv('PORT', 5000))

# ডেটা ফাইলের পাথ (Persistent storage এর জন্য)
DATA_DIR = os.getenv('DATA_DIR', './data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATA_FILE = os.path.join(DATA_DIR, "users_data.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
MATCHES_FILE = os.path.join(DATA_DIR, "active_matches.json")
ANNOUNCEMENT_FILE = os.path.join(DATA_DIR, "announcement.json")

# ═══════════════════════════════════════════════════════════════════════════
# ডেটা ম্যানেজমেন্ট ফাংশন
# ═══════════════════════════════════════════════════════════════════════════

def load_users():
    """ব্যবহারকারীর ডেটা লোড করা"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"❌ Error loading users: {e}")
    return {}

def save_users(users):
    """ব্যবহারকারীর ডেটা সংরক্ষণ করা"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        logger.info("✅ Users data saved")
    except Exception as e:
        logger.error(f"❌ Error saving users: {e}")

def load_history():
    """গেম হিস ট্রি লোড করা"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"❌ Error loading history: {e}")
    return []

def save_history(history):
    """গেম হিস্ট্রি সংরক্ষণ করা"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"❌ Error saving history: {e}")

def load_matches():
    """সক্রিয় ম্যাচ লোড করা"""
    try:
        if os.path.exists(MATCHES_FILE):
            with open(MATCHES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"❌ Error loading matches: {e}")
    return {}

def save_matches(matches):
    """সক্রিয় ম্যাচ সংরক্ষণ করা"""
    try:
        with open(MATCHES_FILE, 'w', encoding='utf-8') as f:
            json.dump(matches, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"❌ Error saving matches: {e}")

def load_announcement():
    """ঘোষণা লোড করা"""
    try:
        if os.path.exists(ANNOUNCEMENT_FILE):
            with open(ANNOUNCEMENT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get('message', '')
    except:
        pass
    return ""

def save_announcement(msg):
    """ঘোষণা সংরক্ষণ করা"""
    try:
        with open(ANNOUNCEMENT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'message': msg}, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"❌ Error saving announcement: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# API ইএন্ডপয়েন্ট
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """মূল পৃষ্ঠা - HTML serve করা"""
    return render_template('index_main.html')

@app.route('/api/health', methods=['GET'])
def health():
    """স্বাস্থ্য পরীক্ষা - Railway/Render এর জন্য"""
    return jsonify({'status': 'ok', 'message': 'Server is running ✅'})

@app.route('/api/register', methods=['POST'])
def register():
    """নতুন ব্যবহারকারী নিবন্ধন"""
    try:
        data = request.json
        user_id = data.get('user_id')
        name = data.get('name', 'Unknown')
        team = data.get('team', 'Alpha')
        
        users = load_users()
        
        if user_id in users:
            return jsonify({'error': 'Already registered'}), 400
        
        users[user_id] = {
            'name': name,
            'team': team,
            'study_hours': 0.0,
            'total_xp': 0,
            'level': 1,
            'streak': 0,
            'daily_hours': 0.0,
            'weekly_hours': 0.0,
            'created_at': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat(),
            'badges': [],
            'refer_code': str(random.randint(100000, 999999)),
            'refer_count': 0,
            'daily_war_opted': False
        }
        
        save_users(users)
        logger.info(f"✅ New user registered: {name} ({user_id})")
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_hours', methods=['POST'])
def update_hours():
    """পড়ার ঘণ্টা আপডেট করা"""
    try:
        data = request.json
        user_id = data.get('user_id')
        hours = float(data.get('hours', 0))
        
        users = load_users()
        
        if user_id not in users:
            return jsonify({'error': 'User not found'}), 404
        
        # আপডেট করা
        users[user_id]['study_hours'] += hours
        users[user_id]['daily_hours'] += hours
        users[user_id]['weekly_hours'] += hours
        users[user_id]['total_xp'] += int(hours * 10)  # 1 ঘণ্টা = 10 XP
        users[user_id]['last_update'] = datetime.now().isoformat()
        
        # লেভেল আপডেট
        xp = users[user_id]['total_xp']
        level = 1 + (xp // 100)
        users[user_id]['level'] = level
        
        save_users(users)
        
        # হিস্ট্রিতে যোগ করা
        history = load_history()
        history.append({
            'user_id': user_id,
            'name': users[user_id]['name'],
            'hours': hours,
            'timestamp': datetime.now().isoformat(),
            'team': users[user_id]['team']
        })
        save_history(history)
        
        logger.info(f"✅ {users[user_id]['name']} added {hours} hours")
        
        return jsonify({
            'success': True,
            'message': 'Hours updated',
            'new_total': users[user_id]['study_hours'],
            'xp_gained': int(hours * 10),
            'new_level': level
        })
    
    except Exception as e:
        logger.error(f"❌ Update hours error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    """ব্যবহারকারী তথ্য পাওয়া"""
    try:
        users = load_users()
        
        if user_id not in users:
            return jsonify({'error': 'User not found'}), 404
        
        user = users[user_id]
        
        # র‍্যাংক গণনা করা
        sorted_users = sorted(users.items(), 
                            key=lambda x: x[1]['study_hours'], 
                            reverse=True)
        rank = next((i+1 for i, (uid, _) in enumerate(sorted_users) 
                    if uid == user_id), 0)
        
        return jsonify({
            **user,
            'user_id': user_id,
            'rank': rank
        })
    
    except Exception as e:
        logger.error(f"❌ Get user error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    """লিডারবোর্ড পাওয়া"""
    try:
        users = load_users()
        
        sorted_users = sorted(users.items(),
                            key=lambda x: x[1]['study_hours'],
                            reverse=True)
        
        leaderboard_data = []
        for rank, (user_id, user) in enumerate(sorted_users[:50], 1):
            leaderboard_data.append({
                'rank': rank,
                'user_id': user_id,
                'name': user['name'],
                'study_hours': user['study_hours'],
                'level': user['level'],
                'team': user['team'],
                'total_xp': user['total_xp']
            })
        
        return jsonify({'leaderboard': leaderboard_data})
    
    except Exception as e:
        logger.error(f"❌ Leaderboard error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/team_stats', methods=['GET'])
def team_stats():
    """টিম পরিসংখ্যান পাওয়া"""
    try:
        users = load_users()
        teams = {}
        
        for user_id, user in users.items():
            team = user['team']
            if team not in teams:
                teams[team] = {
                    'name': team,
                    'total_hours': 0,
                    'members': 0,
                    'avg_level': 0,
                    'total_xp': 0
                }
            
            teams[team]['total_hours'] += user['study_hours']
            teams[team]['members'] += 1
            teams[team]['total_xp'] += user['total_xp']
        
        # গড় লেভেল গণনা করা
        for team in teams:
            if teams[team]['members'] > 0:
                teams[team]['avg_level'] = round(
                    teams[team]['total_xp'] / (teams[team]['members'] * 100)
                )
        
        # র‍্যাঙ্ক করা
        sorted_teams = sorted(teams.items(),
                            key=lambda x: x[1]['total_hours'],
                            reverse=True)
        
        team_stats_data = []
        for rank, (team_name, stats) in enumerate(sorted_teams, 1):
            stats['rank'] = rank
            team_stats_data.append(stats)
        
        return jsonify({'teams': team_stats_data})
    
    except Exception as e:
        logger.error(f"❌ Team stats error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/announcement', methods=['GET'])
def get_announcement():
    """বর্তমান ঘোষণা পাওয়া"""
    try:
        announcement = load_announcement()
        return jsonify({'announcement': announcement})
    except Exception as e:
        logger.error(f"❌ Get announcement error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/announcement', methods=['POST'])
def set_announcement():
    """নতুন ঘোষণা সেট করা (অ্যাডমিন)"""
    try:
        data = request.json
        admin_key = data.get('admin_key')
        announcement = data.get('announcement', '')
        
        # সিম্পল অ্যাডমিন চেক
        if admin_key != os.getenv('ADMIN_KEY', 'admin123'):
            return jsonify({'error': 'Invalid admin key'}), 401
        
        save_announcement(announcement)
        logger.info(f"✅ Announcement updated: {announcement}")
        
        return jsonify({'success': True, 'message': 'Announcement saved'})
    
    except Exception as e:
        logger.error(f"❌ Set announcement error: {e}")
        return jsonify({'error': str(e)}), 500

# ═══════════════════════════════════════════════════════════════════════════
# এরর হ্যান্ডেলিং
# ═══════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    """404 ত্রুটি হ্যান্ডলার"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 ত্রুটি হ্যান্ডলার"""
    logger.error(f"❌ Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ═══════════════════════════════════════════════════════════════════════════
# মূল
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Railroad এর জন্য 0.0.0.0 এ শুনতে হবে
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=debug
    )
