import os
import asyncio  # Add this line
import logging
from pyrogram import Client, filters, idle
from telethon import TelegramClient
from telethon.sessions import StringSession

# Debugging enable karo
logging.basicConfig(level=logging.DEBUG)

# Environment variables (Railway/Config se set karo)
API_ID = int(os.getenv("API_ID", 24356162))
API_HASH = os.getenv("API_HASH", "62ec18e1057a76c520f10662c66ef71b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8037173328:AAHHlauP_D9le4nLZJPonaio_p0kyG43elM")
SESSION_STRING = os.getenv("SESSION_STRING", "1BVtsOI8Bu5MC93OUbsHTCPRyn4rgR1D0EkwvhCGQ3w453y1LQKotWbgdCHyCSuiDD-C0Szgg87sQmVTpBKR9UQDi_DRxRZ8zvbNW3CQKq1UBXH-bu6J-Igb6f-xBIklSUgVDs_0zE08-d6qGMUNUSVsfAeTExNWoupQxg_aC9t9Dv9JRuxo_wBId6MZ2zdITlYidnTbSJEshEUlOX-uu08UeY1yuoECsoijekY_zZpXabg8sejvL3mfhvIXOntVNfTBw8kq_oWB2WDJx0jj12Thev9cidviG4aHLQqLBe8Hs0DLyVBtE9Whqo0vw8HEPrDEk3Z-_fGWi8lGFHTIvtZb0LymYIHo=")
VIP_CHANNEL_LINK = "https://t.me/+YOUR_VIP_LINK"  # Replace karo

# Pyrogram Bot Initialize
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Telethon Client Setup
tele_client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)

# Start Command Handler
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("👋 Send your Quotex Trader ID to verify!")

# Trader ID Handle Karne Ka Logic
@bot.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_trader_id(client, message):
    try:
        trader_id = message.text.strip()
        user_id = message.from_user.id
        
        await message.reply("⏳ Checking with Quotex...")
        
        # Telethon ke through QuotexPartnerBot se baat karo
        async with tele_client.conversation("QuotexPartnerBot", timeout=20) as conv:
            await conv.send_message(trader_id)
            response = await conv.get_response()
            
            if "success" in response.text.lower() or "minimum deposit" in response.text.lower():
                await message.reply(f"✅ Verified! Join VIP: {VIP_CHANNEL_LINK}")
            else:
                await message.reply("❌ Invalid ID / Deposit nahi hua!")
                
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")

# Bot Start Karne Ka Logic
async def main():
    await tele_client.start()
    await bot.start()
    await idle()  # Bot ko running rakho
    await bot.stop()
    await tele_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
