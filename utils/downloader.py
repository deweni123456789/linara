import os, asyncio, urllib.request
import yt_dlp
from mutagen import File as MutagenFile
from PIL import Image
from config import DOWNLOAD_PATH

YTDL_OPTS_AUDIO = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "outtmpl": os.path.join(DOWNLOAD_PATH, "%(id)s.%(ext)s"),
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
}

async def download_audio(query: str):
    url = query if query.startswith(("http://","https://")) else f"ytsearch1:{query}"
    loop = asyncio.get_event_loop()
    def run_ydl():
        with yt_dlp.YoutubeDL(YTDL_OPTS_AUDIO) as ydl:
            info = ydl.extract_info(url, download=True)
            if "entries" in info: info = info["entries"][0]
            video_id = info.get("id")
            file_path = os.path.join(DOWNLOAD_PATH,f"{video_id}.mp3")
            thumb=None
            if info.get("thumbnail"):
                try:
                    tfile=os.path.join(DOWNLOAD_PATH,f"{video_id}_thumb.jpg")
                    urllib.request.urlretrieve(info["thumbnail"], tfile)
                    Image.open(tfile).verify()
                    thumb=tfile
                except: thumb=None
            return {"title": info.get("title"),"uploader": info.get("uploader"),
                    "duration": int(info.get("duration") or 0),"file_path":file_path,
                    "thumbnail":thumb,"webpage_url":info.get("webpage_url")}
    return await loop.run_in_executor(None, run_ydl)

async def download_video(query: str):
    url = query if query.startswith(("http://","https://")) else f"ytsearch1:{query}"
    loop = asyncio.get_event_loop()
    def run_ydl():
        opts = {"format":"best","noplaylist":True,"quiet":True,"no_warnings":True,
                "outtmpl": os.path.join(DOWNLOAD_PATH,"%({id})s.%(ext)s")}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info=ydl.extract_info(url, download=True)
            if "entries" in info: info = info["entries"][0]
            vid=info.get("id"); ext=info.get("ext","mp4")
            fpath=os.path.join(DOWNLOAD_PATH,f"{vid}.{ext}")
            thumb=None
            if info.get("thumbnail"):
                try:
                    tfile=os.path.join(DOWNLOAD_PATH,f"{vid}_thumb.jpg")
                    urllib.request.urlretrieve(info["thumbnail"], tfile)
                    Image.open(tfile).verify()
                    thumb=tfile
                except: thumb=None
            return {"title":info.get("title"),"uploader":info.get("uploader"),
                    "duration":int(info.get("duration") or 0),"file_path":fpath,
                    "thumbnail":thumb,"webpage_url":info.get("webpage_url")}
    return await loop.run_in_executor(None, run_ydl)

def extract_tags(filepath:str):
    try:
        audio=MutagenFile(filepath,easy=True)
        return {"title":audio.get("title",[None])[0],"artist":audio.get("artist",[None])[0],
                "duration":int(audio.info.length) if audio.info else None}
    except:
        return {"title":None,"artist":None,"duration":None}
