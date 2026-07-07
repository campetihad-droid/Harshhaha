from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import random
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trackethiad"

running = False
used_users = []
user_last_used = {}

def generate_random_user_id():
    now = datetime.now()

    # 5-10 minute purane users repeat honge
    repeat_users = [
        uid for uid, t in user_last_used.items()
        if 300 <= (now - t).total_seconds() <= 600
    ]

    if repeat_users and random.randint(1, 100) <= 40:
        uid = random.choice(repeat_users)
        user_last_used[uid] = now
        return uid

    uid = f"{random.randint(6000,9999)}****{random.randint(1000,9999)}"

    while uid in user_last_used:
        uid = f"{random.randint(6000,9999)}****{random.randint(1000,9999)}"

    user_last_used[uid] = now
    return uid


def build_message(user_id, amount, run_time, track_time):
    return (
        "Test Conversation Count 💝\n\n"
        "🎁 Offer Name - Test\n\n"
        f"User Id : {user_id}\n"
        f"User Amount : ₹{amount}\n"
        "🥳 User Payment : Success\n\n"
        f"Run Time - {run_time}\n"
        f"Track Time - {track_time}\n\n"
                "Powered By - CashFlix"
    )


async def send_conversation(context):
    global running

    while running:
        for _ in range(10):
            user_id = generate_random_user_id()
            now = datetime.now()

            run_time = (now - timedelta(minutes=1)).strftime("%m/%d/%Y %H:%M:%S")
            track_time = now.strftime("%m/%d/%Y %H:%M:%S")

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=build_message(user_id, "0.1", run_time, track_time)
            )

            asyncio.create_task(send_second_message(context, user_id, run_time))

        await asyncio.sleep(60)


async def send_second_message(context, user_id, run_time):
    await asyncio.sleep(60)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=build_message(
            user_id,
            "5",
            run_time,
            datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                )
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running

    if running:
        await update.message.reply_text("⚠️ Test already running.")
        return

    running = True
    asyncio.create_task(send_conversation(context))
    await update.message.reply_text("✅ Test Started.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running

    running = False
    await update.message.reply_text("🛑 Test Stopped.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("stop", stop))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
