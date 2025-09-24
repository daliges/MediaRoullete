import telebot
from telebot.types import BotCommand, BotCommandScopeDefault, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import roll
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Set up bot commands for the side menu
def set_bot_commands():
    commands = [
        BotCommand("help", "Help and information about the bot"),
        BotCommand("random", "Get random media from the channel")
    ]
    bot.set_my_commands(commands, scope=BotCommandScopeDefault())

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "Hello! I'm your Random bot. Use /random to get random media from the channel in private chat with me."
    )

@bot.message_handler(commands=['random'])
def random_media(message):
    roll.roll(message, bot)

# Function to send a message with a deep link to the channel
def send_channel_message_with_deep_link(channel_id):
    bot_username = bot.get_me().username
    deep_link_url = f"https://t.me/{bot_username}?start=channel_{channel_id}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Interact with the Bot", url=deep_link_url)
    )

    bot.send_message(
        channel_id,
        "Hello! To get random media from the channel, please click the button below to start a private chat.",
        reply_markup=keyboard
    )

# Handler to detect when the bot is added as an admin to a channel
@bot.my_chat_member_handler()
def handle_chat_member_update(chat_member_update):
    new_status = chat_member_update.new_chat_member.status
    if new_status == 'administrator':
        chat_id = chat_member_update.chat.id
        print(f"Bot added as admin to channel. Channel ID: {chat_id}")
        send_channel_message_with_deep_link(chat_id)
        # add data to database if needed

# Function to get the channel name based on the channel_id
def get_channel_name(channel_id):
    try:
        chat = bot.get_chat(channel_id)  # Fetch chat details using the channel_id
        return chat.title  # Return the channel's title (name)
    except Exception as e:
        print(f"Error fetching channel name for ID {channel_id}: {e}")
        return "Unknown Channel"  # Fallback if the channel name cannot be retrieved

# Handle the deep link in private chat
@bot.message_handler(commands=['start'])
def start(message):
    # Check if the user started the bot with a deep link
    if message.text.startswith('/start channel_'):
        try:
            # Extract everything after 'channel_'
            channel_id = message.text[len('/start channel_'):]
            # Convert back underscores to minus for negative channel IDs if needed
            channel_id = channel_id.replace('_', '-', 1) if channel_id.startswith('_') else channel_id
        except (IndexError, ValueError) as e:
            print(f"Error parsing deep link: {e}")
            bot.send_message(message.chat.id, "Invalid deep link format.")
            return
        channel_name = get_channel_name(channel_id)
        bot.send_message(
            message.chat.id,
            f"Hello! You are now connected to the channel : {channel_name}. "
            "Use /random to get random media from the channel."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Hello! I'm your Random bot. Use /random to get random media."
        )

set_bot_commands()
bot.polling(none_stop=True)