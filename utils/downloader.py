import os, asyncio, urllib.request
import yt_dlp
from mutagen import File as MutagenFile
from PIL import Image
from config import DOWNLOAD_PATH

# Ensure downloads folder exists
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Common yt-dlp options
YTDL_COMMON = {
    "quiet": True,
    "no_warnings": True,
    "nocheckcertificate": True,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36"
    },
    "cookiefile": "cookies.txt",  # Optional: Put cookies.txt in same folder for age-restricted content
}

YTDL_OPTS_AUDIO = YTDL_COMMON.copy()
YTDL_OPTS_AUDIO.update({
    "format": "bestaudio/best",
    "noplaylist": True,
    "outtmpl": os.path.join(DOWNLOAD_PATH, "%(id)s.%(ext)s"),
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
})

YTDL_OPTS_VIDEO = YTDL_COMMON.copy()
YTDL_OPTS_VIDEO.update({
    "format": "best",
    "noplaylist": True,
    "outtmpl": os.path.join(DOWNLOAD_PATH, "%(id)s.%(ext)s"),
})

# -----------------------------
# Download Audio
# -----------------------------
async def download_audio(query: str):
    url = query if query.startswith(("http://","https://")) else f"ytsearch1:{query}"
    loop = asyncio.get_event_loop()

    def run_ydl():
        try:
            with yt_dlp.YoutubeDL(YTDL_OPTS_AUDIO) as ydl:
                info = ydl.extract_info(url, download=True)
                if "entries" in info:
                    info = info["entries"][0]

                vid = info.get("id")
                file_path = os.path.join(DOWNLOAD_PATH, f"{vid}.mp3")
                thumb = None
                if info.get("thumbnail"):
                    try:
                        tfile = os.path.join(DOWNLOAD_PATH, f"{vid}_thumb.jpg")
                        urllib.request.urlretrieve(info["thumbnail"], tfile)
                        Image.open(tfile).verify()
                        thumb = tfile
                    except: thumb = None

                return {
                    "title": info.get("title"),
                    "uploader": info.get("uploader"),
                    "duration": int(info.get("duration") or 0),
                    "file_path": file_path,
                    "thumbnail": thumb,
                    "webpage_url": info.get("webpage_url"),
                }
        except Exception as e:
            print("Audio download error:", e)
            return None

    return await loop.run_in_executor(None, run_ydl)

# -----------------------------
# Download Video
# -----------------------------
async def download_video(query: str):
    url = query if query.startswith(("http://","https://")) else f"ytsearch1:{query}"
    loop = asyncio.get_event_loop()

    def run_ydl():
        try:
            with yt_dlp.YoutubeDL(YTDL_OPTS_VIDEO) as ydl:
                info = ydl.extract_info(url, download=True)
                if "entries" in info:
                    info = info["entries"][0]

                vid = info.get("id")
                ext = info.get("ext", "mp4")
                file_path = os.path.join(DOWNLOAD_PATH, f"{vid}.{ext}")
                thumb = None
                if info.get("thumbnail"):
                    try:
                        tfile = os.path.join(DOWNLOAD_PATH, f"{vid}_thumb.jpg")
                        urllib.request.urlretrieve(info["thumbnail"], tfile)
                        Image.open(tfile).verify()
                        thumb = tfile
                    except: thumb = None

                return {
                    "title": info.get("title"),
                    "uploader": info.get("uploader"),
                    "duration": int(info.get("duration") or 0),
                    "file_path": file_path,
                    "thumbnail": thumb,
                    "webpage_url": info.get("webpage_url"),
                }
        except Exception as e:
            print("Video download error:", e)
            return None

    return await loop.run_in_executor(None, run_ydl)

# -----------------------------
# Extract metadata tags for audio
# -----------------------------
def extract_tags(filepath: str):
    try:
        audio = MutagenFile(filepath, easy=True)
        return {
            "title": audio.get("title", [None])[0],
            "artist": audio.get("artist", [None])[0],
            "duration": int(audio.info.length) if audio.info else None,
        }
    except:
        return {"title": None, "artist": None, "duration": None}
