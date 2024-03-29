import json
from datetime import timedelta, datetime

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bot.register_hook import register_webhook
from bot.check_callbacks import check_callbacks
from bot.send_message import (send_start_message, send_pure_text_message, send_subscribe_link, send_invite_link_message, send_doc, 
                              send_about_message, send_goods_info, send_guide, send_guide_plus,
                                send_channel_info, send_buy_channel, send_channel_msg, send_about_group_message, proccess_user_text, send_pay_notify_message)

from bot.models import Order, Settings

from bot.consts import GROUP_ID, CHANNEL_ID, URL

from bot.get_recurent_pay import get_pay


register_webhook()



def unban_user(user_id, id):
    req = {'chat_id': id, 'user_id': user_id, 'revoke_messages': False}
    requests.post(URL + '/unbanChatMember', json = req)


def invite_link_user(id):
    req = {'chat_id': id, 'member_limit': 1, 'creates_join_request': False}
    res = requests.post(URL + '/createChatInviteLink', json = req)
    return res.json()


@csrf_exempt
def prodamus_webhook(request):   
    data = request.body.decode('utf-8')
    order_id = None
    binding_id = None
    for item in data.split('&'):
        if 'order_num=' in item:
            order_id = int(item.split('-')[1])
        if 'binding_id' in item:
            binding_id = item.split('=')[1]
    order = Order.objects.get(id=order_id)
    order.paid = True
    order.save()
    profile = order.profile
    settings = Settings.objects.first()
    if order.subscribe_type == 3:
        # отправка чек-листа (пока отключаем)
        send_doc(profile.user_id)
    if order.subscribe_type == 5:
        # отправка чек-листа (пока отключаем)
        send_guide(profile.user_id)
    if order.subscribe_type == 6:
        # отправка чек-листа (пока отключаем)
        send_guide_plus(profile.user_id)
    if order.subscribe_type == 1:
        if profile.premium_bought_to and profile.premium_bought_to > datetime.now().date():
            # если у юзера есть дата подписки и она больше чем текущая дата, то ничего не делать, иначе скинуть ссылку
            send_pay_notify_message(order.profile.user_id)
        else:
            unban_user(order.profile.user_id, CHANNEL_ID)
            invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
            print(invite_link)
            send_invite_link_message(settings.invite_message_channel, order.profile.user_id, invite_link)
        
        profile.premium_bought_to = datetime.now() + timedelta(days=1*30)
        if binding_id:
            profile.binding_id = binding_id
        get_pay(profile.user_id, order.subscribe_type, schedule=timedelta(hours=24*30-14))
    
    # elif order.subscribe_type == 4:
    #     if profile.premium_bought_to and profile.premium_bought_to > datetime.now().date():
    #         # если у юзера есть дата подписки и она больше чем текущая дата, то ничего не делать, иначе скинуть ссылку
    #         send_pay_notify_message(order.profile.user_id)
    #     else:
    #         unban_user(order.profile.user_id, CHANNEL_ID)
    #         invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
    #         print(invite_link)
    #         send_invite_link_message(settings.invite_message_channel, order.profile.user_id, invite_link)
            
    #     profile.premium_bought_to = datetime.now() + timedelta(days=1*365)
    #     if binding_id:
    #         profile.binding_id = binding_id
    #     get_pay(profile.user_id, order.subscribe_type, schedule=timedelta(hours=24*365-14))

    elif order.subscribe_type == 2:
        unban_user(order.profile.user_id, CHANNEL_ID)
        invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
        print(invite_link)
        send_invite_link_message(settings.invite_message_channel, order.profile.user_id, invite_link)

        unban_user(order.profile.user_id, GROUP_ID)
        invite_link = invite_link_user(GROUP_ID)['result']['invite_link']
        print(invite_link)
        send_invite_link_message(settings.invite_message_group, order.profile.user_id, invite_link)

        profile.premium_bought_to = datetime.now() + timedelta(days=1*30)

    # if profile.premium_bought_to:
    #     profile.premium_bought_to += timedelta(days=1*30)
    #     send_pure_text_message(profile.user_id, f"Доступ продлен")
    # else:
    #     unban_user(order.profile.user_id, CHANNEL_ID)
    #     profile.premium_bought_to = datetime.now() + timedelta(days=1*30)
    #     invite_link = invite_link_user(CHANNEL_ID)['result']['invite_link']
    #     print(invite_link)
    #     send_invite_link_message(order.profile.user_id, invite_link)
    #     if order.subscribe_type == 2:
    #         unban_user(order.profile.user_id, GROUP_ID)
    #         invite_link = invite_link_user(GROUP_ID)['result']['invite_link']
    #         print(invite_link)
    #         send_invite_link_message(order.profile.user_id, invite_link)
    profile.save()
    # по ордеру находим пользователя, проставляем ему дату до какого числа он может пользоваться, и отправляем ссылку на вступление в группу
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def webhook(request):   
    
    json_data = json.loads(request.body)

    if 'message' not in json_data and 'callback_query' not in json_data:
        return JsonResponse({'status': 'ok'})
    json_data = check_callbacks(json_data)

    chat_id = json_data['message']['chat']['id']
    user_telegram_username = json_data['message']['chat']['username']
    print(chat_id)
    if chat_id < 0:
        return JsonResponse({'status': 'ok'})

    
    
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
        send_start_message(chat_id) 
    elif text == '/about':
        print('about')
        send_about_message(chat_id)
    elif text == '/buy_goods':
        print('buy_goods')
        send_goods_info(chat_id)
    elif text == '/channel':
        print('channel')
        send_channel_info(chat_id)
    elif text == '/buy_channel':
        print('buy_channel')
        send_channel_msg(chat_id)
    elif text == '/buy_channel_link':
        print('buy_channel_link')
    elif text == '/about_group':
        print('about_group')
        send_about_group_message(chat_id)
    elif text == '/group_buy':
        print('group_buy')
    elif '/subscribe_' in text: 
        send_subscribe_link(chat_id, user_telegram_username, text)
    else:
        proccess_user_text(chat_id, user_telegram_username, text)
    return JsonResponse({'status': 'ok'})
