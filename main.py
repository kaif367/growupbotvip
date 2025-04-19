import asyncio
import logging
from pyrogram import Client, filters
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from pyrogram import idle

# ✅ Logging enabled
logging.basicConfig(level=logging.DEBUG)

# ✅ Replace with your actual data
API_ID = 24356162
API_HASH = "62ec18e1057a76c520f10662c66ef71b"
BOT_TOKEN = "8037173328:AAHHlauP_D9le4nLZJPonaio_p0kyG43elM"
SESSION_STRING = "1BVtsOI8Bu3iMLLZDga5XT3ON-BUSko87s9mwGNFDZGHJSmzwbu_ZlTum-vn9YKLMzVuqM--w4WySsF6SBFEkA0EnJ3lLecg6Em595I-NrmzYHGWtoo8ncOJWOXEE69H0u9WqkmUgEoNcsd0oFwSs_a0VP_naz-Y-H9wvdiZcwDcin2CJcD_kSVLvAxInhIv-1D5gaF4gNEGh59QgXlDPG-IilNua-cvo215D5JBCjLqrtj_L5K5miIRjBjGlmbEB6bMgrlfVZuDbyj2wuW87pWuLnc04PwfmOAqJB8Co6ReBk900H-ygU2W-D4M5bDHKNy9uSRLAuVp-DKb4sx2PZWeYVaUUeU4="
VIP_LINK = "https://t.me/+YOUR_VIP_INVITE_LINK"

bot = Client("growup_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tele_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    logging.info(f"/start command received from {message.from_user.id}")
    await message.reply("👋 Welcome! Please send your Trader ID to get verified.")

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def handle_trader_id(client, message):
    trader_id = message.text.strip()
    user_id = message.from_user.id

    await message.reply("⏳ Checking your Trader ID, please wait...")

    async def verify_id():
        async with tele_client.conversation("QuotexPartnerBot") as conv:
            await conv.send_message(trader_id)
            response = await conv.get_response()
            text = response.text.lower()

            if "minimum deposit" in text or "approved" in text or "successfully" in text:
                await bot.send_message(user_id, f"✅ Verified! Here is your VIP link:\n{VIP_LINK}")
            else:
                await bot.send_message(user_id, "❌ Verification failed. Either Trader ID is invalid or no deposit found.")

    asyncio.create_task(verify_id())

async def main():
    await tele_client.start()
    await bot.start()
    print("🤖 Bot is live and running...")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
