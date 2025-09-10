import os, asyncio, urllib.request
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DOWNLOAD_PATH, DEVELOPER, SUPPORT_GROUP
from utils.downloader import download_audio, extract_tags

def build_buttons(bot_username: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Support Group", url=SUPPORT_GROUP),
         InlineKeyboardButton("Add Bot to Group", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("Developer", url=f"https://t.me/{DEVELOPER.lstrip('@')}")]
    ])

def register_song(app: Client):

    @app.on_message(filters.command("song"))
    async def song_handler(client, message):
        # Get query from command or reply
        args = message.text.split(maxsplit=1)
        query = args[1] if len(args) > 1 else (
            message.reply_to_message.text if message.reply_to_message else ""
        )

        if not query:
            await message.reply_text("Usage: /song <song name or YouTube link>")
            return

        msg = await message.reply_text(f"🔍 Searching: {query}")
        data = await download_audio(query)
        if not data:
            await msg.edit("❌ Could not download. Maybe the video is age/restricted. Try using cookies.txt.")
            return

        file_path, title, performer, duration, thumb = (
            data["file_path"], data["title"], data["uploader"], data["duration"], data["thumbnail"]
        )
        tags = extract_tags(file_path)
        title = tags.get("title") or title
        performer = tags.get("artist") or performer
        duration = tags.get("duration") or duration

        requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        caption = f"🎵 {title}\nRequested by: {requester}\nSource: {data['webpage_url']}"

        me = await client.get_me()
        await msg.edit("⬆️ Uploading audio...")

        await client.send_audio(
            message.chat.id,
            audio=file_path,
            caption=caption,
            parse_mode="markdown",
            title=title,
            performer=performer,
            duration=duration,
            thumb=thumb,
            reply_markup=build_buttons(me.username),
        )
        await msg.delete()

        # Cleanup
        for f in os.listdir(DOWNLOAD_PATH):
            try: os.remove(os.path.join(DOWNLOAD_PATH, f))
            except: pass
