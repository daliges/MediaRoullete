import telebot
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Hello! I'm your MediaRoullete bot. " \
                    " You can just run a command /random to get a random media")
    
bot.polling(none_stop=True)   