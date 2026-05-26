# ⚔️ Study Wars - Telegram Mini App

> পড়াশোনার যুদ্ধে বন্ধুদের সাথে প্রতিযোগিতা করুন!

একটি সম্পূর্ণ **production-ready** Telegram মিনি অ্যাপ যা পড়াশোনার সময় ট্র্যাক করে এবং লিডারবোর্ড তৈরি করে।

---

## 📋 বিষয়বস্তু

- [বৈশিষ্ট্য](#বৈশিষ্ট্য)
- [সিস্টেম প্রয়োজনীয়তা](#সিস্টেম-প্রয়োজনীয়তা)
- [স্থানীয় সেটআপ](#স্থানীয়-সেটআপ)
- [Railway এ Deploy করা](#railway-এ-deploy-করা)
- [Render এ Deploy করা](#render-এ-deploy-করা)
- [পরিবেশ ভেরিয়েবল](#পরিবেশ-ভেরিয়েবল)
- [API ডকুমেন্টেশন](#api-ডকুমেন্টেশন)
- [সমস্যা সমাধান](#সমস্যা-সমাধান)

---

## ✨ বৈশিষ্ট্য

### 👤 ব্যবহারকারী সিস্টেম
- ✅ Telegram ইন্টিগ্রেশন (Mini App)
- ✅ ব্যবহারকারী নিবন্ধন এবং প্রোফাইল
- ✅ টিম সিস্টেম (Alpha, Beta, Gamma, Delta)
- ✅ লেভেল এবং XP ট্র্যাকিং

### ⏰ পড়া ট্র্যাকিং
- ✅ দৈনিক পড়ার সময় লগ করা
- ✅ সাপ্তাহিক এবং মাসিক পরিসংখ্যান
- ✅ স্ট্রিক ট্র্যাকার
- ✅ XP গেইন সিস্টেম

### 🏆 প্রতিযোগিতা
- ✅ লাইভ লিডারবোর্ড
- ✅ টিম পরিসংখ্যান
- ✅ দৈনিক চ্যাম্পিয়ন
- ✅ সপ্তাহান্তের বোনাস পয়েন্ট

### 🎁 গেমিফিকেশন
- ✅ ব্যাজ সিস্টেম
- ✅ রেফারেল প্রোগ্রাম
- ✅ ঘোষণা সিস্টেম
- ✅ লাইভ ম্যাচ আপডেট

---

## 📦 সিস্টেম প্রয়োজনীয়তা

### নূন্যতম প্রয়োজন
- Python 3.11+
- Git
- Telegram Account
- Railway/Render Account

### পাইথন লাইব্রেরি
```bash
Flask==3.0.0
Flask-CORS==4.0.0
python-telegram-bot==20.5
gunicorn==21.2.0
python-dotenv==1.0.0
```

---

## 🚀 স্থানীয় সেটআপ

### ধাপ ১: রিপোজিটরি ক্লোন করা

```bash
git clone https://github.com/yourusername/study-wars.git
cd study-wars
```

### ধাপ ২: Virtual Environment তৈরি করা

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### ধাপ ৩: Dependencies ইনস্টল করা

```bash
pip install -r requirements.txt
```

### ধাপ ৪: Environment Variables সেট করা

```bash
# .env.example কপি করুন
cp .env.example .env

# এবং নিজের মান দিয়ে সম্পাদনা করুন
```

**উদাহরণ `.env` ফাইল:**

```ini
BOT_TOKEN=8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ
WEB_APP_URL=http://localhost:5000
PORT=5000
FLASK_ENV=development
ADMIN_KEY=admin123
```

### ধাপ ৫: ডেটা ডিরেক্টরি তৈরি করা

```bash
mkdir -p data
```

### ধাপ ৬: Flask সার্ভার চালু করা (একটি টার্মিনাল)

```bash
python app.py
```

আউটপুট:
```
 * Running on http://127.0.0.1:5000
```

### ধাপ ৭: বট চালু করা (নতুন টার্মিনাল)

```bash
python bot.py
```

আউটপুট:
```
🤖 Study Wars বট শুরু হচ্ছে...
✅ সব হ্যান্ডলার যুক্ত করা হয়েছে
```

### ধাপ ৮: অ্যাপ অ্যাক্সেস করা

- Flask: `http://localhost:5000`
- Telegram বট: `@Studycompetition_for_finallapbot`

---

## 📤 Railway এ Deploy করা

### ধাপ ১: GitHub রিপোজিটরি সেটআপ করা

```bash
# GitHub এ নতুন রিপোজিটরি তৈরি করুন
# https://github.com/new

# লোকাল রিপোজিটরি যুক্ত করুন
git remote add origin https://github.com/yourusername/study-wars.git
git branch -M main
git push -u origin main
```

### ধাপ ২: Railway Account এ Log In করা

1. [railway.app](https://railway.app) এ যান
2. GitHub দিয়ে সাইন আপ করুন
3. ড্যাশবোর্ডে যান

### ধাপ ৩: নতুন প্রজেক্ট তৈরি করা

1. "+ New Project" বাটনে ক্লিক করুন
2. "Deploy from GitHub" নির্বাচন করুন
3. আপনার `study-wars` রিপোজিটরি নির্বাচন করুন
4. Deploy করুন

### ধাপ ৪: Environment Variables সেট করা

Railway ড্যাশবোর্ডে:

1. Project খুলুন
2. Settings → Variables সেকশনে যান
3. নিম্নলিখিত ভেরিয়েবল যোগ করুন:

| ভেরিয়েবল | মান |
|-----------|-----|
| `BOT_TOKEN` | আপনার Telegram বট টোকেন |
| `WEB_APP_URL` | `https://your-railway-app.railway.app` |
| `FLASK_ENV` | `production` |
| `ADMIN_KEY` | `your-secure-key` |

### ধাপ ৫: Domains সেট করা

1. Railway ড্যাশবোর্ডে প্রজেক্ট খুলুন
2. Settings → Networking এ যান
3. Public URL কপি করুন (যেমন: `https://study-wars-xxx.railway.app`)
4. এটি `WEB_APP_URL` environment variable এ পেস্ট করুন

### ধাপ ৬: বট কনফিগারেশন আপডেট করা

Railway টার্মিনালে:

```bash
# বট API সেট করুন (ওয়েবহুক ব্যবহার করতে)
curl -X POST "https://api.telegram.org/bot{BOT_TOKEN}/setWebhook" \
  -d "url=https://your-railway-app.railway.app/webhook"

# বট কমান্ড সেট করুন
curl -X POST "https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      {"command": "start", "description": "শুরু করুন"},
      {"command": "help", "description": "সাহায্য পান"},
      {"command": "status", "description": "স্ট্যাটাস দেখুন"},
      {"command": "leaderboard", "description": "লিডারবোর্ড দেখুন"}
    ]
  }'
```

### ধাপ ৭: Deployment যাচাই করা

1. Railway লগে Deploy সম্পন্ন দেখুন
2. Telegram বটে `/start` পাঠান
3. লিংক ওপেন করুন এবং কাজ করছে কিনা দেখুন

---

## 📤 Render এ Deploy করা

### ধাপ ১: Render Account তৈরি করা

1. [render.com](https://render.com) এ যান
2. সাইন আপ করুন (GitHub দিয়ে সুবিধাজনক)

### ধাপ ২: নতুন Web Service তৈরি করা

1. Dashboard এ "New+" বাটন ক্লিক করুন
2. "Web Service" নির্বাচন করুন
3. GitHub রিপোজিটরি সংযোগ করুন

### ধাপ ৩: সার্ভিস কনফিগারেশন

| সেটিং | মান |
|-------|-----|
| **Name** | `study-wars` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --workers 1 --worker-class sync app:app` |

### ধাপ ৪: Environment Variables যোগ করা

Settings → Environment ট্যাবে:

```
BOT_TOKEN=your_token
WEB_APP_URL=https://study-wars-xxx.onrender.com
FLASK_ENV=production
ADMIN_KEY=secure_key
```

### ধাপ ৫: Deploy করা

1. "Create Web Service" বাটন ক্লিক করুন
2. Render Deploy সম্পন্ন হওয়ার অপেক্ষা করুন
3. Public URL পান (যেমন: `https://study-wars-xxx.onrender.com`)

### ধাপ ৬: বট ওয়েবহুক সেটআপ (Optional)

```bash
curl -X POST "https://api.telegram.org/bot{BOT_TOKEN}/setWebhook" \
  -d "url=https://your-render-app.onrender.com/webhook"
```

---

## 🔐 পরিবেশ ভেরিয়েবল

### প্রয়োজনীয় ভেরিয়েবল

| ভেরিয়েবল | বর্ণনা | উদাহরণ |
|----------|--------|--------|
| `BOT_TOKEN` | Telegram বট টোকেন (BotFather থেকে) | `8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ` |
| `WEB_APP_URL` | মিনি অ্যাপ ইউআরএল | `https://study-wars-xxx.railway.app` |

### Optional ভেরিয়েবল

| ভেরিয়েবল | বর্ণনা | Default |
|----------|--------|---------|
| `PORT` | সার্ভার পোর্ট | `5000` |
| `FLASK_ENV` | Flask পরিবেশ | `production` |
| `ADMIN_KEY` | অ্যাডমিন কী | `admin123` |
| `DATA_DIR` | ডেটা ডিরেক্টরি | `./data` |

---

## 🔌 API ডকুমেন্টেশন

### স্বাস্থ্য চেক
```
GET /api/health
Response: {"status": "ok", "message": "Server is running ✅"}
```

### ব্যবহারকারী নিবন্ধন
```
POST /api/register
Body: {
  "user_id": "123456789",
  "name": "নাম",
  "team": "Alpha"
}
```

### পড়া ঘণ্টা আপডেট
```
POST /api/update_hours
Body: {
  "user_id": "123456789",
  "hours": 2.5
}
```

### ব্যবহারকারী তথ্য পাওয়া
```
GET /api/get_user/<user_id>
Response: {
  "name": "...",
  "study_hours": 10.5,
  "rank": 1,
  "level": 2,
  ...
}
```

### লিডারবোর্ড পাওয়া
```
GET /api/leaderboard
Response: {
  "leaderboard": [
    {"rank": 1, "name": "...", "study_hours": 100, ...},
    ...
  ]
}
```

### টিম পরিসংখ্যান পাওয়া
```
GET /api/team_stats
Response: {
  "teams": [
    {"rank": 1, "name": "Alpha", "total_hours": 500, ...},
    ...
  ]
}
```

---

## 🐛 সমস্যা সমাধান

### সমস্যা ১: "BOT_TOKEN environment variable not set!"

**সমাধান:**
```bash
# .env ফাইল সৃষ্টি করুন
cp .env.example .env

# এবং এতে BOT_TOKEN যোগ করুন
```

### সমস্যা ২: "WEB_APP_URL environment variable not set!"

**সমাধান:**
- Railway/Render থেকে আপনার public URL পান
- `.env` এ `WEB_APP_URL` সেট করুন
- পুনরায় deploy করুন

### সমস্যা ৩: Local এ Flask সার্ভার কাজ করছে না

**সমাধান:**
```bash
# পোর্ট চেক করুন
lsof -i :5000

# Kill করে আবার চালু করুন
python app.py
```

### সমস্যা ৪: বট কমান্ড রেসপন্ড করছে না

**সমাধান:**
```bash
# বট টোকেন সঠিক কিনা চেক করুন
curl https://api.telegram.org/bot{BOT_TOKEN}/getMe

# বট আপনাকে follow করছে কিনা চেক করুন
```

### সমস্যা ৫: Mini App লোড হচ্ছে না

**সমাধান:**
- ব্রাউজার কনসোল এ error দেখুন (F12)
- `WEB_APP_URL` সঠিক কিনা যাচাই করুন
- CORS সমস্যা থাকলে Flask logs চেক করুন

---

## 📚 ফোল্ডার স্ট্রাকচার

```
study-wars/
├── app.py                 # Flask ওয়েব সার্ভার
├── bot.py               # Telegram বট
├── templates/
│   └── index_main.html  # মিনি অ্যাপ ফ্রন্টএন্ড
├── data/                # JSON ডেটা ফাইল (auto created)
│   ├── users_data.json
│   ├── history.json
│   ├── active_matches.json
│   └── announcement.json
├── requirements.txt     # Python dependencies
├── Procfile            # Railway/Render configuration
├── runtime.txt         # Python version
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # এই ফাইল
```

---

## 🔄 Deployment আপডেট করা

### GitHub এ পুশ করা

```bash
# পরিবর্তন সংরক্ষণ করুন
git add .
git commit -m "Feature: নতুন ফিচার যোগ করা"

# GitHub এ পুশ করুন
git push origin main
```

### Railway/Render এ Redeploy হবে

স্বয়ংক্রিয়ভাবে! GitHub এ push করলেই নতুন deployment শুরু হয়।

---

## 💡 টিপস এবং কৌশল

### ১. Data Persistence
JSON ফাইল ব্যবহার করা সহজ কিন্তু production এ MongoDB/PostgreSQL ব্যবহার করুন।

### ২. Monitoring
Railway/Render ড্যাশবোর্ডে লগ চেক করুন troubleshooting এর জন্য।

### ৩. Security
- `ADMIN_KEY` সুরক্ষিত রাখুন
- Production এ SSL/HTTPS ব্যবহার করুন
- Sensitive ডেটা `.env` এ রাখুন

### ৪. Performance
- Caching যুক্ত করুন (Redis)
- Database queries optimize করুন
- CDN ব্যবহার করুন স্ট্যাটিক ফাইলের জন্য

---

## 📞 সাহায্য এবং সমর্থন

### জ্ঞাত সমস্যা

| সমস্যা | সমাধান |
|--------|--------|
| Mini App HTTPS ছাড়া কাজ করে না | Telegram শুধু HTTPS URLs সাপোর্ট করে |
| Local IP কাজ করছে না | Railway/Render URL ব্যবহার করুন |
| Data হারিয়ে যাচ্ছে | JSON files persistent folder এ রাখুন |

---

## 📝 লাইসেন্স

এই প্রজেক্ট MIT লাইসেন্সের অধীন।

---

## 🙏 অবদানকারী

এই প্রজেক্টে অবদান রাখতে:

1. Fork করুন
2. Feature branch তৈরি করুন (`git checkout -b feature/AmazingFeature`)
3. Commit করুন (`git commit -m 'Add AmazingFeature'`)
4. Push করুন (`git push origin feature/AmazingFeature`)
5. Pull Request খুলুন

---

## ❓ FAQ

**Q: কী আমি এটি production এ ব্যবহার করতে পারি?**
A: হাঁ! এটি production-ready।

**Q: Railway/Render free?**
A: Railway এবং Render উভয়ই free tier অফার করে।

**Q: ডেটাবেস হিসেবে কী ব্যবহার করছি?**
A: JSON files, কিন্তু MongoDB/PostgreSQL এ migrate করতে পারেন।

**Q: কী offline mode সাপোর্ট করে?**
A: HTML localStorage ব্যবহার করে, কিন্তু sync করা দরকার।

---

**Happy Coding! 🚀**
