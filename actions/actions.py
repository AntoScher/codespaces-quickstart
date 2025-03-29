from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from googleapiclient.discovery import build
from google_auth import get_credentials
import pytz
from datetime import datetime, timedelta  # Добавлен timedelta
import logging  # Добавлено логирование

class ActionCreateCalendarEvent(Action):
    def name(self):
        return "action_create_calendar_event"

    async def run(self, dispatcher, tracker, domain):
        # Извлечение данных из слотов
        event_title = tracker.get_slot("event_title")
        event_date = tracker.get_slot("date")
        event_time = tracker.get_slot("time")

        # Проверка заполнения всех слотов
        if not all([event_title, event_date, event_time]):
            dispatcher.utter_message("Ошибка: Не все данные заполнены!")
            return []

        try:
            # Аутентификация
            creds = get_credentials()
            service = build('calendar', 'v3', credentials=creds)

            # Парсинг времени с обработкой формата
            try:
                time_format = "%Y-%m-%d %H:%M:%S" if ":" in event_time.count(":") == 2 else "%Y-%m-%d %H:%M"
                start_time = datetime.strptime(f"{event_date} {event_time}", time_format)
            except ValueError as e:
                dispatcher.utter_message(f"Ошибка формата времени: {str(e)}")
                return []

            # Работа с временной зоной
            timezone = pytz.timezone("Europe/Moscow")
            start_time = timezone.localize(start_time)
            end_time = start_time + timedelta(hours=1)  # Исправлено: используем локализованное время

            # Создание события
            event = {
                'summary': event_title,
                'start': {'dateTime': start_time.isoformat()},
                'end': {'dateTime': end_time.isoformat()},
            }
            
            # Вызов API
            service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            
            dispatcher.utter_message("Событие создано в Google Calendar!")
            # Очищаем слоты только при успехе
            return [
                SlotSet("event_title", None),
                SlotSet("date", None),
                SlotSet("time", None)
            ]

        except Exception as e:
            logging.error(f"Google API Error: {str(e)}")
            dispatcher.utter_message(f"Ошибка при создании события: {str(e)}")
            # Не очищаем слоты для возможности повтора
            return []
        # actions.py
class ActionAskEventTitle(Action):
    def name(self):
        return "action_ask_event_title"
    
    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_ask_event_title")
        return []