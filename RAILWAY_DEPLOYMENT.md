# 🚀 Railway এ Deploy করার সম্পূর্ণ গাইড

**Study Wars Telegram Mini App**

---

## প্রিরিকুইজিট

- GitHub Account (Free: github.com)
- Railway Account (Free: railway.app)
- Telegram Bot Token (BotFather থেকে)

---

## ধাপ ১: GitHub Repository তৈরি করা

### ১.১ GitHub এ যান

```
https://github.com/new
```

### ১.২ Repository তৈরি করুন

| ফিল্ড | মান |
|------|-----|
| Repository name | `study-wars` |
| Description | Study Wars - Telegram Mini App |
| Public/Private | Public |
| Add .gitignore | ✅ (Python নির্বাচন করুন) |

**"Create repository" বাটনে ক্লিক করুন**

### ১.৩ Local ফোল্ডারে Repository সংযোগ করুন

```bash
# GitHub দেখাবে এই কমান্ডগুলি চালান

git init
git add README.md
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/study-wars.git
git push -u origin main
```

---

## ধাপ ২: সব ফাইল GitHub এ আপলোড করা

### ২.১ নিম্নলিখিত ফাইল তৈরি/কপি করুন

```
study-wars/
├── app.py                 ✅ (ইতিমধ্যে আছে)
├── bot.py                 ✅ (ইতিমধ্যে আছে)
├── templates/
│   └── index_main.html    ✅ (ইতিমধ্যে আছে)
├── requirements.txt       ✅ (ইতিমধ্যে আছে)
├── Procfile              ✅ (ইতিমধ্যে আছে)
├── runtime.txt           ✅ (ইতিমধ্যে আছে)
├── .env.example          ✅ (ইতিমধ্যে আছে)
├── .gitignore            ✅ (ইতিমধ্যে আছে)
└── README.md             ✅ (ইতিমধ্যে আছে)
```

### ২.२ GitHub এ Push করুন

```bash
git add .
git commit -m "Study Wars - Production Ready Setup"
git push origin main
```

**GitHub এ সব ফাইল দেখুন:** `https://github.com/yourusername/study-wars`

---

## ধাপ ३: Telegram Bot টোকেন পাওয়া

### ३.১ BotFather খোলুন

```
https://t.me/BotFather
```

### ३.२ নতুন বট তৈরি করুন (যদি না থাকে)

```
/newbot

Name: Study Wars Bot
Username: studywarsgame_bot (অনন্য হতে হবে)
```

### ३.३ Bot Token কপি করুন

BotFather এটি দেবে:
```
8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ
```

**এটি সংরক্ষণ করুন! ⭐**

---

## ধাপ ४: Railway Account সেটআপ করা

### ४.१ Railway এ যান

```
https://railway.app
```

### ४.२ Sign Up করুন

- "Sign up with GitHub" বাটনে ক্লিক করুন
- GitHub authorization দিন
- Railway ড্যাশবোর্ডে আসবেন

---

## ধাপ ५: Railway এ প্রজেক্ট তৈরি করা

### ५.१ নতুন প্রজেক্ট তৌরি করুন

Railway ড্যাশবোর্ডে:
```
New Project → Deploy from GitHub
```

### ५.२ GitHub Repository সংযোগ করুন

1. "Connect GitHub Account" এ ক্লিক করুন
2. GitHub authorization দিন
3. আপনার `study-wars` রিপোজিটরি খুঁজুন এবং নির্বাচন করুন
4. "Deploy" বাটনে ক্লিক করুন

**ধাপ ৫-১০ মিনিট সময় লাগতে পারে**

---

## ধাপ ६: Environment Variables সেট করা

### ६.१ Railway ড্যাশবোর্ডে যান

```
Your Project → Variables সেকশন
```

### ६.२ নিম্নলিখিত ভেরিয়েবল যোগ করুন

#### BOT_TOKEN যোগ করুন

```
Key:   BOT_TOKEN
Value: 8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ
```

#### WEB_APP_URL যোগ করুন (পরে করব)

এখন ছেড়ে দিন, Railway deploy করার পরে URL পাবেন

#### অন্যান্য ভেরিয়েবল

```
Key:   FLASK_ENV
Value: production

Key:   ADMIN_KEY
Value: admin123
```

**Save এ ক্লিক করুন**

---

## ধাপ ७: Public URL পাওয়া

### ७.१ Railway ড্যাশবোর্ডে যান

```
Your Project → Networking সেকশন
```

### ७.२ Public URL কপি করুন

উদাহরণস্বরূপ:
```
https://study-wars-production-xxx.up.railway.app
```

### ७.३ এটি WEB_APP_URL হিসেবে সেট করুন

1. Variables সেকশনে ফিরুন
2. WEB_APP_URL যোগ করুন:

```
Key:   WEB_APP_URL
Value: https://study-wars-production-xxx.up.railway.app
```

**Save এ ক্লিক করুন → Railway Redeploy হবে**

---

## ধাপ ८: বট কমান্ড সেট করা (Optional কিন্তু সুবিধাজনক)

### ८.१ Railway Terminal খুলুন

```
Your Project → Deployments → Terminal
```

### ८.२ নিম্নলিখিত কমান্ড চালান

```bash
# বট কমান্ড সেট করুন
curl -X POST "https://api.telegram.org/bot8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      {"command": "start", "description": "শুরু করুন এবং খেলুন"},
      {"command": "help", "description": "সাহায্য পান"},
      {"command": "status", "description": "আপনার স্ট্যাটাস দেখুন"},
      {"command": "leaderboard", "description": "লিডারবোর্ড দেখুন"}
    ]
  }'
```

---

## ধাপ ९: Deployment যাচাই করা

### ९.१ Railway Logs চেক করুন

```
Your Project → Deployments → Latest → Logs
```

এটি দেখুন:
```
✅ সব হ্যান্ডলার যুক্ত করা হয়েছে
📍 বট polling শুরু করছে
```

### ९.२ Web সার্ভার চেক করুন

ব্রাউজারে যান:
```
https://study-wars-production-xxx.up.railway.app
```

এটি দেখুন:
```
Study Wars Home Page
```

---

## ধাপ १०: Telegram বটে টেস্ট করুন

### १०.१ বট খুলুন

```
https://t.me/your_bot_username
```

উদাহরণ:
```
https://t.me/studywarsgame_bot
```

### १०.२ /start লাইখুন

```
/start
```

**ফলাফল দেখুন:**

```
🎉 স্বাগতম!

আপনি Study Wars এ এসেছেন! 🚀

⚔️ Study Wars শুরু করো
[বাটনটি দেখুন]
```

### १०.३ বাটনে ক্লিক করুন

Mini App খুলবে এবং গেম শুরু করতে পারবেন! 🎮

---

## ✅ সাফল্যের লক্ষণ

যদি এটি কাজ করছে:

✅ বট `/start` এ রেসপন্ড করে
✅ Mini App লোড হয়
✅ ইউজার রেজিস্টার করতে পারে
✅ পড়া ঘণ্টা লগ করতে পারে
✅ লিডারবোর্ড দেখা যায়

---

## 🔄 আপডেট করা

কোড আপডেট করতে:

```bash
# লোকালে কোড এডিট করুন
vim app.py

# GitHub এ Push করুন
git add .
git commit -m "Bug fix: সমস্যা সমাধান"
git push origin main

# Railway স্বয়ংক্রিয়ভাবে redeploy করবে
```

---

## ❌ সমস্যা সমাধান

### সমস্যা: বট কাজ করছে না

**সমাধান:**
1. Railway Logs চেক করুন
2. BOT_TOKEN সঠিক কিনা যাচাই করুন
3. Project redeploy করুন

### সমস্যা: Mini App লোড হচ্ছে না

**সমাধান:**
1. WEB_APP_URL সঠিক কিনা চেক করুন
2. Railway Public URL পান এবং আপডেট করুন
3. ব্রাউজার এ direct URL চেষ্টা করুন

### সমস্যা: ডেটা হারিয়ে যাচ্ছে

**সমাধান:**
Railway ড্যাশবোর্ডে Volumes সেট করুন:
1. Project Settings → Volumes
2. `/app/data` মাউন্ট করুন

---

## 📊 উন্নত বৈশিষ্ট্য (Optional)

### ডাটাবেস যোগ করা

Railway এ PostgreSQL যোগ করুন:

```
Project → Add Service → PostgreSQL
```

তারপর `app.py` আপডেট করুন JSON এর পরিবর্তে।

### Monitoring সেটআপ করা

```
Project → Settings → Monitoring
```

---

## 📞 সাহায্য প্রয়োজন?

1. **Railway Docs:** https://docs.railway.app
2. **Telegram Bot API:** https://core.telegram.org/bots/api
3. **GitHub Issues:** আপনার repository এ issue করুন

---

## 🎉 Congratulations!

আপনার **Study Wars** মিনি অ্যাপ এখন **Live** এবং **24/7** চলছে! 🚀

সবাই এটি access করতে পারে:
```
https://t.me/your_bot_username
```

---

**Happy Deploying! ⚔️**
