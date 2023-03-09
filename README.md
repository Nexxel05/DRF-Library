# Library API

Django Rest Framework project for management of 
books and borrowings in library

## Features:
* Authentication functionality
* Management of books inventory
* Monitoring of due borrowings
* Notifications via Telegram

## How to run

Project supports sending notification via telegram for various occasions. 
Skip telegram part if you don't need this.

### Create telegram bot

1. Proceed to https://telegram.me/BotFather or search for **BotFather** in your telegram app
2. Click **Start**
3. Type **/newbot** and follow short instructions
4. Receive the bot **token** - store it safely!!!

### Create telegram group

1. Create telegram group where notifications received
2. Add telegram bot that you've just created to group
3. Type something in newly created group
4. Navigate to https://api.telegram.org/bot<YourBOTToken>/getUpdates
where _YourBOTToken_ is your bot token.
For example: https://api.telegram.org/bot123456789:jbd78sadvbdy63d37gda37bd8/getUpdates
5. Look for the **chat** object - store it safely!!!
### Install project

```shell
git clone https://github.com/Nexxel05/DRF-Library.git
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Create .env file in root directory and store there your 
DJANGO_SECRET_KEY, TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID 
like shown in .env_sample

```
python manage.py migrate
python manage.py runserver
```