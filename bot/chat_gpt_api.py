import threading

import openai

from bot.models import Settings, Proile, Dialogs, Messages
from bot.send_message import send_gpt_response, send_pure_text_message, send_start_message, send_subscribe_check
from bot.consts import GPT_API_KEY

openai.api_key = GPT_API_KEY


def chat_gpt_request(settings, profile, messages, text, chat_id, dialog):

    messages_to_gpt = []
    messages_to_gpt.append({
        "role": "system", "content": profile.preferences
    })
    for message in messages:
        messages_to_gpt.append({
            "role": "user" if message.is_send_by_user else "assistant",
            "content": message.text
            })
    messages_to_gpt.append({
        "role": "user", "content": text
    })
    response = None
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_to_gpt
        )
    except:
        dialog.delete()
        send_pure_text_message(chat_id, settings.max_gpt_context_limit)
        return

    generated_text = response.choices[0].message.content
    send_gpt_response(chat_id, generated_text)
    profile.message_count += 1
    profile.save()
    user_message = Messages.objects.create(
        dialog=dialog,
        text =text,
        is_send_by_user=True
    )
    user_message.save()
    system_message = Messages.objects.create(
        dialog=dialog,
        text=generated_text,
        is_send_by_user=False
    )
    system_message.save()
    print('ответ сгенерирован')


def make_chat_gpt_request(chat_id, text):
    # проверка что пользователь может делать запросы
    settings = Settings.objects.first()
    profile = Proile.objects.filter(user_id=chat_id).first()
    if not profile:
        send_pure_text_message(chat_id, settings.you_need_to_register)
        send_start_message(chat_id)
        return
    if profile.preferences_edit_mode:
        profile.preferences = text
        profile.preferences_edit_mode = False
        profile.save()
        send_pure_text_message(chat_id, settings.preferences_success_edit_message)
        send_subscribe_check(chat_id)
        return
    if profile.is_premium or profile.message_count < settings.max_free_requests_count:
        dialog = Dialogs.objects.filter(profile=profile).last()
        if not dialog:
            dialog = Dialogs.objects.create(profile=profile)
            dialog.save()
        messages = Messages.objects.filter(dialog=dialog).order_by('created_at')
        send_pure_text_message(chat_id, settings.gpt_process_started)
        t = threading.Thread(target=chat_gpt_request, args=(settings, profile, messages, text, chat_id, dialog))
        t.start()
        print('задача поставлена')
    else:
        send_pure_text_message(chat_id, settings.get_premium_message)
