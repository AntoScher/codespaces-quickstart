import os
from dotenv import load_dotenv
load_dotenv()

rasa_license = os.getenv("RASA_PRO_LICENSE")
if rasa_license:
    print("Лицензия успешно загружена!")
else:
    print("Лицензия не найдена.")