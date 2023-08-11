from django.db import models

from django.utils.translation import gettext_lazy as _



class Settings(models.Model):

    start_message = models.TextField(default='Стартовое сообщение')

    payment_link_message = models.TextField(default='Вот вам ссылка на <a href="{}">оплату</a> ')
    success_payment_message = models.TextField(default='Вы оплатили, пользуйтесь ')
    invite_message_channel = models.TextField(default='Вступайте в канал')
    invite_message_group = models.TextField(default='Вступайте в группу')
    access_extended = models.TextField(default='Доступ продлен')
    three_days_left_payment_message = models.TextField(default='У вас осталось 3 дня, продлите доступ ')
    no_access_message = models.TextField(default='У вас больше нет доступа, пополните пожалуйста ')

    file_link = models.TextField(default='')

    def __str__(self) -> str:
        return 'Настройки'


class Profile(models.Model):
    user_id = models.CharField(default='', max_length=100)
    is_premium = models.BooleanField(default=False)
    premium_bought_to = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user_id


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subscribe_type = models.IntegerField()
    paid = models.BooleanField(default=False)


class Tariff(models.Model):
    name = models.CharField(default='', max_length=100)
    price = models.IntegerField(default=500)
    number = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name

