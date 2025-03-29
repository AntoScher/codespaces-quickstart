import os
from dotenv import load_dotenv
load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
if telegram_token:
    print(f"Telegram Token: {telegram_token}")
else:
    print("Telegram Token not found!")

rasa_license = os.getenv("RASA_PRO_LICENSE")
if rasa_license:
    print("Лицензия успешно загружена!")
else:
    print("Лицензия не найдена.")
    