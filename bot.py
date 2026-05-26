"""
Study Wars - টেলিগ্রাম বট
Environment variables থেকে কনফিগুরেশন পায়
Railway/Render এ চলার জন্য প্রস্তুত
"""

import logging
import asyncio
import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.error import TelegramError

# লগিং সেটআপ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════
# কনফিগুরেশন - Environment variables থেকে
# ═══════════════════════════════════════════════════════════════════════════

# টেলিগ্রাম বট টোকেন
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable not set!")

# মিনি অ্যাপ URL
WEB_APP_URL = os.getenv('WEB_APP_URL')
if not WEB_APP_URL:
    raise ValueError("❌ WEB_APP_URL environment variable not set!")

logger.info(f"🚀 Bot starting with token: {BOT_TOKEN[:10]}...")
logger.info(f"📱 Mini App URL: {WEB_APP_URL}")

# ═══════════════════════════════════════════════════════════════════════════
# কমান্ড হ্যান্ডেলার
# ═══════════════════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start কমান্ড হ্যান্ডলার
    মিনি অ্যাপ খোলার বাটন সহ স্বাগত বার্তা দেখায়
    """
    try:
        user = update.effective_user
        logger.info(f"✅ /start command from {user.first_name} (ID: {user.id})")
        
        # মিনি অ্যাপ খোলার বাটন
        keyboard = [
            [InlineKeyboardButton(
                "⚔️ Study Wars শুরু করো",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )],
            [
                InlineKeyboardButton("📊 লিডারবোর্ড", callback_data="leaderboard"),
                InlineKeyboardButton("ℹ️ সাহায্য", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = f"""
🎉 স্বাগতম {user.first_name}!

আপনি *Study Wars* এ এসেছেন! 🚀

এখানে আপনি:
✅ বন্ধুদের সাথে পড়াশোনা প্রতিযোগিতা করতে পারবেন
⏰ দৈনিক পড়ার সময় ট্র্যাক করতে পারবেন
🏆 লিডারবোর্ডে ওঠতে পারবেন
🎁 ব্যাজ এবং পুরস্কার জিততে পারবেন
👥 টিমে যোগ দিয়ে কমিউনিটি তৈরি করতে পারবেন

নিচের বাটনে ক্লিক করে শুরু করুন! 👇
        """
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    except TelegramError as e:
        logger.error(f"❌ Telegram Error in /start: {e}")
        await update.message.reply_text("⚠️ কিছু সমস্যা হয়েছে। আবার চেষ্টা করুন।")
    except Exception as e:
        logger.error(f"❌ Unexpected error in /start: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help কমান্ড - সাহায্য দেখাও
    """
    try:
        help_text = """
⚔️ *Study Wars কমান্ড:*

/start - অ্যাপ শুরু করুন
/help - এই মেসেজ দেখুন
/status - আপনার স্ট্যাটাস চেক করুন
/leaderboard - লিডারবোর্ড দেখুন

*কীভাবে ব্যবহার করবেন:*

1️⃣ /start দিয়ে শুরু করুন
2️⃣ আপনার নাম এবং টিম নির্বাচন করুন
3️⃣ প্রতিদিন পড়ার সময় লগ করুন
4️⃣ লিডারবোর্ডে ওঠার চেষ্টা করুন

📱 নিচের বাটনে ক্লিক করে অ্যাপ খুলুন
        """
        
        keyboard = [[InlineKeyboardButton(
            "⚔️ খেলতে শুরু করো",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]]
        
        await update.message.reply_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"❌ Error in /help: {e}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /status কমান্ড - স্ট্যাটাস দেখাও
    """
    try:
        user = update.effective_user
        status_message = f"""
✅ *বট সফলভাবে চলছে!*

👤 *আপনার তথ্য:*
• নাম: {user.first_name}
• ID: `{user.id}`
• ব্যবহারকারী নাম: @{user.username or 'Not set'}

📱 অ্যাপ খোলতে নিচের বাটনে ক্লিক করুন
        """
        
        keyboard = [[InlineKeyboardButton(
            "⚔️ খেলতে যান",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]]
        
        await update.message.reply_text(
            status_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"❌ Error in /status: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    বাটন ক্লিক হ্যান্ডলার
    """
    try:
        query = update.callback_query
        await query.answer()
        
        if query.data == "leaderboard":
            leaderboard_text = """
🏆 *লিডারবোর্ড*

এই অ্যাপে সর্বোচ্চ পড়ুয়া:

(লাইভ ডেটা দেখতে অ্যাপ খুলুন)

অ্যাপে যাওয়ার জন্য নিচের বাটনে ক্লিক করুন 👇
            """
            
            keyboard = [[InlineKeyboardButton(
                "⚔️ অ্যাপ খুলুন",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )]]
            
            await query.edit_message_text(
                leaderboard_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif query.data == "help":
            await help_command(update, context)
    
    except Exception as e:
        logger.error(f"❌ Error in button handler: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    এরর হ্যান্ডলার - সবকিছু লগ করো
    """
    logger.error(
        msg="Exception while handling an update:",
        exc_info=context.error
    )

# ═══════════════════════════════════════════════════════════════════════════
# মেইন ফাংশন - বট চালু করা
# ═══════════════════════════════════════════════════════════════════════════

async def main():
    """
    বট শুরু করা এবং চলমান রাখা
    """
    try:
        logger.info("🤖 Study Wars বট শুরু হচ্ছে...")
        
        # অ্যাপ্লিকেশন তৈরি করা
        app = Application.builder().token(BOT_TOKEN).build()
        
        # কমান্ড হ্যান্ডলার যোগ করা
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("status", status_command))
        
        # বাটন হ্যান্ডলার যোগ করা
        app.add_handler(CallbackQueryHandler(button_handler))
        
        # এরর হ্যান্ডলার যোগ করা
        app.add_error_handler(error_handler)
        
        logger.info("✅ সব হ্যান্ডলার যুক্ত করা হয়েছে")
        logger.info("📍 @Studycompetition_for_finallapbot এ /start লিখুন")
        logger.info("⏳ বট polling শুরু করছে...\n")
        
        # বট শুরু করা
        await app.initialize()
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
        # চিরকাল চলতে থাকুক
        await asyncio.Event().wait()
    
    except Exception as e:
        logger.error(f"❌ Critical error in main: {e}")
        raise

# ═══════════════════════════════════════════════════════════════════════════
# প্রোগ্রাম এন্ট্রি পয়েন্ট
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 বট বন্ধ হয়েছে")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
