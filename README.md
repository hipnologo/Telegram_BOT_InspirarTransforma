# InspirarTransforma Telegram BOT

This Telegram BOT is designed to send users an inspirational and transformative quote on a regular interval. The interval can be customized to the user's preference, and the BOT can be started, stopped, enabled, and disabled using commands.

## Requirements
- Python 3.x
- Telegram API key
- OpenAI API key

## Installation
1. Clone the repository to your local machine:

git clone https://github.com/hipnologo/InspirarTransforma.git

2. Install the required libraries:

pip install -r requirements.txt

3. Set up your Telegram and OpenAI API keys as environment variables:

export TELEGRAM_BOT_TOKEN=<your_telegram_api_key>
export OPENAI_API_KEY=<your_openai_api_key>

## Usage
1. Start the BOT:

python bot.py

2. Send the BOT the following commands to customize the interval:
- `/start` - starts the BOT with a default interval of 30 minutes
- `/start <interval in minutes>` - starts the BOT with a custom interval
- `/hourly` - sets the interval to 60 minutes
- `/daily` - sets the interval to 1440 minutes (24 hours)
- `/weekly` - sets the interval to 10080 minutes (7 days)
- `/monthly` - sets the interval to 43800 minutes (30 days)
- `/custom <interval in minutes>` - sets a custom interval
- `/stop` - stops the BOT
- `/enable` - enables the BOT
- `/disable` - disables the BOT
- `/get_quote` - sends a quote immediately 

## Note
The Telegram BOT uses OpenAI's GPT-3 to generate the quotes. The user must have a valid OpenAI API key for the BOT to function properly.
