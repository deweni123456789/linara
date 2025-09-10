import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DOWNLOAD_PATH, DEVELOPER, SUPPORT_GROUP
from utils.downloader import download_video

def build_buttons(bot_username: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Support Group", url=SUPPORT_GROUP),
         InlineKeyboardButton("Add Bot to Group", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("Developer", url=f"https://t.me/{DEVELOPER.lstrip('@')}")],
    ])

def register_video(app: Client):

    @app.on_message(filters.command("video"))
    async def video_handler(client, message):
        args = message.text.split(maxsplit=1)
        query = args[1] if len(args) > 1 else message.reply_to_message.text if message.reply_to_message else ""
        if not query:
            await message.reply_text("Usage: /video <name or YouTube link>")
            return

        msg = await message.reply_text(f"🔍 Searching video: {query}")
        data = await download_video(query)
        if not data:
            await msg.edit("❌ Could not download. Try again.")
            return

        file_path, title, performer, duration, thumb = (
            data["file_path"], data["title"], data["uploader"], data["duration"], data["thumbnail"]
        )

        requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        caption = f"📹 {title}\nRequested by: {requester}\nSource: {data['webpage_url']}"

        me = await client.get_me()
        await msg.edit("⬆️ Uploading video...")

        await client.send_video(
            message.chat.id,
            video=file_path,
            caption=caption,
            parse_mode="markdown",
            duration=duration,
            thumb=thumb,
            reply_markup=build_buttons(me.username),
        )
        await msg.delete()
        for f in os.listdir(DOWNLOAD_PATH):
            try: os.remove(os.path.join(DOWNLOAD_PATH, f))
            except: pass
