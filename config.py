import os

API_ID = int(os.getenv("API_ID", "5047271"))
API_HASH = os.getenv("API_HASH", "047d9ed308172e637d4265e1d9ef0c27")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7896090354:AAE_NaVu_d-x-TCJt9CPNMl9t94Mltw_jrw")

DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

DEVELOPER = "@deweni2"
SUPPORT_GROUP = "https://t.me/your_support_group_here"
