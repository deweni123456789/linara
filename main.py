from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from modules.song import register_song
from modules.video import register_video

app = Client("song_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Send /song <name> or /video <name> to download!")

register_song(app)
register_video(app)

if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run()
