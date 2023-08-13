import requests
from django.utils import timezone
from django.core.management import BaseCommand


from bot.models import Profile
from bot.consts import URL, GROUP_ID, CHANNEL_ID
from bot.send_message import send_pure_text_message, send_channel_info


user_id = 340473490



def ban_user(user_id, chat_id):
    req = {'chat_id': chat_id, 'user_id': user_id, 'revoke_messages': False}
    requests.post(URL + '/banChatMember', json = req)


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Получите текущую дату и время
        current_date = timezone.now().date()

        # Найдите пользователей, чья подписка заканчивается через три дня
        users = Profile.objects.filter(premium_bought_to=current_date + timezone.timedelta(days=3), premium_ending_alerted=False)

        for user in users:
            # Отправьте уведомление пользователю
            # Например, отправка электронной почты или уведомление через внешний сервис

            # Обновите флаг уведомления в профиле пользователя
            user.premium_ending_alerted = True
            user.save()
            send_pure_text_message(user.user_id, 'Через 3 дня у вас закончится подписка, пожалуйста продлите')
            send_channel_info(user.user_id)
            self.stdout.write(self.style.SUCCESS(f'Notification sent to user: {user}'))

        # Найти пользователей, у которых закончилась подписка
        users = Profile.objects.filter(premium_bought_to__lt=current_date)

        for user in users:
            # Удалить пользователя из группы

            send_pure_text_message(user.user_id, 'У вас закончилась подписка, пожалуйста продлите')
            send_channel_info(user.user_id)
            ban_user(user.user_id, GROUP_ID)
            ban_user(user.user_id, CHANNEL_ID)
            self.stdout.write(self.style.SUCCESS(f'User removed from group: {user}'))

