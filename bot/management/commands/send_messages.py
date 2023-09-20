from django.core.management.base import BaseCommand
from bot.models import Posts

from bot.send_posts import send_posts_to_groups



class Command(BaseCommand):
    help = "get all shifts"

    def handle(self, *args, **options):
        print('send messages')
        posts = Posts.objects.filter(sent=False)  # Получение всех постов с sent=False

        for post in posts:
            # Ваш код для выполнения действий с постом
            send_posts_to_groups(post.message)

            post.sent = True  # Установка sent=True
            post.save()  # Сохранение изменений


