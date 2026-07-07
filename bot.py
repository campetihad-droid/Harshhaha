from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import random
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@trackethiad"

running = False
task = None
user_last_used = {}

def generate_random_user_id():
    now = datetime.now()

    repeat_users = [
        uid for uid, last_time in user_last_used.items()
        if 300 <= (now - last_time).total_seconds() <= 600
    ]

    if repeat_users and random.randint(1, 100) <= 40:
        uid = random.choice(repeat_users)
        user_last_used[uid] = now
        return uid

    while True:
        uid = f"{random.randint(6000,9999)}****{random.randint(1000,9999)}"
        if uid not in user_last_used:
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


async def send_conversation(context):
    global running

    while running:
        for _ in range(10):
            now = datetime.now()
            user_id = generate_random_user_id()

            run_time = (now - timedelta(minutes=1)).strftime("%m/%d/%Y %H:%M:%S")
            track_time = now.strftime("%m/%d/%Y %H:%M:%S")

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=build_message(user_id, "0.1", run_time, track_time)
            )

            asyncio.create_task(
                send_second_message(context, user_id, run_time)
            )

                await asyncio.sleep(60)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running, task

    if running:
        await update.message.reply_text("⚠️ Test already running.")
        return

    running = True
    task = asyncio.create_task(send_conversation(context))

    await update.message.reply_text("✅ Test Started.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running, task

    running = False

    if task:
        task.cancel()
        task = None

    await update.message.reply_text("🛑 Test Stopped.")
