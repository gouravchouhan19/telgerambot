from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import time
from server import keep_alive

# Bot Token
BOT_TOKEN = "7751903987:AAGZiLgA5-qZz1hpM05O-BlR9Qrb1jsv1sk"

# Bot username & name
BOT_USERNAME = "@FREETEMPNUMBEERR_BOT"
BOT_NAME = "𝗧𝗘𝗠𝗣 𝗡𝗨𝗠𝗕𝗘𝗥 𝗕𝗢𝗧"

# Dictionaries for invites & referrals
user_invites = {}
referrals = {}

# -------------------- START COMMAND --------------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    name = user.first_name
    user_id = user.id

    # Referral check
    args = context.args
    if args:
        ref_id = int(args[0])
        if ref_id != user_id:  # self-referral not allowed
            referrals[user_id] = ref_id
            user_invites[ref_id] = user_invites.get(ref_id, 0) + 1

    # Step 1: Show Join Channels Page (with buttons)
    join_msg = (
        f"👋 Hey {name}, Welcome To {BOT_NAME} 💌\n\n"
        "📢 Number lene se pehle please in channels ko join karo 👇\n\n"
        "✅ Done karne ke baad niche button dabao."
    )

    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel 1", url="https://t.me/+s7yZ3tNTklA0Nzll")],
        [InlineKeyboardButton("🔗 Join Channel 2", url="https://t.me/+lIRyYpOv3zc4MzA1")],
        [InlineKeyboardButton("🔗 Join Channel 3", url="https://t.me/Script_Promoter")],
        [InlineKeyboardButton("🔗 Join Channel 4", url="https://t.me/WHITE_METHODZ")],
        [InlineKeyboardButton("✅ Done", callback_data="done_channels")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(join_msg, reply_markup=reply_markup)


# -------------------- BUTTON HANDLER --------------------
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Step 2: After Done → Show App Selection
    if query.data == "done_channels":
        app_msg = "👇 Choose Application Where You Want Free Temporary Number 📬"
        keyboard = [
            [InlineKeyboardButton("Instagram", callback_data="instagram")],
            [InlineKeyboardButton("Telegram", callback_data="telegram")],
            [InlineKeyboardButton("WhatsApp", callback_data="whatsapp")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(app_msg, reply_markup=reply_markup)

    # Step 3: App Selected → Generate Number
    elif query.data in ["instagram", "telegram", "whatsapp"]:
        app = query.data

        query.message.reply_text("Processing... ⏳")
        time.sleep(1)
        query.message.reply_text("Almost Done... 🔄")
        time.sleep(1)

        # Generate random number
        number = "+91" + str(random.randint(7000000000, 9999999999))
        query.message.reply_text(
            f"📱 App: {app.capitalize()}\n\n"
            f"Country Code: +91\n\nYour Number Has Been Generated 👇\n\n{number}"
        )

        # Step 4: Invite condition
        query.message.reply_text(
            "📥 First Invite 10 Users To Get Free OTP\n\n"
            "Use /invite Command For Complete 10 Invites."
        )


# -------------------- INVITE COMMAND --------------------
def invite(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    count = user_invites.get(user_id, 0)

    if count >= 10:
        update.message.reply_text("✅ Congrats! You unlocked OTP service 🎉")
    else:
        update.message.reply_text(
            f"📥 You have invited {count} users.\n"
            f"Invite {10 - count} more to unlock OTP service."
        )

    # Referral link
    bot_username = context.bot.username or BOT_USERNAME
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    update.message.reply_text(f"🔗 Your Referral Link:\n{ref_link}")

keep_alive()
# -------------------- MAIN FUNCTION --------------------
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("invite", invite))
    dp.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot started successfully...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":

    main()
