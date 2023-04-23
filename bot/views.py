import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from bot.register_hook import register_webhook
from bot.send_message import send_pure_text_message


register_webhook()


@csrf_exempt
def webhook(request):   
    json_data = json.loads(request.body)


    chat_id = json_data['message']['chat']['id']
    
    
    text = json_data['message']['text']
    
    # Обработка стартовой команды
    if text == '/start':
        print('start!')
        send_pure_text_message(chat_id, 'Стартовое сообщение') 
        return JsonResponse({'status': 'ok'})
