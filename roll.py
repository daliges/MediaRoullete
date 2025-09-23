import telebot
import re

def roll(message, bot):
    # Ask the user for a channel link
    bot.send_message(message.chat.id, "Send a channel link from which you want to get random media")

    # Define a handler for the next message only
    def process_channel_link(msg):
        channel_link = msg.text

        # Validate the channel link
        # Validate the channel link (accepts public channels with dashes and private invite links)
        if not re.match(r'^https://t\.me/([\w\-]+|\+[\w\-]+)$', channel_link):
            bot.send_message(
                msg.chat.id,
                "Invalid channel link. Please send a valid Telegram public channel (https://t.me/username) or private invite link (https://t.me/+hash)."
            )
            return
        # Process the channel link (fetch media, etc.)
        bot.send_message(msg.chat.id, f"Processing media from the channel: {channel_link}")

        # Example: Fetch random media (you'll need to implement this part)
        # media = fetch_random_media_from_channel(channel_link)
        # bot.send_message(msg.chat.id, f"Here is your random media: {media}")

    bot.register_next_step_handler(message, process_channel_link)
