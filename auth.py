import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate():
    """Authenticate the user and generate a token.json file."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("No valid credentials found.")
        if creds and creds.expired and creds.refresh_token:
            print('Refreshing credentials...')
            creds.refresh(Request())
        else:
            print('Creating new credentials...')
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        print("Authentication successful. token.json has been saved.")
        with open("token.json", "w") as token:
            token.write(creds.to_json())


if __name__ == "__main__":
    authenticate()
    print('Authentication is successful')
