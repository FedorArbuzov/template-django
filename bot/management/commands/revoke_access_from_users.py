import requests
from django.utils import timezone
from django.core.management import BaseCommand


from bot.models import Profile
from bot.consts import URL, GROUP_ID


user_id = 340473490



def ban_user(user_id):
    req = {'chat_id': GROUP_ID, 'user_id': user_id, 'revoke_messages': False}
    requests.post(URL + '/banChatMember', json = req)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(123)
        ban_user(user_id)
        print(f'User {user_id} has been blocked in the group.')
        # current_date = timezone.now().date()

        # # Выбираем пользователей, у которых премиум уже закончился
        # expired_users = Profile.objects.filter(is_premium=True, premium_bought_to__lt=current_date)

        # return expired_users
