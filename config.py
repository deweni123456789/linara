import os

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

DEVELOPER = "@deweni2"
SUPPORT_GROUP = "https://t.me/your_support_group_here"
