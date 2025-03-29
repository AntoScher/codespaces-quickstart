from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from googleapiclient.discovery import build
from google_auth import get_credentials
import pytz
from datetime import datetime

class ActionCreateCalendarEvent(Action):
    def name(self):
        return "action_create_calendar_event"

    async def run(self, dispatcher, tracker, domain):
        # Извлечение данных из слотов
        event_title = tracker.get_slot("event_title")
        event_date = tracker.get_slot("date")
        event_time = tracker.get_slot("time")

        # Аутентификация
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        # Форматирование времени
        start_time = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
        timezone = pytz.timezone("Europe/Moscow")
        start_time = timezone.localize(start_time).isoformat()
        end_time = (datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)).isoformat()

        # Создание события
        event = {
            'summary': event_title,
            'start': {'dateTime': start_time},
            'end': {'dateTime': end_time},
        }
        
        try:
            service.events().insert(calendarId='primary', body=event).execute()
            dispatcher.utter_message("Событие создано в Google Calendar!")
        except Exception as e:
            dispatcher.utter_message(f"Ошибка: {str(e)}")

        return [SlotSet("event_title", None), SlotSet("date", None), SlotSet("time", None)]