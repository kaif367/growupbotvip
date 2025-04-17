from pyrogram import Client, filters
from pyrogram.types import Message
import re
import os

API_ID = 24356162
API_HASH = "62ec18e1057a76c520f10662c66ef71b"
BOT_TOKEN = "7145293109:AAFpWPXnPbRk_svPa8dSkdn5gvDtiNXOpf8"
VIP_CHANNEL_ID = -1002125235629
MIN_DEPOSIT = 10

app = Client("GrowUpBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Manual session client (your main account must be logged in here)
from pyrogram import Client as UserClient
user = UserClient("user", api_id=API_ID, api_hash=API_HASH)

QUOTEX_BOT_USERNAME = "QuotexAffiliateBot"  # Replace with actual username if different

@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_trader_id(client: Client, message: Message):
    trader_id = message.text.strip()
    
    if not trader_id.isdigit():
        await message.reply("❌ Please send a valid Trader ID (numbers only).")
        return

    await message.reply("🔍 Checking your Trader ID with Quotex bot, please wait...")

    async with user:
        sent = await user.send_message(QUOTEX_BOT_USERNAME, trader_id)

        @user.on_message(filters.chat(QUOTEX_BOT_USERNAME))
        async def handle_reply(_, msg: Message):
            text = msg.text

            if "Trader #" not in text:
                await client.send_message(message.chat.id, "❌ Trader ID not found. Please ensure it's correct.")
                return

            deposit_match = re.search(r"Deposits Sum: \$ ([\d.]+)", text)
            if deposit_match:
                deposit = float(deposit_match.group(1))
                if deposit >= MIN_DEPOSIT:
                    await client.send_message(message.chat.id, "✅ Verified! Welcome to VIP.")
                    await client.send_message(message.chat.id, f"https://t.me/c/{str(VIP_CHANNEL_ID)[4:]}")
                else:
                    await client.send_message(message.chat.id, f"❌ Minimum deposit $10 required. Your deposit: ${deposit:.2f}")
            else:
                await client.send_message(message.chat.id, "⚠️ Couldn't find deposit info.")

app.run()
