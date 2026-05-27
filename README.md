# 🎯 Study Wars - একটি গেমিফাইড স্টাডি ম্যানেজমেন্ট প্ল্যাটফর্ম

একটি **Telegram Bot + Web Dashboard** যেখানে স্টুডেন্টরা প্রতিযোগিতা করে, লিডারবোর্ডে ওঠে এবং XP/Refer সিস্টেম দিয়ে উৎসাহিত হয়।

---

## ✨ ফিচার

✅ **Telegram Bot Integration**
- নাম রেজিস্টার, ফ্যাকশন বেছে নেওয়া
- Refer সিস্টেম (100 XP প্রতি রেফার)
- Daily War auto-matching
- সময় লগ করা, লিডারবোর্ড

✅ **Web Dashboard** (HTML + API)
- Focus Timer (XP গেইন)
- Daily Tasks (করলে +30 XP)
- 1v1 Matchmaking Arena
- Global Leaderboard + Faction Ranking
- Admin Announcement Panel

✅ **Backend (Flask)**
- REST API for all operations
- JSON-based data storage
- Referral code generation
- Match making logic

---

## 🚀 Setup Guide

### **1️⃣ GitHub Setup**

```bash
# Clone করো
git clone https://github.com/তোমার-username/study-wars.git
cd study-wars

# Dependencies install করো
pip install python-telegram-bot flask flask-cors
```

### **2️⃣ Telegram Bot Setup**

#### **Step A: BotFather-এ Bot তৈরি করো**
1. Telegram-এ `@BotFather` search করো
2. `/newbot` command দাও
3. Bot name দাও: "Study Wars"
4. Bot username দাও: `study_wars_bot` (unique হতে হবে)
5. TOKEN পাবে — **copy করো**

#### **Step B: Bot Menu Button Setup**
1. BotFather-এ আবার যাও
2. `/mybots` → তোমার bot → `Bot Settings` → `Menu Button`
3. `Edit Menu Button` → URL set করো:
   - **Web App URL**: `https://hilarious-palmier-6c1235.netlify.app/`
   - (অথবা তোমার hosted dashboard URL)

#### **Step C: bot.py তে Token বসাও**
```python
TOKEN = "তোমার_সত্যিকারের_TOKEN_এখানে"  # BotFather থেকে পাওয়া
```

### **3️⃣ Flask Backend চালু করো**

```bash
# Terminal-এ
python app.py
```

Output দেখাবে:
```
🚀 Study Wars Backend Server চালু হচ্ছে...
📍 URL: http://127.0.0.1:5000
```

### **4️⃣ Telegram Bot চালু করো**

```bash
# নতুন Terminal window-এ
python bot.py
```

Output দেখাবে:
```
🚀 Study Wars Bot চালু হয়েছে!
🔗 Refer system: ✅ Active
⚡ XP System: ✅ Active
```

### **5️⃣ Web Dashboard আপলোড করো**

1. `index.html` ফাইল খোলো
2. এই line খুঁজো:
   ```javascript
   const API_URL = "https://Alsami.pythonanywhere.com/api";
   ```
   বদলে দাও তোমার Flask server URL দিয়ে:
   ```javascript
   const API_URL = "http://localhost:5000/api";  // Local
   // অথবা
   const API_URL = "https://তোমার-public-url/api";  // Production
   ```
3. Netlify-এ আপলোড করো (drag-drop)

---

## 📁 ফাইল স্ট্রাকচার

```
study-wars/
├── app.py                 # Flask Backend
├── bot.py                 # Telegram Bot
├── index.html             # Web Dashboard
├── users.json             # User data storage
├── study_data.json        # Match/Score data
├── README.md              # এই ফাইল
└── requirements.txt       # Python dependencies
```

---

## 🎮 কীভাবে ব্যবহার করবে?

### **Telegram Bot এ:**
```
/start          → Register করো, ফ্যাকশন বেছে নাও
/refer          → তোমার refer link পাবে
/dailywar       → Daily War-এ যোগ দাও (Yes/No)
/announce       → Admin announcement পাঠাও (only 5726202509)
```

### **Web Dashboard এ:**
1. **Focus Timer** → স্টাডি করো, XP পাও (10 XP/মিনিট)
2. **Daily Tasks** → Task যোগ করো, complete করলে +30 XP
3. **1v1 Arena** → Opponent খুঁজো, match করো
4. **Leaderboard** → সবার score দেখো
5. **Refer System** → Link শেয়ার করো, 100 XP পাও

---

## 🔧 Config/Customization

### **Refer System**
ফাইল: `bot.py` (line ~150)
```python
# প্রতি refer-এ points (default 100)
users[referrer_id]['xp'] = users[referrer_id].get('xp', 0) + 100
```

### **XP Earning Rates**
- Timer (স্টাডি): **10 XP/মিনিট**
- Daily Task complete: **+30 XP**
- Refer পাওয়া: **+50 XP**
- Refer দেওয়া: **+100 XP**

ফাইল: `index.html` (search করো "xpGained")

### **Flask API URL**
ফাইল: `index.html` (line ~1)
```javascript
const API_URL = "YOUR_API_URL_HERE";
```

---

## 🌐 Production Deployment

### **Option A: Render.com (Recommended)**

```bash
# 1. Render.com-এ যাও
# 2. New Web Service create করো
# 3. GitHub repo connect করো
# 4. Build command: pip install -r requirements.txt
# 5. Start command: python app.py
```

### **Option B: PythonAnywhere**

```bash
# 1. Pythonanywhere.com সাইন আপ করো
# 2. Web app create করো (Flask)
# 3. Code ফাইল আপলোড করো
# 4. app.py → wsgi.py connect করো
```

### **Option C: Heroku (Free tier বন্ধ)**
```bash
# heroku login
# heroku create study-wars-bot
# git push heroku main
```

---

## 📊 Data Files (JSON)

### **users.json**
```json
{
  "5726202509": {
    "name": "Rafiq",
    "faction": "Alpha",
    "xp": 1500,
    "referral_code": "A1B2C3D4",
    "referred_count": 5,
    "daily_war_opted": true,
    "total": 12.5
  }
}
```

### **study_data.json**
```json
{
  "today": "2024-12-19",
  "matches": {
    "m1": {
      "p1": "Rafiq",
      "p2": "Nadia",
      "p1_time": 3.5,
      "p2_time": 2.0
    }
  },
  "scores": {
    "Rafiq": 3.5,
    "Nadia": 2.0
  },
  "wins": {
    "Rafiq": 3,
    "Nadia": 1
  }
}
```

---

## 🐛 Troubleshooting

| সমস্যা | সমাধান |
|--------|--------|
| Bot offline | `python bot.py` চালু আছে কিনা check করো |
| API error | Flask server চলছে কিনা check করো (`python app.py`) |
| Dashboard blank | Browser console-এ error দেখো (F12) |
| Data not saving | JSON files read-only নয় কিনা check করো |
| Refer link না খোলা | `/start?ref_CODE` syntax check করো |

---

## 📞 Support

- **Bot Issues**: `python bot.py` আবার চালু করো
- **Server Issues**: Flask server restart করো
- **Dashboard Issues**: Browser cache clear করো (Ctrl+Shift+Del)

---

## 📜 License

**MIT License** — যেকোনো কাজে ব্যবহার করতে পারবে

---

## 👨‍💻 Author

**তোমার নাম** — Created Study Wars

---

## 🔗 Quick Links

- **Bot**: `https://t.me/study_wars_bot` (BotFather থেকে পাওয়া link)
- **Dashboard**: `https://hilarious-palmier-6c1235.netlify.app/`
- **API Docs**: Check `app.py` routes

---

## ✅ Checklist before GitHub Push

- [ ] Token secret করেছ (`.gitignore` তে add করো)
- [ ] API URL update করেছ
- [ ] Bot username setup করেছ
- [ ] Test করেছ locally
- [ ] README দেখেছ কোনো typo আছে কিনা

---

**Ready to deploy? 🚀 আজই push করো GitHub-এ!**
