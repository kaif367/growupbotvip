from pyrogram import Client, filters
from pyrogram.types import Message
from telethon.sync import TelegramClient, events
import asyncio
import re
import os

API_ID = 24356162
API_HASH = "62ec18e1057a76c520f10662c66ef71b"
BOT_TOKEN = "7145293109:AAFpWPXnPbRk_svPa8dSkdn5gvDtiNXOpf8"
VIP_CHANNEL_ID = -1002125235629
QUOTEX_BOT = "QuotexPartnerBot"
MIN_DEPOSIT = 10

app = Client("GrowUpBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
telethon_client = TelegramClient("user_session", API_ID, API_HASH)

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def check_trader_id(client: Client, message: Message):
    trader_id = message.text.strip()
    if not trader_id.isdigit():
        await message.reply("❌ Please send a valid Trader ID (only numbers).")
        return

    await message.reply("⏳ Checking your Trader ID...")
    async with telethon_client:
        sent = await telethon_client.send_message(QUOTEX_BOT, trader_id)
        
        @telethon_client.on(events.NewMessage(from_users=QUOTEX_BOT))
        async def handler(event):
            if trader_id in event.raw_text:
                deposit_match = re.search(r"Deposits Sum: \$ ([\d.]+)", event.raw_text)
                if deposit_match:
                    deposit_amount = float(deposit_match.group(1))
                    if deposit_amount >= MIN_DEPOSIT:
                        await app.send_message(message.chat.id, "✅ You are verified!
Here is your VIP link: https://t.me/c/" + str(VIP_CHANNEL_ID)[4:])
                    else:
                        await app.send_message(message.chat.id, f"❌ Your total deposit is ${deposit_amount}. Minimum ${MIN_DEPOSIT} is required.")
                else:
                    await app.send_message(message.chat.id, "❌ Could not find deposit info. Try again later.")
            await telethon_client.remove_event_handler(handler)

app.start()
telethon_client.start()
print("GrowUpBot is running...")
asyncio.get_event_loop().run_forever()
