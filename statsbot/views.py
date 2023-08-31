import json

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from statsbot.register_hook import register_webhook
from statsbot.check_callbacks import check_callbacks
from statsbot.send_message import (send_start_message, send_pure_text_message, send_photo_message)


register_webhook()



@csrf_exempt
def webhook(request):   
    
    json_data = json.loads(request.body)
    json_data = check_callbacks(json_data)

    if 'message' not in json_data:
        return JsonResponse({'status': 'ok'})
    chat_id = json_data['message']['chat']['id']
    print(chat_id)
    if chat_id < 0:
        return JsonResponse({'status': 'ok'})

    
    try:
        user_telegram_username = json_data['message']['chat']['username']
    except KeyError:
        user_telegram_username = None
    
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
    if text == '/start' or text == '/menu':
        print('start!')
        send_start_message(chat_id, user_telegram_username) 
    elif text == '/get_photo':
        print('get_photo')
        send_photo_message(chat_id)

    return JsonResponse({'status': 'ok'})