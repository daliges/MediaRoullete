import telebot
from telebot.types import BotCommand
from dotenv import load_dotenv
import roll
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Set up bot commands for the side menu
def set_bot_commands():
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("random", "Get random media from the channel"),
        BotCommand("permissions", "Check bot permissions in the channel")
    ]
    bot.set_my_commands(commands)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Hello! I'm your MediaRoulette bot. " \
                    "You can just run a command /random to get a random media.")

@bot.message_handler(commands=['random'])
def random_media(message):
    roll.roll(message, bot)

# Handler to detect when the bot is added as an admin to a channel
@bot.my_chat_member_handler()
def handle_chat_member_update(chat_member_update):
    new_status = chat_member_update.new_chat_member.status
    if new_status == 'administrator':
        chat_id = chat_member_update.chat.id
        print(f"Bot added as admin to channel. Channel ID: {chat_id}")
        # Add database entry


set_bot_commands()
bot.polling(none_stop=True)