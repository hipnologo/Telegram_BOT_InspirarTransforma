import openai
import telegram
import os
from telegram.ext import Updater, Job, CommandHandler, CallbackContext, MessageHandler
from datetime import timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

openai.api_key = os.environ.get("OPENAI_API_KEY")

bot = telegram.Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
updater = Updater(token=os.environ.get("TELEGRAM_BOT_TOKEN"), use_context=True)
updater.start_polling()

dispatcher = updater.dispatcher

interval = 30
enabled = True

def start(update: telegram.Update, context: CallbackContext):
    global interval
    if context.args:
        interval = int(context.args[0])
    update.message.reply_text(f'Scheduler has been started for every {interval} minutes')
    job_queue = context.job_queue
    job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)

def stop(update: telegram.Update, context: CallbackContext):
    job_queue = updater.job_queue
    job_queue.stop()
    update.message.reply_text(f'Scheduler has been stopped')

def enable(update: telegram.Update, context: CallbackContext):
    global enabled
    enabled = True
    update.message.reply_text('Scheduler has been enabled')

def disable(update: telegram.Update, context: CallbackContext):
    global enabled
    enabled = False
    update.message.reply_text('Scheduler has been disabled')

def hourly(update: telegram.Update, context: CallbackContext):
    interval = 60
    job_queue = updater.job_queue
    job_queue.stop()
    job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)
    update.message.reply_text(f'Interval has been set to {interval} minutes')

def daily(update: telegram.Update, context: CallbackContext):
    interval = 1440 # 24 hours * 60 minutes
    job_queue = updater.job_queue
    job_queue.stop()
    job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)
    update.message.reply_text(f'Interval has been set to {interval} minutes')

def weekly(update: telegram.Update, context: CallbackContext):
    interval = 10080 # 7 days * 24 hours * 60 minutes
    job_queue = updater.job_queue
    job_queue.stop()
    job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)
    update.message.reply_text(f'Interval has been set to {interval} minutes')

def monthly(update: telegram.Update, context: CallbackContext):
    interval = 43800 # 30 days * 24 hours * 60 minutes
    job_queue = updater.job_queue
    job_queue.stop()
    job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)
    update.message.reply_text(f'Interval has been set to {interval} minutes')

def custom(update: telegram.Update, context: CallbackContext):
    #interval = update.message.text.split()[1]
    if context.args:
        try:
            interval = int(update.message.text.split()[1])
            job_queue = context.job_queue
            job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)
            update.message.reply_text(f'Scheduler has been started for every {interval} minutes')
        except ValueError:
            update.message.reply_text(f'{interval} is not a valid interval. Please enter a number.')
            return
    else:
        update.message.reply_text("Please provide an interval in minutes")

def get_quote(update: telegram.Update, context: CallbackContext):
    if enabled:
        try:
            prompt = "Por favor, me dê uma citação inspiradora e transformadora."
            completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            message = completions.choices[0].text
            update.message.reply_text(f'{message}')
        except ValueError:
            update.message.reply_text(f'Some error has just happen')
            return

def send_quote(context: CallbackContext):
    if enabled:
        try:
            prompt = "Please give me a random inspirational quote"
            completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            message = completions.choices[0].text
            context.bot.send_message(chat_id=os.environ.get("CHAT_ID"), text=message)
        except ValueError:
            update.message.reply_text(f'Some error has just happen')
            return
    
def start_scheduler(update: telegram.Update, context: CallbackContext):
    interval = int(context.args[0]) if context.args else 30 #if no argument is passed use 30 as default
    job_queue = updater.job_queue
    job_queue.run_repeating(send_quote, timedelta(minutes=interval), context=context)
    update.message.reply_text(f'Scheduler has been started for every {interval} minutes')
    if enabled:
        prompt = "Please give me a random inspirational quote"
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text
        context.bot.send_message(chat_id=update.message.chat_id, text=message)

def create_menu():
    button_list = [[InlineKeyboardButton("Start", callback_data="start"),
                    InlineKeyboardButton("Stop", callback_data="stop"),
                    InlineKeyboardButton("Daily", callback_data="daily"),
                    InlineKeyboardButton("Weekly", callback_data="weekly"),
                    InlineKeyboardButton("Get_Quote", callback_data="get_quote")
                    ]]
    return InlineKeyboardMarkup(button_list)

def menu_handler(update, context):
    update.message.reply_text("Please select an option:", reply_markup=create_menu())
    
daily_handler = CommandHandler('daily', daily)
dispatcher.add_handler(daily_handler)
weekly_handler = CommandHandler('weekly', weekly)
dispatcher.add_handler(weekly_handler)
monthly_handler = CommandHandler('monthly', monthly)
dispatcher.add_handler(monthly_handler)

custom_handler = CommandHandler('custom', custom)
dispatcher.add_handler(custom_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)
enable_handler = CommandHandler('enable', enable)
dispatcher.add_handler(enable_handler)
disable_handler = CommandHandler('disable', disable)
dispatcher.add_handler(disable_handler)

get_quote_handler = CommandHandler('get_quote', get_quote)
dispatcher.add_handler(get_quote_handler)

menu_handler_handler = CommandHandler("menu", menu_handler)
dispatcher.add_handler(menu_handler_handler)

updater.start_polling()
