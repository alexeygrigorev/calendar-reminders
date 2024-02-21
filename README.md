# calendar-reminders
An app that creates an event at random day of the month


## Preparing the local environment

Clone the repository to your local machine

```bash
git clone git@github.com:alexeygrigorev/calendar-reminders.git
cd calendar-reminders
```

Install the dependencies

```bash
pip install pipenv
pipenv install
```

Activate the virtual environment:
```bash
pipenv shell
```


## Running the Application

Make sure you have `credentials.json` file (see below)

**First, run the `auth.py` script** to authenticate with Google and generate the `token.json` file.

This step is necessary only once, or whenever the token needs to be refreshed.

```bash
# python auth.py
make auth
```

Follow the on-screen instructions to log in to your Google account and authorize the application. This process will create a `token.json` file in your project directory.

**Run `main.py`**, which will create events in your Google Calendar:

``` bash
# python main.py
make run
```

Make sure both `credentials.json` and `token.json` are in the same directory.


## Obtaining `credentials.json` for Google Calendar API

To access the Google Calendar API, you need to obtain `credentials.json` by following these steps:

1. **Go to the Google Developers Console**:
   - Visit [https://console.developers.google.com/](https://console.developers.google.com/) and sign in with your Google account.

2. **Create a New Project**:
   - Click on the project dropdown next to the Google Cloud Platform logo in the top left corner.
   - Click on the "NEW PROJECT" button at the top right.
   - Enter a project name and select a billing account as applicable. Click "CREATE".

3. **Enable the Google Calendar API**:
   - With your project selected, navigate to "APIs & Services".
   - Click "+ ENABLE APIS AND SERVICES" at the top.
   - Search for "Google Calendar API" and click on it.
   - Click the "ENABLE" button to enable the API for your project.

4. **Create Credentials**:
   - After enabling the API, click on "Create Credentials" at the top of the page.
   - Choose "User data" as the credential type.
   - If prompted, configure the consent screen by selecting "External" and providing the necessary information (app name, user support email, etc.). Save the consent screen settings.
   - Back in the "Create credentials" flow, select "Application type" as "Desktop app".
   - Enter a name for your OAuth 2.0 client ID and click "Create".

5. **Download the Credentials**:
   - After creating the client ID, click the "Download JSON" button on the OAuth 2.0 Client IDs section of the Credentials page.
   - Rename the downloaded file to `credentials.json` and place it in your project directory.

If you encounter the error "Access blocked: Cron Calendar has not completed the Google verification process," follow these steps:

Add Test Users

1. Navigate to your project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Select "APIs & Services" > "OAuth consent screen".
3. Scroll to the "Test users" section and click on "ADD USERS".
4. Enter the email address(es) of the user(s) you wish to grant access to, and save your changes.

Verification (optionally), to make the app available beyond test users:

1. Ensure compliance with [Google's API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy).
2. On the "OAuth consent screen" page, find and click the option to submit your app for verification, then follow the instructions provided.


## Telegram Bot Setup

Create a Telegram Bot:
* **Bot Creation**: Chat with `@BotFather` on Telegram, use `/newbot`, follow prompts.
* **Save Token**: Note down the token - this is your `TELEGRAM_BOT_TOKEN`

Obtain Your Telegram User ID

* **Get User ID**: Start a chat with `@userinfobot` to receive your chat_id - this is your `TELEGRAM_CHAT_ID`.

Setup Environment Variables with direnv
* Ensure `direnv` is installed.
* **Prepare .envrc**:
   - Copy `.envrc_template` to `.envrc`.
   - Replace placeholders with your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
* **Enable direnv**: Run `direnv allow` in your project directory.


## Deploying to AWS Lambda

### Step 1: Create Your Lambda Function on AWS

1. **Navigate to AWS Lambda**: Go to the AWS Management Console and open the Lambda service.
2. **Create Function**: Click on "Create function".
3. **Configure**: Choose "Author from scratch". Set your function name (e.g. "present-reminder"), select Python 3.9 as the runtime, and configure permissions as needed.

### Step 2: Set Environment Variables in AWS Lambda

1. In your Lambda function's configuration page, find the "Environment variables" section.
2. Add the necessary environment variables (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).

### Step 3: Modify Deployment Script

1. Open `deploy_to_lambda.sh` in your editor.
2. Replace `LAMBDA_FUNCTION_NAME="YourLambdaFunctionName"` with the name of your Lambda function.

### Step 4: Execute the Deployment Script

1. Ensure the script is executable:

```bash
chmod +x deploy_to_lambda.sh
```

2. Run the script:

```bash
./deploy_to_lambda.sh
```

**Note**: For the AWS CLI upload to work, you need the AWS CLI installed and configured with the appropriate permissions.


## Scheduling Lambda with Amazon EventBridge

### Step 1: Open Amazon EventBridge
1. Navigate to the [Amazon EventBridge service](https://eu-west-1.console.aws.amazon.com/events/home) in the AWS Management Console.

### Step 2: Create Rule
1. Click on "Create rule".
2. Enter a name and description for your rule. (e.g. "present-reminder")

### Step 3: Define Trigger with Cron
- For "Define pattern", select "Schedule".
- Choose "Cron expression" and enter your desired cron schedule.

  Example for running at 8 AM on the first day of every month:

  ```
  cron(0 8 1 * ? *)
  ```
- Check next 10 trigger dates to verify that the trigger is set correctly

### Step 4: Select Target
- In the "Select targets" section, choose "Lambda function" as the target.
- Select your Lambda function from the dropdown list.

### Step 5: Configure Input (Optional)

```json
{"test": true}
```

(it doesn't really matter)

### Step 6: Deploy Rule
1. Click "Create" to deploy your rule.

Your Lambda function is now scheduled to run monthly via Amazon EventBridge.
