from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json, os, random, hashlib

app = Flask(__name__)
CORS(app)

# File paths for data storage
DATA_FILE = "users_data.json"
HISTORY_FILE = "history.json"
MATCHES_FILE = "active_matches.json"
ANNOUNCEMENT_FILE = "announcement.json"

# ═══════════════════════════════════════════════════════════════════════════
# DATA MANAGEMENT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def load_users():
    """Load all user data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save user data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_history():
    """Load game history"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Save game history"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_announcement():
    """Load current announcement"""
    if os.path.exists(ANNOUNCEMENT_FILE):
        with open(ANNOUNCEMENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('message', '')
    return ""

def save_announcement(msg):
    """Save announcement"""
    with open(ANNOUNCEMENT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'message': msg}, f, ensure_ascii=False)

def load_matches():
    """Load active matches"""
    if os.path.exists(MATCHES_FILE):
        with open(MATCHES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_matches(matches):
    """Save active matches"""
    with open(MATCHES_FILE, 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

def generate_referral_code(user_id):
    """Generate unique referral code"""
    return hashlib.md5(str(user_id).encode()).hexdigest()[:8].upper()

def check_daily_reset(users):
    """Reset daily stats if new day"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    for uid, user in users.items():
        if user.get('last_reset') != today:
            # Calculate streak
            if user.get('daily', 0) > 0:
                user['streak'] = user.get('streak', 0) + 1
            else:
                user['streak'] = 0
            
            user['maxStreak'] = max(user.get('maxStreak', 0), user.get('streak', 0))
            user['daily'] = 0
            user['last_reset'] = today
    
    return users

# ═══════════════════════════════════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/get_data', methods=['GET'])
def get_data():
    """Get all data (users, history, announcement)"""
    users = load_users()
    users = check_daily_reset(users)
    save_users(users)
    
    history = load_history()
    announcement = load_announcement()
    
    return jsonify({
        'users': users,
        'history': history,
        'announcement': announcement,
        'lastReset': datetime.now().strftime('%Y-%m-%d'),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/update_data', methods=['POST'])
def update_data():
    """Update user data (called after adding time, completing tasks, etc)"""
    try:
        data = request.json
        my_id = data.get('myId')
        user_data = data.get('userData')
        announcement = data.get('announcement')
        
        if not my_id or not user_data:
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
        
        # Load existing users
        users = load_users()
        users[my_id] = user_data
        save_users(users)
        
        # Save announcement if provided
        if announcement:
            save_announcement(announcement)
        
        return jsonify({'status': 'success', 'message': 'Data updated'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/find_match', methods=['POST'])
def find_match():
    """Find 1v1 match for a user"""
    try:
        data = request.json
        my_id = data.get('myId')
        
        if not my_id:
            return jsonify({'status': 'error'}), 400
        
        users = load_users()
        matches = load_matches()
        
        # Check if user already has a match
        for match_id, match_data in matches.items():
            if match_data.get('player1') == my_id:
                if match_data.get('player2'):
                    return jsonify({
                        'status': 'matched',
                        'opponent': match_data['player2']
                    })
                else:
                    return jsonify({
                        'status': 'waiting',
                        'players_in_queue': sum(1 for m in matches.values() if not m.get('player2'))
                    })
        
        # Create new match for this player
        available_users = [uid for uid in users.keys() if uid != my_id]
        
        if not available_users:
            match_id = f"match_{datetime.now().timestamp()}"
            matches[match_id] = {
                'player1': my_id,
                'player2': None,
                'created_at': datetime.now().isoformat()
            }
            save_matches(matches)
            return jsonify({
                'status': 'waiting',
                'players_in_queue': 1
            })
        
        # Try to match with someone already waiting
        waiting_match = None
        for m_id, m_data in matches.items():
            if m_data.get('player2') is None and m_data.get('player1') != my_id:
                waiting_match = m_id
                break
        
        if waiting_match:
            # Match found!
            matches[waiting_match]['player2'] = my_id
            save_matches(matches)
            return jsonify({
                'status': 'matched',
                'opponent': matches[waiting_match]['player1']
            })
        else:
            # Create new match, wait for opponent
            match_id = f"match_{datetime.now().timestamp()}"
            matches[match_id] = {
                'player1': my_id,
                'player2': None,
                'created_at': datetime.now().isoformat()
            }
            save_matches(matches)
            return jsonify({
                'status': 'waiting',
                'players_in_queue': len([m for m in matches.values() if not m.get('player2')])
            })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cancel_match', methods=['POST'])
def cancel_match():
    """Cancel active match"""
    try:
        data = request.json
        my_id = data.get('myId')
        
        matches = load_matches()
        matches_to_remove = []
        
        for match_id, match_data in matches.items():
            if match_data.get('player1') == my_id or match_data.get('player2') == my_id:
                matches_to_remove.append(match_id)
        
        for match_id in matches_to_remove:
            del matches[match_id]
        
        save_matches(matches)
        return jsonify({'status': 'success'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/save_todo', methods=['POST'])
def save_todo():
    """Save user's todo list"""
    try:
        data = request.json
        my_id = data.get('myId')
        todos = data.get('todos', [])
        
        users = load_users()
        if my_id not in users:
            users[my_id] = {}
        
        users[my_id]['todos'] = todos
        save_users(users)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/add_history', methods=['POST'])
def add_history():
    """Add game result to history"""
    try:
        data = request.json
        history = load_history()
        
        history.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'winner': data.get('winner'),
            'daily': data.get('daily', 0),
            'timestamp': datetime.now().isoformat()
        })
        
        save_history(history)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/set_announcement', methods=['POST'])
def set_announcement():
    """Set announcement (admin only)"""
    try:
        data = request.json
        admin_id = data.get('adminId')
        message = data.get('message')
        
        # Simple admin check (replace with proper auth in production)
        ADMIN_IDS = ['5726202509']
        if admin_id not in ADMIN_IDS:
            return jsonify({'status': 'error', 'message': 'Not authorized'}), 401
        
        save_announcement(message)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get_referral_code', methods=['POST'])
def get_referral_code():
    """Get or generate referral code for user"""
    try:
        data = request.json
        my_id = data.get('myId')
        
        users = load_users()
        if my_id not in users:
            return jsonify({'status': 'error'}), 400
        
        user = users[my_id]
        
        # Generate referral code if not exists
        if 'referral_code' not in user:
            user['referral_code'] = generate_referral_code(my_id)
            user['referred_count'] = 0
            save_users(users)
        
        return jsonify({
            'status': 'success',
            'referral_code': user['referral_code'],
            'referred_count': user.get('referred_count', 0),
            'bonus_xp': user.get('referred_count', 0) * 100  # 100 XP per referral
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/use_referral', methods=['POST'])
def use_referral():
    """Use referral code when registering"""
    try:
        data = request.json
        my_id = data.get('myId')
        referral_code = data.get('referralCode', '').upper()
        
        users = load_users()
        
        if my_id not in users:
            return jsonify({'status': 'error', 'message': 'User not found'}), 400
        
        # Find who referred this code
        referrer_id = None
        for uid, user in users.items():
            if user.get('referral_code') == referral_code:
                referrer_id = uid
                break
        
        if not referrer_id:
            return jsonify({'status': 'error', 'message': 'Invalid referral code'}), 400
        
        if referrer_id == my_id:
            return jsonify({'status': 'error', 'message': 'Cannot refer yourself'}), 400
        
        # Check if already used
        if users[my_id].get('used_referral'):
            return jsonify({'status': 'error', 'message': 'Already used a referral'}), 400
        
        # Add bonus to referrer and mark as used
        users[referrer_id]['xp'] = users[referrer_id].get('xp', 0) + 100
        users[referrer_id]['referred_count'] = users[referrer_id].get('referred_count', 0) + 1
        
        users[my_id]['xp'] = users[my_id].get('xp', 0) + 50
        users[my_id]['used_referral'] = True
        users[my_id]['referred_by'] = referrer_id
        
        save_users(users)
        
        return jsonify({
            'status': 'success',
            'message': f'✅ {users[referrer_id]["name"]} কে 100 XP দিয়েছ!',
            'referrer_name': users[referrer_id]['name']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/toggle_daily_war', methods=['POST'])
def toggle_daily_war():
    """Toggle daily war participation"""
    try:
        data = request.json
        my_id = data.get('myId')
        opted = data.get('opted', False)
        
        users = load_users()
        if my_id not in users:
            return jsonify({'status': 'error'}), 400
        
        users[my_id]['daily_war_opted'] = opted
        save_users(users)
        
        return jsonify({
            'status': 'success',
            'message': '✅ Daily War ' + ('enabled' if opted else 'disabled')
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get_daily_war', methods=['POST'])
def get_daily_war():
    """Get daily war opponent for user"""
    try:
        data = request.json
        my_id = data.get('myId')
        
        users = load_users()
        if my_id not in users or not users[my_id].get('daily_war_opted'):
            return jsonify({'status': 'error', 'message': 'Not opted in daily war'}), 400
        
        # Check if user already has a daily war
        matches = load_matches()
        today = datetime.now().strftime('%Y%m%d')
        
        for match_id, match in matches.items():
            if today in match_id and match.get('is_daily'):
                if match.get('player1') == my_id:
                    opponent_id = match.get('player2')
                    if opponent_id and opponent_id in users:
                        return jsonify({
                            'status': 'matched',
                            'opponent': opponent_id,
                            'opponent_name': users[opponent_id]['name'],
                            'opponent_daily': users[opponent_id].get('daily', 0)
                        })
                elif match.get('player2') == my_id:
                    opponent_id = match.get('player1')
                    if opponent_id and opponent_id in users:
                        return jsonify({
                            'status': 'matched',
                            'opponent': opponent_id,
                            'opponent_name': users[opponent_id]['name'],
                            'opponent_daily': users[opponent_id].get('daily', 0)
                        })
        
        # No match found, create new daily war
        opted_users = [uid for uid, user in users.items() 
                      if user.get('daily_war_opted') and uid != my_id]
        
        if not opted_users:
            return jsonify({'status': 'no_opponents'})
        
        opponent_id = random.choice(opted_users)
        
        match_id = f"daily_war_{my_id}_{opponent_id}_{today}"
        new_match = {
            'player1': my_id,
            'player2': opponent_id,
            'type': 'daily_war',
            'created_at': datetime.now().isoformat(),
            'is_daily': True
        }
        
        matches[match_id] = new_match
        save_matches(matches)
        
        return jsonify({
            'status': 'matched',
            'opponent': opponent_id,
            'opponent_name': users[opponent_id]['name'],
            'opponent_daily': users[opponent_id].get('daily', 0)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("🚀 Study Wars Backend Server চালু হচ্ছে...")
    print("📍 URL: http://127.0.0.1:5000")
    print("🎯 API: http://127.0.0.1:5000/api/get_data")
    print("\n⚠️  Ctrl+C দিয়ে থামাতে পারবে\n")
    
    # Create initial data files if they don't exist
    if not os.path.exists(DATA_FILE):
        save_users({})
    if not os.path.exists(HISTORY_FILE):
        save_history([])
    if not os.path.exists(ANNOUNCEMENT_FILE):
        save_announcement("")
    if not os.path.exists(MATCHES_FILE):
        save_matches({})
    
    app.run(debug=True, host='0.0.0.0', port=5000)
