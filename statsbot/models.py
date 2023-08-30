from django.db import models

# Create your models here.

class Settings(models.Model):

    start_message = models.TextField(default='Стартовое сообщение')
    get_photo_btn_text = models.TextField(default='Получить фото')

    image = models.TextField(default='картинка photo:123')

    def __str__(self) -> str:
        return 'Настройки'


class Profile(models.Model):
    user_id = models.CharField(default='', max_length=100)

    def __str__(self) -> str:
        return self.user_id
