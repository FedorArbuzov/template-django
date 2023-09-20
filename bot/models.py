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
    check_list_btn_text = models.TextField(default='Чеклист «Дорогое лицо»')

    check_list_text = models.TextField(default="""Все хотят иметь кожу лучше, чем у них есть: без пор, матовую, сияющую здоровым блеском, подтянутую, плотную, гладкую и однотонную. И желательно – сохранить результат надолго. 

Кажется, что методов куча и постоянно появляются новые – как проверить каждый, ведь их много, а опыт подруг не показателен, ведь их кожа другая и они другого возраста?!

А что, если я скажу, что МНОГО аппаратов и препаратов, а методов, по которому они работают – НЕМНОГО? И добавлю, что возраст и тип кожи вообще не решающие факторы в выборе метода? Так и есть. 

Вместе с косметологами пространства Lume21 Маша разработала самый понятный путь к идеальной коже для всех, независимо от возраста, пола и типа кожи, города и даже страны, где вы находитесь. 

Этот чеклист будет работать на вас всегда и везде – даже когда косметологов заменят роботы. Он будет передаваться из поколения в поколение. И ваши дети и внуки скажут вам за него спасибо. 

Он не просто покажет, какие есть методы и продукты, но и научит вас правильно их выбирать – отсеивая все ненужное и не тратя время и деньги впустую. Он научит вас так хорошо, что косметологи будут бояться впаривать вам ненужное.

Стоимость 3 300 Р""")

    buy_check_list_btn_text = models.TextField(default='Купить чеклист')

    buy_check_list_text = models.TextField(default="""Благодарим вас за приобретение продукта!

Вы присоединились к элитному кругу покупателей, входящих в топ-100, и поэтому мы рады предоставить вам специальный бонус:

https://drive.google.com/file/d/1QJ8SybH1hjSG_CbsRhge-rskpZksWbDY/view?usp=share_link 
document:BQACAgIAAxkBAAIZVWT4Dy2IK2SpD8lXkJgYZEYclYu1AAKSMAAC14nBS8qzs1edYdhBMAQ""")



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
    buy_group_btn = models.TextField(default="Тариф «База + чат инсайтов» 2 490 Р")

    about_group = models.TextField(default="""Мы любим людей, которым вечно всего мало. Значит, вы всегда хотите большего. 

Поэтому вы можете оплатить тариф «База + чат инсайтов». """)

    channel_msg = models.TextField(default="""Дает доступ к закрытому каналу на 1 месяц (я напомню вам обновить подписку, не переживайте).""")

    group_msg = models.TextField(default="""Дает доступ к закрытому каналу на 1 месяц (я напомню вам обновить подписку, не переживайте) + доступ к закрытому чату с другими участниками, куда вы можете писать свои инсайты и читать чужие, перечитывать и держать перед глазами, чтобы не упускать философию #нахуйлогии из своей жизни. И делать запросы на интересующие вас темы. """)



    def __str__(self) -> str:
        return 'Настройки'


class Profile(models.Model):
    user_id = models.CharField(default='', max_length=100)
    username = models.CharField(default='', max_length=100, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    premium_bought_to = models.DateField(blank=True, null=True)
    premium_ending_alerted = models.BooleanField(default=False)

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


class Posts(models.Model):
    message = models.TextField(default='У вас новый материал')
    sent = models.BooleanField(default=False)