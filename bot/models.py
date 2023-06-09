from django.db import models

from django.utils.translation import gettext_lazy as _



class Settings(models.Model):

    start_message = models.TextField(default='Стартовое сообщение')
    subscribe_link = models.CharField(default='Подписаться', max_length=100)
    subscribe_check = models.CharField(default='Проверить', max_length=100)
    back_button = models.CharField(default='Назад', max_length=100)

    channel_link = models.CharField(default='https://t.me/test_gpt', max_length=100)
    channel_id = models.CharField(default='@test_gpt', max_length=100)
    you_not_subscribed_message = models.TextField(default='Вы еще не подписаны, подпишитесь пожалуйста')
    you_subscribed_message = models.TextField(default='Вы подписаны, можете пользоваться')
    you_not_subscribed_message = models.TextField(default='Вы еще не подписаны, подпишитесь пожалуйста')
    subscribe_please_message = models.TextField(default='Подпишитесь пожалуйста на @test_gpt')

    max_gpt_context_limit = models.TextField(default='Достигнуто ограничение по числу сообщений в диалоге, попробуйте задать вопрос в новом диалоге')
    generate_image_command = models.CharField(default='Сгенерировать изображение', max_length=100)
    generate_image_prompt = models.TextField(default='Напишите описание для генерации изображения', max_length=100)
    stop_generate_button = models.CharField(default='Отменить генерацию', max_length=100)
    stop_generate_message = models.TextField(default='Вы отменили генерацию')
    start_generate_message = models.TextField(default='Генрация началась')
    
    start_dialog = models.CharField(default='Начать диалог', max_length=100)
    profile = models.CharField(default='Профиль', max_length=100)

    max_free_requests_count = models.IntegerField(default=20)

    get_premium_message = models.TextField(default='Напишите @farbuzov чтобы получить премиум')
    get_premium = models.TextField(default='Купить премиум')

    dialog_started_message = models.TextField(default='Диалог начат')
    stop_dialog_button = models.CharField(default='Закончить диалог', max_length=100)
    dialog_stoped_message = models.TextField(default='Диалог закончен')
    gpt_process_started = models.TextField(default='Сейчас ответим')

    you_got_premium = models.TextField(default='Вы получили премиум')
    set_preferences_button = models.CharField(default='Настройки', max_length=100)
    get_premium_button = models.CharField(default='Получить премиум', max_length=100)
    preferences_start_edit_message = models.TextField(default='Можете начать редактировать')
    preferences_success_edit_message = models.TextField(default='Вы отредактировали настройки')
    
    you_need_to_register = models.TextField(default='Сначала подпишитесь')

    def __str__(self) -> str:
        return 'Настройки'


class Proile(models.Model):
    user_id = models.CharField(default='', max_length=100)
    message_count = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    preferences = models.TextField(default='Общайся со мной как с другом')
    preferences_edit_mode = models.BooleanField(default=False)
    generate_image_mode = models.BooleanField(default=False)
    premium_bought_to = models.DateField(blank=True, null=True)


class Dialogs(models.Model):
    profile = models.ForeignKey(Proile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    dialog = models.ForeignKey(Dialogs, on_delete=models.CASCADE)
    text = models.TextField(default='')
    is_send_by_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class Posts(models.Model):
    content = models.TextField(verbose_name='Содержимое сообщения')
    
    class GroupOfUsers(models.TextChoices):
        ALL = 'ALL', _('всем')
        ADMINS = 'ADMINS', _('администратор')
        

    group = models.CharField(
        max_length=100,
        choices=GroupOfUsers.choices,
        default=GroupOfUsers.ADMINS,
    )

    is_send = models.BooleanField(default=False, verbose_name='Сообщение отправлено')

    target_users = models.TextField(default="", null=True, blank=True)
    
