# Generated by Django 4.2 on 2023-05-01 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='', max_length=100)),
                ('message_count', models.IntegerField(default=0)),
                ('is_premium', models.BooleanField(default=False)),
                ('preferences', models.TextField(default='Общайся со мной как с другом')),
                ('preferences_edit_mode', models.BooleanField(default=False)),
                ('premium_bought_to', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_message', models.TextField(default='Стартовое сообщение')),
                ('subscribe_link', models.CharField(default='Подписаться', max_length=100)),
                ('subscribe_check', models.CharField(default='Проверить', max_length=100)),
                ('channel_id', models.CharField(default='@test_gpt', max_length=100)),
                ('you_subscribed_message', models.TextField(default='Вы подписаны, можете пользоваться')),
                ('you_not_subscribed_message', models.TextField(default='Вы еще не подписаны, подпишитесь пожалуйста')),
                ('subscribe_please_message', models.TextField(default='Подпишитесь пожалуйста на @test_gpt')),
                ('start_dialog', models.CharField(default='Начать диалог', max_length=100)),
                ('profile', models.CharField(default='Профиль', max_length=100)),
                ('max_free_requests_count', models.IntegerField(default=20)),
                ('get_premium_message', models.TextField(default='Напишите @farbuzov чтобы получить премиум')),
                ('get_premium', models.TextField(default='Купить премиум')),
                ('dialog_started_message', models.TextField(default='Диалог начат')),
                ('stop_dialog_button', models.CharField(default='Закончить диалог', max_length=100)),
                ('dialog_stoped_message', models.TextField(default='Диалог закончен')),
                ('you_got_premium', models.TextField(default='Вы получили премиум')),
                ('set_preferences_button', models.CharField(default='Настройки', max_length=100)),
                ('get_premium_button', models.CharField(default='Получить премиум', max_length=100)),
                ('preferences_start_edit_message', models.TextField(default='Можете начать редактировать')),
                ('preferences_success_edit_message', models.TextField(default='Вы отредактировали настройки')),
                ('you_need_to_register', models.TextField(default='Сначала подпишитесь')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('is_send_by_user', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.dialogs')),
            ],
        ),
        migrations.AddField(
            model_name='dialogs',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.proile'),
        ),
    ]
