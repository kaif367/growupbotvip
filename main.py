import asyncio
from pyrogram import Client, filters
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

# Pyrogram bot setup
API_ID = 24356162
API_HASH = "62ec18e1057a76c520f10662c66ef71b"
BOT_TOKEN = "8037173328:AAHHlauP_D9le4nLZJPonaio_p0kyG43elM"
VIP_CHANNEL_LINK = "https://t.me/+YOUR_VIP_INVITE_LINK"  # replace with your actual VIP invite

# Telethon client setup
SESSION_STRING = "1BVtsOI8Bu3iMLLZDga5XT3ON-BUSko87s9mwGNFDZGHJSmzwbu_ZlTum-vn9YKLMzVuqM--w4WySsF6SBFEkA0EnJ3lLecg6Em595I-NrmzYHGWtoo8ncOJWOXEE69H0u9WqkmUgEoNcsd0oFwSs_a0VP_naz-Y-H9wvdiZcwDcin2CJcD_kSVLvAxInhIv-1D5gaF4gNEGh59QgXlDPG-IilNua-cvo215D5JBCjLqrtj_L5K5miIRjBjGlmbEB6bMgrlfVZuDbyj2wuW87pWuLnc04PwfmOAqJB8Co6ReBk900H-ygU2W-D4M5bDHKNy9uSRLAuVp-DKb4sx2PZWeYVaUUeU4="

bot = Client("growup_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tele_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Queue for async message passing
pending_checks = {}

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def handle_trader_id(client, message):
    user_id = message.from_user.id
    trader_id = message.text.strip()

    await message.reply("⏳ Verifying your Trader ID with Quotex Affiliate Bot...")

    async def check_affiliate():
        async with tele_client.conversation("QuotexPartnerBot") as conv:
            await conv.send_message(trader_id)
            response = await conv.get_response()
            reply = response.text.lower()

            if "minimum deposit" in reply or "approved" in reply or "successfully" in reply:
                await bot.send_message(user_id, f"✅ Verified! Here’s your VIP access:\n{VIP_CHANNEL_LINK}")
            elif "not found" in reply or "invalid" in reply:
                await bot.send_message(user_id, "❌ Trader ID not found or not under our affiliate.")
            else:
                await bot.send_message(user_id, f"⚠️ Unexpected response:\n\n{response.text}")

    asyncio.create_task(check_affiliate())

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply("👋 Welcome! Send your Quotex Trader ID to verify and join our VIP channel.")

async def main():
    await tele_client.start()
    await bot.start()
    print("🚀 Bot is running!")
    await idle()

from pyrogram import idle

if __name__ == "__main__":
    asyncio.run(main())
