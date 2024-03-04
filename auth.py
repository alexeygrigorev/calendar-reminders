import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate():
    """Authenticate the user and generate a new token.json file."""
    creds = None
    token_path = "token.json"

    # Check if the token.json file exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If credentials are not valid, initiate the login flow
    if not creds or not creds.valid:
        print("No valid credentials. Initiating login flow...")
        if creds and creds.expired and creds.refresh_token:
            try:
                print('Attempting to refresh expired credentials...')
                creds.refresh(Request())
            except Exception as e:
                print("Refresh failed: ", str(e))
                # If refresh fails, delete the token.json and initiate new login flow
                print('Deleting expired token and re-initiating authentication flow...')
                os.remove(token_path)
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
        print("Authentication successful. New token.json has been saved.")


if __name__ == "__main__":
    authenticate()
    print('Authentication is successful')
