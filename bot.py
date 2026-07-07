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
