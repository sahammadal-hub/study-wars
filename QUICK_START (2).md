# 📖 Study Wars - Quick Start Guide

**সম্পূর্ণ সেটআপ শুরু থেকে শেষ পর্যন্ত**

---

## 🎯 আপনার লক্ষ্য

✅ **Study Wars মিনি অ্যাপ Railway এ Live করা**
✅ **সবাই Telegram এর মাধ্যমে access করতে পারবে**
✅ **24/7 Online থাকবে**

---

## 📋 আপনার কাছে থাকবে

```
study-wars/
├── app.py                      (Flask backend)
├── bot.py                      (Telegram Bot)
├── templates/index_main.html   (Mini App)
├── requirements.txt            (Dependencies)
├── Procfile                    (Railway config)
├── runtime.txt                 (Python version)
├── .env.example               (Variables template)
├── .gitignore                 (Git ignore)
├── README.md                  (সম্পূর্ণ ডকুমেন্টেশন)
└── RAILWAY_DEPLOYMENT.md      (Railway গাইড)
```

**✅ সব ফাইল ইতিমধ্যে প্রস্তুত!**

---

## 🚀 দ্রুত স্টার্ট (5 ধাপে)

### ধাপ ১️⃣ : ডাউনলোড করুন

```bash
# সব ফাইল ডাউনলোড করুন (outputs folder থেকে)
# একটি নতুন folder তৈরি করুন: C:\Study-Wars (Windows)
# বা ~/Study-Wars (Mac/Linux)
```

### ধাপ २⃣ : GitHub এ রাখুন

```bash
cd Study-Wars
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/study-wars.git
git push -u origin main
```

### ধাপ ३⃣ : Railway এ Deploy করুন

1. https://railway.app এ যান
2. "New Project → Deploy from GitHub" এ ক্লিক করুন
3. `study-wars` repository নির্বাচন করুন
4. Deploy বাটন ক্লিক করুন

### ধাপ ४⃣ : Environment Variables সেট করুন

Railway Dashboard এ:

```
BOT_TOKEN = 8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ
WEB_APP_URL = https://study-wars-xxx.up.railway.app (Railway দেবে)
FLASK_ENV = production
ADMIN_KEY = admin123
```

### ধাপ ५⃣ : বট টেস্ট করুন

```
Telegram বটে যান: https://t.me/your_bot
/start লিখুন
বাটনে ক্লিক করুন → Game শুরু! 🎮
```

---

## 📚 বিস্তারিত গাইড

### নতুনদের জন্য

যদি GitHub/Railway নতুন হন:
- **📖 README.md পড়ুন** (সম্পূর্ণ ডকুমেন্টেশন)
- **📱 RAILWAY_DEPLOYMENT.md পড়ুন** (ধাপে ধাপে Railway গাইড)

### অভিজ্ঞদের জন্য

- `app.py` - Flask API
- `bot.py` - Telegram Bot
- `templates/index_main.html` - Mini App UI

---

## 🔐 গুরুত্বপূর্ণ

### ⚠️ এটি কখনো শেয়ার করবেন না

```
BOT_TOKEN = 8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ
```

যদি শেয়ার হয়ে যায়:
1. BotFather এ যান
2. `/revoke_token` করুন
3. নতুন token পান

---

## 🎨 কাস্টমাইজ করা

### বট নাম বদলানো

`bot.py` এ:
```python
welcome_message = f"স্বাগতম {user.first_name}!"  # এটা বদলান
```

### টিম যোগ করা

`templates/index_main.html` এ:
```html
<option value="Alpha">Team Alpha 🔥</option>
<option value="Beta">Team Beta 💧</option>
<!-- নতুন টিম যোগ করুন -->
```

### রঙ বদলানো

`templates/index_main.html` এ:
```css
:root {
  --accent: #f0c040;  /* এই রঙ বদলান */
}
```

---

## 🧪 লোকালে টেস্ট করা (Optional)

```bash
# ১. Python install করুন (3.11+)
# ২. 
python -m venv venv
venv\Scripts\activate  (Windows)
source venv/bin/activate  (Mac/Linux)

# ३. Dependencies ইনস্টল করুন
pip install -r requirements.txt

# ४. .env তৈরি করুন (Terminal এ)
cp .env.example .env

# ५. Flask চালু করুন (একটি terminal)
python app.py

# ६. বট চালু করুন (নতুন terminal)
python bot.py

# ७. ব্রাউজারে যান
http://localhost:5000
```

---

## 📊 ফাইলের ভূমিকা

| ফাইল | কাজ | আপডেট করবেন? |
|------|------|---|
| `app.py` | Flask সার্ভার | শুধু নতুন ফিচার চাইলে |
| `bot.py` | Telegram বট | শুধু বার্তা বদলাতে |
| `index_main.html` | মিনি অ্যাপ UI | ডিজাইন পরিবর্তন করতে |
| `requirements.txt` | Dependencies | নতুন লাইব্রেরি যোগ করতে |
| `Procfile` | Railway config | সাধারণত ছাড়াই কাজ করে |
| `runtime.txt` | Python version | আপডেট রাখতে |
| `.env.example` | Variables template | সবাই দেখতে পারে |
| `README.md` | ডকুমেন্টেশন | উন্নত ব্যবহারকারীদের জন্য |

---

## 🔄 আপডেট করা

```bash
# কোড এডিট করুন
vim app.py

# GitHub এ পুশ করুন
git add .
git commit -m "Updated: নতুন ফিচার"
git push origin main

# Railway স্বয়ংক্রিয়ভাবে redeploy করবে ✅
```

---

## ⚙️ API Endpoints (Advanced)

```
GET  /api/health              - সার্ভার চেক করা
POST /api/register            - নতুন ইউজার
POST /api/update_hours        - পড়া ঘণ্টা আপডেট
GET  /api/get_user/:id        - ইউজার তথ্য
GET  /api/leaderboard         - টপ ১০০ ইউজার
GET  /api/team_stats          - টিম পরিসংখ্যান
GET  /api/announcement        - ঘোষণা
POST /api/announcement        - নতুন ঘোষণা
```

---

## 🐛 Common Issues

| সমস্যা | সমাধান |
|--------|--------|
| ❌ "BOT_TOKEN not set" | `.env` তৈরি করুন, টোকেন পেস্ট করুন |
| ❌ Mini App লোড হচ্ছে না | `WEB_APP_URL` সঠিক কিনা চেক করুন |
| ❌ বট রেসপন্ড করছে না | Railway logs চেক করুন |
| ❌ ডেটা হারিয়ে যাচ্ছে | Railway Volumes সেট করুন |
| ❌ GitHub push fail | Token expire হয়েছে, re-login করুন |

---

## 📞 Help Resources

- **📖 README.md** - সম্পূর্ণ ডকুমেন্টেশন
- **🚀 RAILWAY_DEPLOYMENT.md** - Railway গাইড
- **💬 Telegram**: @BotFather - বট সাপোর্ট
- **📚 Docs**: railway.app/docs - Railway ডকুমেন্টেশন

---

## ✅ Checklist

Deploy করার আগে চেক করুন:

- [ ] সব ফাইল ডাউনলোড করেছেন
- [ ] GitHub repository তৈরি করেছেন
- [ ] Telegram bot token পেয়েছেন
- [ ] Railway account তৈরি করেছেন
- [ ] GitHub দিয়ে Railway এ login করেছেন
- [ ] Repository deploy করেছেন
- [ ] BOT_TOKEN environment variable সেট করেছেন
- [ ] WEB_APP_URL environment variable সেট করেছেন
- [ ] Railway redeploy হয়েছে
- [ ] Telegram বটে /start টেস্ট করেছেন
- [ ] Mini App লোড হয়েছে

---

## 🎉 Success!

যখন সব কাজ করবে, দেখবেন:

✅ Telegram বটে `/start` রেসপন্ড করে
✅ Mini App খোলে এবং সুন্দর দেখায়
✅ ইউজার রেজিস্টার করতে পারে
✅ পড়া ঘণ্টা যোগ করতে পারে
✅ লিডারবোর্ড দেখা যায়

**তখন আপনি প্রস্তুত!** 🚀

---

## 🌟 পরবর্তী পদক্ষেপ

### ১. বন্ধুদের জন্য শেয়ার করুন
```
https://t.me/your_bot_username
```

### २. নতুন ফিচার যোগ করুন
- লেভেল সিস্টেম উন্নত করা
- ডেটাবেস যোগ করা (MongoDB)
- নোটিফিকেশন যোগ করা
- সোশ্যাল ফিচার যোগ করা

### ३. Production optimize করুন
- Caching যোগ করা
- Rate limiting যোগ করা
- Error monitoring যোগ করা

---

## 💡 চূড়ান্ত টিপস

1. **নিয়মিত আপডেট করুন** - নতুন dependencies আছে কিনা চেক করুন
2. **ডেটা ব্যাকআপ নিন** - JSON files বড় হলে database এ migrate করুন
3. **লগ চেক করুন** - কোন সমস্যা হলে Railway logs দেখুন
4. **কমিউনিটি তৈরি করুন** - বন্ধুদের invite করুন

---

## 📧 ফিডব্যাক দিন

এই গাইড কেমন লেগেছে? উন্নতির জন্য সাজেশন দিন! 💬

---

**Happy Gaming! ⚔️**

*Study Wars - বন্ধুদের সাথে পড়ার যুদ্ধ*
