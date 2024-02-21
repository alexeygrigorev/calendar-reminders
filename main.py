import datetime
import random

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from telegram import send_telegram_message


def get_credentials():
    """Load the saved credentials from token.json."""
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return creds


def create_event(creds, date):
    """Create an event on the Google Calendar at the specified date."""
    service = build("calendar", "v3", credentials=creds)

    end = date + datetime.timedelta(hours=1)

    event = {
        "summary": "Present",
        "description": "I need to buy a present.",
        "start": {
            "dateTime": date.isoformat(),
            "timeZone": "Europe/Berlin",
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "Europe/Berlin",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()

    event_link = event.get("htmlLink")
    print(f"Event created: {event_link}")

    send_telegram_message(
        f"Buy a present on {date.strftime('%Y-%m-%d')} ({date.strftime('%A')}). Here's the Google Calendar link: {event_link}"
    )


def select_random_date():
    """Select a random date within the current month for the event."""
    today = datetime.date.today()
    current_year, current_month = today.year, today.month
    first_day_of_next_month = datetime.date(current_year, current_month + 1, 1)
    last_day_of_month = (first_day_of_next_month - datetime.timedelta(days=1)).day
    random_day = random.randint(1, last_day_of_month)
    return datetime.datetime(current_year, current_month, random_day, 8, 0)  # 8 AM CET


def main():
    try:
        creds = get_credentials()
        event_date = select_random_date()
        create_event(creds, event_date)
    except Exception as e:
        error_message = f"calenar-reminder: failed to create the event: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)

if __name__ == "__main__":
    main()
