from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import json, random, os, hashlib
from datetime import datetime

DATA_FILE = "study_data.json"
USERS_FILE = "users.json"
ADMIN_IDS = [5726202509]

def load_users():
    return json.load(open(USERS_FILE)) if os.path.exists(USERS_FILE) else {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def load_data():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    users = load_users()
    names = list(users.values())
    return {
        "today": str(datetime.now().date()),
        "matches": {},
        "scores": {n: 0 for n in names},
        "wins": {n: 0 for n in names}
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_referral_code(user_id):
    """Generate unique referral code"""
    return hashlib.md5(str(user_id).encode()).hexdigest()[:8].upper()

def generate_matches(names):
    if len(names) < 2:
        return {}
    shuffled = names.copy()
    random.shuffle(shuffled)
    matches = {}
    for i in range(0, len(shuffled)-1, 2):
        matches[f"m{i//2+1}"] = {"p1": shuffled[i], "p2": shuffled[i+1], "p1_time": 0.0, "p2_time": 0.0}
    return matches

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    uid = str(update.message.from_user.id)
    
    if uid not in users:
        kb = [[InlineKeyboardButton("✍️ নাম রেজিস্টার করো", callback_data="reg")]]
        await update.message.reply_text("🎯 *স্টাডি ওয়ার্স*\n\nপ্রথমে নাম রেজিস্টার করো!", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
    else:
        user = users[uid]
        name = user.get('name', 'তুমি')
        xp = user.get('xp', 0)
        
        kb = [
            [InlineKeyboardButton("📝 সময়", callback_data="log"), InlineKeyboardButton("🏆 ম্যাচ", callback_data="m")],
            [InlineKeyboardButton("📊 বোর্ড", callback_data="b"), InlineKeyboardButton("⚡ XP", callback_data="xp")],
            [InlineKeyboardButton("🔗 Refer করো", callback_data="refer_menu"), InlineKeyboardButton("⚔️ Daily War", callback_data="dw_menu")]
        ]
        await update.message.reply_text(
            f"🎯 *স্বাগতম, {name}!*\n\n⚡ XP: {xp}pts",
            reply_markup=InlineKeyboardMarkup(kb), 
            parse_mode=ParseMode.MARKDOWN
        )

# ════════════════════════════════════════════════════════════════
# REFER SYSTEM
# ════════════════════════════════════════════════════════════════

async def refer_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Refer menu - show link and stats"""
    query = update.callback_query
    await query.answer()
    
    users = load_users()
    uid = str(query.from_user.id)
    
    if uid not in users:
        await query.edit_message_text("❌ আগে register করো!")
        return
    
    user = users[uid]
    
    # Generate referral code if not exists
    if 'referral_code' not in user:
        user['referral_code'] = generate_referral_code(uid)
        user['referred_count'] = 0
        user['xp'] = user.get('xp', 0)
        save_users(users)
    
    code = user['referral_code']
    ref_count = user.get('referred_count', 0)
    xp_from_ref = ref_count * 100  # প্রতি refer-এ 100 XP
    
    # Telegram bot username দাও (change এটা)
    bot_username = "study_wars_bot"  # আপনার bot username
    refer_link = f"https://t.me/{bot_username}?start=ref_{code}"
    
    text = (
        f"🔗 *তোমার Refer Link*\n\n"
        f"`{refer_link}`\n\n"
        f"📋 *যা হবে:*\n"
        f"✅ যে join করবে: +50 XP\n"
        f"✅ তুমি পাবে: +100 XP ⚡\n\n"
        f"📊 *তোমার স্ট্যাটস:*\n"
        f"👥 Referred: {ref_count} জন\n"
        f"⚡ Ref XP: {xp_from_ref}pts\n\n"
        f"_Link copy করে বন্ধুদের পাঠাও!_"
    )
    
    kb = [
        [InlineKeyboardButton("📋 Link Copy করো", callback_data="copy_link")],
        [InlineKeyboardButton("◀️ Back", callback_data="back_menu")]
    ]
    
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))

async def start_with_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start with referral code"""
    users = load_users()
    uid = str(update.message.from_user.id)
    
    # Check for referral in start args
    if context.args and context.args[0].startswith('ref_'):
        ref_code = context.args[0].replace('ref_', '')
        
        # Find referrer
        referrer_id = None
        for uid_check, user_check in users.items():
            if user_check.get('referral_code') == ref_code and uid_check != uid:
                referrer_id = uid_check
                break
        
        if referrer_id and uid in users and not users[uid].get('used_referral'):
            # Apply referral bonus
            users[referrer_id]['xp'] = users[referrer_id].get('xp', 0) + 100
            users[referrer_id]['referred_count'] = users[referrer_id].get('referred_count', 0) + 1
            
            users[uid]['xp'] = users[uid].get('xp', 0) + 50
            users[uid]['used_referral'] = True
            users[uid]['referred_by'] = referrer_id
            
            save_users(users)
            
            referrer_name = users[referrer_id].get('name', 'বন্ধু')
            
            await update.message.reply_text(
                f"🎉 *Referral Success!*\n\n"
                f"✅ {referrer_name}-এর link দিয়ে join করেছ!\n"
                f"⚡ তুমি পেয়েছ: +50 XP\n"
                f"🎁 {referrer_name} পেয়েছে: +100 XP",
                parse_mode=ParseMode.MARKDOWN
            )
    
    # Normal start
    await start(update, context)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("নাম লিখ:")
    context.user_data['reg'] = True

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = load_users()
    names = list(users.values())
    if not names:
        await query.edit_message_text("❌ কোনো ইউজার নেই!")
        return
    kb = [[InlineKeyboardButton(users[n].get('name', n), callback_data=f"s_{n}")] for n in users.keys()]
    await query.edit_message_text("👤 কে?", reply_markup=InlineKeyboardMarkup(kb))

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.data.split("_")[1]
    users = load_users()
    name = users[uid].get('name', uid)
    context.user_data['friend'] = name
    context.user_data['friend_uid'] = uid
    await query.answer()
    kb = [[InlineKeyboardButton("0.5h", callback_data="t_0.5"), InlineKeyboardButton("1h", callback_data="t_1")], 
          [InlineKeyboardButton("2h", callback_data="t_2"), InlineKeyboardButton("3h", callback_data="t_3")],
          [InlineKeyboardButton("Custom", callback_data="t_c")]]
    await query.edit_message_text(f"⏱️ {name} - কত?", reply_markup=InlineKeyboardMarkup(kb))

async def add_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    val = query.data.split("_")[1]
    friend = context.user_data.get('friend')
    friend_uid = context.user_data.get('friend_uid')
    
    if val == 'c':
        await query.answer()
        await query.edit_message_text("সংখ্যা দাও (যেমন 1.5):")
        context.user_data['custom'] = True
        return
    
    hours = float(val)
    data = load_data()
    users = load_users()
    
    # Update match times
    for m in data['matches'].values():
        if friend == m['p1']:
            m['p1_time'] += hours
        elif friend == m['p2']:
            m['p2_time'] += hours
    
    # Update scores
    data['scores'][friend] = data['scores'].get(friend, 0) + hours
    
    # Update user total
    if friend_uid in users:
        users[friend_uid]['total'] = users[friend_uid].get('total', 0) + hours
    
    save_data(data)
    save_users(users)
    
    await query.answer()
    await query.edit_message_text(f"✅ {hours}h যোগ!")

async def view_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_data()
    text = "🏆 *আজকের ম্যাচ:*\n\n"
    for m in data['matches'].values():
        status = "⚔️"
        if m['p1_time'] > m['p2_time']:
            status = f"✅ {m['p1']}"
        elif m['p2_time'] > m['p1_time']:
            status = f"✅ {m['p2']}"
        text += f"{m['p1']}({m['p1_time']}h) vs {m['p2']}({m['p2_time']}h) - {status}\n"
    
    kb = [[InlineKeyboardButton("◀️ Back", callback_data="back_menu")]]
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = load_data()
    sorted_data = sorted(data['scores'].items(), key=lambda x: x[1], reverse=True)
    text = "📊 *লিডারবোর্ড:*\n\n"
    for i, (name, hours) in enumerate(sorted_data, 1):
        text += f"{i}. {name}: {hours}h\n"
    
    kb = [[InlineKeyboardButton("◀️ Back", callback_data="back_menu")]]
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))

async def show_xp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show XP stats"""
    query = update.callback_query
    await query.answer()
    
    users = load_users()
    uid = str(query.from_user.id)
    
    if uid not in users:
        await query.edit_message_text("❌ User not found!")
        return
    
    user = users[uid]
    xp = user.get('xp', 0)
    ref_count = user.get('referred_count', 0)
    used_ref = user.get('used_referral', False)
    
    text = (
        f"⚡ *তোমার XP*\n\n"
        f"Total XP: {xp}pts\n\n"
        f"📋 *কোথা থেকে পেয়েছ:*\n"
        f"✅ Refer করে: {ref_count * 100}pts\n"
        f"✅ Refer পেয়ে: {'50pts' if used_ref else 'পাওনি এখনো'}\n\n"
        f"_আরো refer করো আরো XP পাও!_"
    )
    
    kb = [[InlineKeyboardButton("◀️ Back", callback_data="back_menu")]]
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))

async def daily_war_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily War opt-in/out"""
    query = update.callback_query
    await query.answer()
    
    users = load_users()
    uid = str(query.from_user.id)
    
    if uid not in users:
        await query.edit_message_text("❌ আগে register করো!")
        return
    
    is_opted = users[uid].get('daily_war_opted', False)
    status = "✅ চালু আছে" if is_opted else "❌ বন্ধ আছে"
    
    kb = [
        [InlineKeyboardButton("⚔️ হ্যাঁ, যোগ দেবো!", callback_data="dw_yes"),
         InlineKeyboardButton("🚫 না, এখন না", callback_data="dw_no")],
        [InlineKeyboardButton("◀️ Back", callback_data="back_menu")]
    ]
    
    text = (
        f"⚔️ *Daily War*\n\n"
        f"প্রতিদিন auto-match হবে!\n"
        f"যে বেশি পড়বে সে জিতবে 🏆\n\n"
        f"বর্তমান status: {status}"
    )
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)

async def daily_war_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle daily war"""
    query = update.callback_query
    uid = str(query.from_user.id)
    opted = query.data == "dw_yes"
    
    users = load_users()
    users[uid]['daily_war_opted'] = opted
    save_users(users)
    
    await query.answer()
    
    text = (
        f"✅ *Daily War {'enabled' if opted else 'disabled'}!*"
        if opted 
        else "🚫 *Daily War disabled.*"
    )
    
    kb = [[InlineKeyboardButton("◀️ Back", callback_data="back_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)

async def back_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to main menu"""
    query = update.callback_query
    await query.answer()
    
    users = load_users()
    uid = str(query.from_user.id)
    
    if uid in users:
        user = users[uid]
        name = user.get('name', 'তুমি')
        xp = user.get('xp', 0)
        
        kb = [
            [InlineKeyboardButton("📝 সময়", callback_data="log"), InlineKeyboardButton("🏆 ম্যাচ", callback_data="m")],
            [InlineKeyboardButton("📊 বোর্ড", callback_data="b"), InlineKeyboardButton("⚡ XP", callback_data="xp")],
            [InlineKeyboardButton("🔗 Refer", callback_data="refer_menu"), InlineKeyboardButton("⚔️ Daily War", callback_data="dw_menu")]
        ]
        
        await query.edit_message_text(
            f"🎯 *স্বাগতম, {name}!*\n\n⚡ XP: {xp}pts",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode=ParseMode.MARKDOWN
        )

async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin announce"""
    if update.message.from_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Admin only")
        return
    
    data = load_data()
    users = load_users()
    
    text = "🎉 *আজকের বিজয়ী:*\n\n"
    for m in data['matches'].values():
        if m['p1_time'] > m['p2_time']:
            winner = m['p1']
            data['wins'][winner] = data['wins'].get(winner, 0) + 1
            text += f"👑 {winner}\n"
        elif m['p2_time'] > m['p1_time']:
            winner = m['p2']
            data['wins'][winner] = data['wins'].get(winner, 0) + 1
            text += f"👑 {winner}\n"
    
    data['today'] = str(datetime.now().date())
    data['matches'] = generate_matches(list(set([users[n].get('name', n) for n in users.keys()])))
    save_data(data)
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.message.from_user.id)
    
    if context.user_data.get('reg'):
        name = update.message.text.strip()
        users = load_users()
        users[uid] = {
            'name': name,
            'total': 0,
            'xp': 0,
            'referral_code': generate_referral_code(uid),
            'referred_count': 0,
            'daily_war_opted': False
        }
        save_users(users)
        context.user_data['reg'] = False
        
        kb = [[InlineKeyboardButton("📝 সময়", callback_data="log"), InlineKeyboardButton("🏆 ম্যাচ", callback_data="m")],
              [InlineKeyboardButton("🔗 Refer করো", callback_data="refer_menu")]]
        
        await update.message.reply_text(f"✅ স্বাগতম, {name}!", reply_markup=InlineKeyboardMarkup(kb))
    
    elif context.user_data.get('custom'):
        try:
            hours = float(update.message.text)
            friend = context.user_data.get('friend')
            friend_uid = context.user_data.get('friend_uid')
            
            data = load_data()
            users = load_users()
            
            for m in data['matches'].values():
                if friend == m['p1']:
                    m['p1_time'] += hours
                elif friend == m['p2']:
                    m['p2_time'] += hours
            
            data['scores'][friend] = data['scores'].get(friend, 0) + hours
            
            if friend_uid in users:
                users[friend_uid]['total'] = users[friend_uid].get('total', 0) + hours
            
            save_data(data)
            save_users(users)
            
            context.user_data['custom'] = False
            await update.message.reply_text(f"✅ {hours}h যোগ!")
        except:
            await update.message.reply_text("❌ সংখ্যা দাও")

def main():
    TOKEN = "8835845552:AAGNNGMSGdezJiRzNi3nSJEq1bn94rAIplQ"  # আপনার token
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start_with_referral))
    app.add_handler(CommandHandler("announce", announce))
    
    app.add_handler(CallbackQueryHandler(register, pattern="^reg$"))
    app.add_handler(CallbackQueryHandler(log, pattern="^log$"))
    app.add_handler(CallbackQueryHandler(select, pattern="^s_"))
    app.add_handler(CallbackQueryHandler(add_time, pattern="^t_"))
    app.add_handler(CallbackQueryHandler(view_matches, pattern="^m$"))
    app.add_handler(CallbackQueryHandler(leaderboard, pattern="^b$"))
    
    # Refer system
    app.add_handler(CallbackQueryHandler(refer_menu, pattern="^refer_menu$"))
    app.add_handler(CallbackQueryHandler(show_xp, pattern="^xp$"))
    
    # Daily War
    app.add_handler(CallbackQueryHandler(daily_war_menu, pattern="^dw_menu$"))
    app.add_handler(CallbackQueryHandler(daily_war_toggle, pattern="^dw_"))
    
    # Navigation
    app.add_handler(CallbackQueryHandler(back_menu, pattern="^back_menu$"))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("🚀 Study Wars Bot চালু হয়েছে!")
    print("🔗 Refer system: ✅ Active")
    print("⚡ XP System: ✅ Active")
    app.run_polling()

if __name__ == "__main__":
    main()
