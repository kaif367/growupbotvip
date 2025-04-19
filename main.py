import asyncio
from pyrogram import Client, filters
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Pyrogram bot setup
API_ID = 24356162
API_HASH = "62ec18e1057a76c520f10662c66ef71b"
BOT_TOKEN = "8037173328:AAHHlauP_D9le4nLZJPonaio_p0kyG43elM"
VIP_CHANNEL_LINK = "https://t.me/+YOUR_VIP_INVITE_LINK"  # replace with your actual VIP invite

# Telethon client setup
SESSION_STRING = "1BVtsOI8Bu5MC93OUbsHTCPRyn4rgR1D0EkwvhCGQ3w453y1LQKotWbgdCHyCSuiDD-C0Szgg87sQmVTpBKR9UQDi_DRxRZ8zvbNW3CQKq1UBXH-bu6J-Igb6f-xBIklSUgVDs_0zE08-d6qGMUNUSVsfAeTExNWoupQxg_aC9t9Dv9JRuxo_wBId6MZ2zdITlYidnTbSJEshEUlOX-uu08UeY1yuoECsoijekY_zZpXabg8sejvL3mfhvIXOntVNfTBw8kq_oWB2WDJx0jj12Thev9cidviG4aHLQqLBe8Hs0DLyVBtE9Whqo0vw8HEPrDEk3Z-_fGWi8lGFHTIvtZb0LymYIHo="

bot = Client("growup_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
tele_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Queue for async message passing
pending_checks = {}

@bot.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def handle_trader_id(client, message):
    user_id = message.from_user.id
    trader_id = message.text.strip()

    logging.debug(f"📩 Got trader ID: {trader_id}")  # Debug log

    await message.reply("⏳ Verifying your Trader ID with Quotex Affiliate Bot...")

    async def check_affiliate():
        logging.debug("🛜 Sending ID to QuotexPartnerBot...")  # Debug log
        async with tele_client.conversation("QuotexPartnerBot") as conv:
            logging.debug(f"🔄 Sending {trader_id} to QuotexPartnerBot...")
            await conv.send_message(trader_id)
            logging.debug("✅ ID sent. Waiting for response...")  # Debug log
            response = await conv.get_response()
            logging.debug(f"📨 Got response: {response.text}")  # Debug log

            # Check if response is positive (successful verification)
            if "minimum deposit" in response.text.lower() or "approved" in response.text.lower() or "successfully" in response.text.lower():
                logging.debug("✅ User verified. Sending VIP invite...")
                await bot.send_message(user_id, f"✅ Verified! Here’s your VIP access:\n{VIP_CHANNEL_LINK}")
            elif "not found" in response.text.lower() or "invalid" in response.text.lower():
                logging.debug("❌ Trader ID not found or not under our affiliate.")
                await bot.send_message(user_id, "❌ Trader ID not found or not under our affiliate.")
            else:
                logging.debug(f"⚠️ Unexpected response: {response.text}")
                await bot.send_message(user_id, f"⚠️ Unexpected response:\n\n{response.text}")

    asyncio.create_task(check_affiliate())

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    logging.debug(f"🟢 Bot started by user {message.from_user.id}")
    await message.reply("👋 Welcome! Send your Quotex Trader ID to verify and join our VIP channel.")

async def main():
    try:
        logging.debug("🔄 Starting Telethon...")
        await tele_client.start()
        logging.debug("✅ Telethon started")

        logging.debug("🔄 Starting Pyrogram bot...")
        await bot.start()
        logging.debug("🚀 Bot is running!")
        
        await idle()
    except Exception as e:
        logging.error(f"❌ Error starting bot: {e}")

from pyrogram import idle

if __name__ == "__main__":
    asyncio.run(main())
