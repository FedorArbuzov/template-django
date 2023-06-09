import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bot.register_hook import register_webhook
from bot.check_callbacks import check_callbacks
from bot.send_message import (send_start_message, send_subscribe_link, send_subscribe_check, send_pure_text_message,
                              send_start_dialog, send_stop_dialog, set_premium, get_profile_info,
                              set_preferences_mode, stop_preferences_mode, generate_image_start, stop_generate_mode)
from bot.chat_gpt_api import make_chat_gpt_request

register_webhook()


@csrf_exempt
def webhook(request):   
    
    json_data = json.loads(request.body)
    json_data = check_callbacks(json_data)

    if 'message' not in json_data:
        return JsonResponse({'status': 'ok'})
    chat_id = json_data['message']['chat']['id']
    
    text = json_data['message'].get('text', '')
    if 'document' in json_data['message']:
        send_pure_text_message(chat_id, f"document:{json_data['message']['document']['file_id']}") 
        return JsonResponse({'status': 'ok'})
    if 'video' in json_data['message']:
        send_pure_text_message(chat_id, f"video:{json_data['message']['video']['file_id']}") 
        return JsonResponse({'status': 'ok'})
    if 'photo' in json_data['message']:
        send_pure_text_message(chat_id, f"photo:{json_data['message']['photo'][0]['file_id']}") 
        return JsonResponse({'status': 'ok'})
    
    # Обработка стартовой команды
    if text == '/start':
        print('start!')
        send_start_message(chat_id) 
    elif text == '/subscribe_link':
        send_subscribe_link(chat_id)
    elif text == '/subscribe_check':
        send_subscribe_check(chat_id)
    elif text == '/start_dialog':
        send_start_dialog(chat_id)
    elif text == '/stop_dialog':
        send_stop_dialog(chat_id)
    elif text == '/profile':
        get_profile_info(chat_id)
    elif text == '/set_preferences':
        set_preferences_mode(chat_id)
    elif text == '/stop_preferences_mode':
        stop_preferences_mode(chat_id)
    elif text == '/generate_image_start':
        generate_image_start(chat_id)
    elif text == '/stop_generate_mode':
        stop_generate_mode(chat_id)
    elif text == '/get_premium':
        set_premium(chat_id)
    else:
        make_chat_gpt_request(chat_id, text)
    
    return JsonResponse({'status': 'ok'})
