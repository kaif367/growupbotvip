from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import re

API_ID = 24356162
API_HASH = "62ec18e1057a76c520f10662c66ef71b"
BOT_TOKEN = "7145293109:AAFpWPXnPbRk_svPa8dSkdn5gvDtiNXOpf8"
VIP_CHANNEL_ID = -1002125235629
MIN_DEPOSIT = 30
QUOTEX_BOT_USERNAME = "QuotexPartnerBot"

# Pyrogram bot client
bot = Client("GrowUpBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# User session (must already be logged in via `user.session`)
user = Client("user", api_id=API_ID, api_hash=API_HASH)

# Map user_chat_id -> trader_id being checked
pending_checks = {}

@bot.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_trader_id(client: Client, message: Message):
    trader_id = message.text.strip()

    if not trader_id.isdigit():
        await message.reply("❌ Please send a valid Trader ID (numbers only).")
        return

    await message.reply("🔍 Checking your Trader ID with Quotex bot...")

    # Save pending user ID
    pending_checks[message.from_user.id] = trader_id

    # Forward ID to Quotex bot (as a user)
    async with user:
        await user.send_message(QUOTEX_BOT_USERNAME, trader_id)

@user.on_message(filters.chat(QUOTEX_BOT_USERNAME))
async def handle_affiliate_reply(client: Client, message: Message):
    text = message.text

    # Match Trader ID from the bot's response
    trader_id_match = re.search(r"Trader #\s*(\d+)", text)
    if not trader_id_match:
        return  # Not a valid affiliate response

    trader_id = trader_id_match.group(1)

    # Find which user was waiting for this ID
    for user_id, expected_id in list(pending_checks.items()):
        if expected_id == trader_id:
            del pending_checks[user_id]  # Remove from pending

            # Check deposit
            deposit_match = re.search(r"Deposits Sum: \$ ([\d.]+)", text)
            if deposit_match:
                deposit = float(deposit_match.group(1))
                if deposit >= MIN_DEPOSIT:
                    invite = await bot.create_chat_invite_link(chat_id=VIP_CHANNEL_ID, member_limit=1, expires_in=3600)
                    await bot.send_message(user_id, f"✅ Verified! Here is your VIP link (valid for 1 hour):\n{invite.invite_link}")
                else:
                    await bot.send_message(user_id, f"❌ Minimum deposit $30 required. Your deposit: ${deposit:.2f}")
            else:
                await bot.send_message(user_id, "⚠️ Couldn't find deposit info.")
            break

async def main():
    await bot.start()
    await user.start()
    print("🚀 Bot is running...")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())
