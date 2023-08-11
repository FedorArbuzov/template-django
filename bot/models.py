from django.db import models

from django.utils.translation import gettext_lazy as _



class Settings(models.Model):

    start_message = models.TextField(default='Что сейчас в доступе?')

    payment_link_message = models.TextField(default='Вот вам ссылка на <a href="{}">оплату</a> ')
    success_payment_message = models.TextField(default='Вы оплатили, пользуйтесь ')
    invite_message_channel = models.TextField(default='Вступайте в канал')
    invite_message_group = models.TextField(default='Вступайте в группу')
    access_extended = models.TextField(default='Доступ продлен')
    three_days_left_payment_message = models.TextField(default='У вас осталось 3 дня, продлите доступ ')
    no_access_message = models.TextField(default='У вас больше нет доступа, пополните пожалуйста ')

    file_link = models.TextField(default='')

    about_btn_text = models.TextField(default='Про автора Бьютимаргиналии')

    about = models.TextField(default="""Мария Милерюс – бьюти-журналист со специализацией по темам косметологии и пластической хирургии. Ее статьи можно найти на таких ресурсах, как Flacon Magazine и Buro 24/7. Мнению Марии доверяют десятки тысяч женщин, потому что она не просто пишет, а проверяет все на личном опыте и умеет задать врачам правильные вопросы, чтобы понять – к кому идти вам. По рекомендациям Марии ее подписчицы находят своих лучших специалистов. Многие признаются, что Мария – их проводник в мир эстетической медицины, ведь они перестали бояться косметологии и хирургии, именно благодаря ей. 

А еще Мария – женщина, которая смогла кардинально поменять свою жизнь, уйти из офисной рутины в разгар кризиса, начать монетизировать себя и зарабатывать в шестизначных цифрах, запустив первые в своем роде обучения по телеграму. Это все получилось у нее, благодаря философии жизни под названием #нахулойгия, которая включает в себя смелое проявление (которому можно научиться) и умение действовать (которое нужно практиковать и Маша знает – как). 
""")

    channel_btn_text = models.TextField(default='Закрытый канал #нахуйлогии')

    close_channel = models.TextField(default="""Что даст вам доступ в закрытый канал #нахуйлогии 

Если коротко, то контент по теме #нахуйлогия нонстоп, а не только, когда у Маши будет на него время. 

Если подробно, то: 

более личные голосовухи, кружочки, эфиры с Машей на темы смелого проявления, ценности себя, важности действий – в канале была верхушка айсберга, а тут будут реальные примеры ситуаций и решений; 

эфиры Маши с приглашенными коучами и психологами;

личные рекомендации Маши по фильмам, книгам, практикам, цитаты Маши и великих людей в карточках и прочие мелочи, которые вы в обычной жизни воспринимаете, как знаки поднять жопу – но их ничтожно мало, и поэтому вы ничего не делаете;

поддержка, которой не хватает от вашего окружения, чтобы верить в себя, не бросать свои начинания, понять, что вы не одни со своими сложностями; 

инсайты, море инсайтов о себе, реальная мотивация к действию и качественному улучшению своей жизни шаг за шагом (больше денег, классные люди вокруг, радость). 

Если с вас достаточно, то тариф «Святая база» – для вас. """)

    close_channel_btn_text = models.TextField(default='С меня достаточно')

    buy_channel_btn = models.TextField(default='Тариф «Святая база» 1 490 Р')


    about_group = models.TextField(default="""Мы любим людей, которым вечно всего мало. Значит, вы всегда хотите большего. 

Поэтому вы можете оплатить тариф «База + чат инсайтов». """)

    channel_msg = models.TextField(default="""Дает доступ к закрытому каналу на 1 месяц (я напомню вам обновить подписку, не переживайте).""")

    group_msg = models.TextField(default="""Дает доступ к закрытому каналу на 1 месяц (я напомню вам обновить подписку, не переживайте) + доступ к закрытому чату с другими участниками, куда вы можете писать свои инсайты и читать чужие, перечитывать и держать перед глазами, чтобы не упускать философию #нахуйлогии из своей жизни. И делать запросы на интересующие вас темы. """)



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

