import asyncio

import telegram

from bot.consts import TOKEN
from bot.models import Settings



def check_user_suscription_to_channel(user_id):
    settings = Settings.objects.first()
    # Replace YOUR_TOKEN with your bot's API token
    bot = telegram.Bot(token=TOKEN)

    # Replace CHANNEL_ID with your channel's ID (e.g. @my_channel or -1001234567890)
    channel_id = settings.channel_id

    # Replace USER_ID with the user's ID you want to check
    user_id = user_id

    # Use the get_chat_member method to check if the user is a member of the channel
    loop = asyncio.new_event_loop()
    chat_member = loop.run_until_complete(bot.get_chat_member(chat_id=channel_id, user_id=user_id))
    loop.close()

    print(chat_member)

    if chat_member.status == chat_member.MEMBER or chat_member.status == chat_member.OWNER:
        return True
    else:
        return False
