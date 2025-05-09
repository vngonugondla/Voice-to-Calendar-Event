import speech_recognition as sr
import dateparser
from datetime import timedelta
from calendar_service import get_calendar_service
from dateparser.search import search_dates
import re

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now")
        audio = r.listen(source)
    return r.recognize_google(audio)

def create_event(service, title, start_time):
    end_time = start_time + timedelta(hours=1)
    event = {
        'summary': title,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'America/New_York'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'America/New_York'},
    }
    service.events().insert(calendarId='primary', body=event).execute()
    
    
def extract_title_and_time(task):
    results = search_dates(task, settings={'PREFER_DATES_FROM': 'future'})
    parsed_time = None

    if results:
        parsed_time = results[0][1]

        for date_text, _ in results:
            task = re.sub(re.escape(date_text), '', task, flags=re.IGNORECASE)

    title = task.strip(" ,.-")
    return title, parsed_time

if __name__ == "__main__":
    try:
        task = get_voice_input()
        print("You said:", task)
        title, parsed_time = extract_title_and_time(task)

        if parsed_time:
            service = get_calendar_service()
            create_event(service, title, parsed_time)
            print("Task added to Google Calendar.")
        else:
            print("No time detected.")
    except Exception as e:
        print("Error", e)