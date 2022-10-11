import requests as r
import os
from dotenv import load_dotenv
load_dotenv()

def send_message(message):
    bot_api = os.getenv("TELEGRAM_KEY")
    channel_id = '-1001749752732'
    channel_url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_api, channel_id, message)
    r.get(channel_url)


def send_message_to_channel(bot_api, channel_id, message):
    channel_url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_api, channel_id, message)
    r.get(channel_url)