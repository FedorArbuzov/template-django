# Темплейт джанго приложения


## Как использовать

Чтобы использовать выполните:

```
git clone ...
cd <название вашего проекта>
rm -rf .git
git init
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Теперь чтобы дебажить в vs code создайте файл launch.json и туда запишите

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "python": "${workspaceFolder}/env/bin/python",
            "args": [
                "runserver"
            ],
            "django": true,
            "justMyCode": true
        },
    ]
}
```


## Настройка тг-бота


Это приложение отрабатывает как тг-бот если вам нужен просто бекенд пропустите этот шаг и откатитесь на самый первый коммит


1. Зайти в @botfather, создать бота и записать токен
2. Запустить `./ngrok http 8000` скопировать урл
3. Взять токен и урл и положить в `bot/consts.py`
   ```
   TOKEN = "6273372078:AAF8dC4SEhmaK1sJpQiSFEkNd00mGt-L_ew"
   HOST = "https://6a45-185-172-136-20.ngrok-free.app"
   URL = f"https://api.telegram.org/bot{TOKEN}"
   ```
4. Запустить сервис в vs code и написать своему боту /start
5. Все, у вас локально запущен бот, можно разрабатывать


## Настройка приложения на сервере

1. Заходим по ssh на свою виртуалку по логину и паролю
2. Делаем ssh ключ чтобы делать git pull без логина и пароля
    1. В терминале запускаем `ssh-keygen`
    2. Прожимаем везде enter (без пароля и тд)
    3. делаем `cat /root/.ssh/id_rsa.pub` и то что выпало вставляем у себя в гитхабе в разделе с ключами https://github.com/settings/keys
3. Делаем git clone по ssh
4. Настройка https на сервере
    1. Установка nginx 
        ```
            apt-get update
            apt-get install nginx
        ```
    2. Создаем конфиг для nginx в /etc/nginx/sites-available/
        1. `cd /etc/nginx/sites-available/`
        2. `nano <ваш домен напримен nabot>`
        3. Сам конфиг
            ```
                server {
                    listen 80;
                    server_name <ваш домен nabot.ru>;
                    
                    location / {
                        include proxy_params;
                        proxy_pass http://127.0.0.1:8080;
                    }
                }
            ```
        4. Рестартуем nginx `sudo systemctl restart nginx`

    3. Получаем SSL сертификат
        1. Установим certbot от Let's Encrypt: `sudo apt-get install certbot python3-certbot-nginx`

        2. Произведем первичную настройку certbot: `sudo certbot certonly --nginx`

        3. И наконец-то автоматически поправим конфигурацию nginx: `sudo certbot install --nginx`
        
        4. Должен получиться вот такой конфиг
        ```
        server {
            server_name nabot.ru;

            location / {
                include proxy_params;
                proxy_pass http://0.0.0.0:8080/;
            }

            listen 443 ssl; # managed by Certbot
            ssl_certificate /etc/letsencrypt/live/nabot.ru/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/nabot.ru/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        }

        server {
            if ($host = nabot.ru) {
                return 301 https://$host$request_uri;
            } # managed by Certbot


            listen 80;
            server_name nabot.ru;
            return 404; # managed by Certbot


        }
        ```
        
        5. Осталось только перезапустить сервис nginx: `sudo systemctl restart nginx`

5. Запуск django бекенда

    1. Идем в папку проекта и выполняем, сайт должен открыться
        ```
            python3 -m venv env
            source env/bin/activate
            pip install -r requirements.txt
            python manage.py runserver 0.0.0.0:8080
        ```

    2. Создаем systemd команду
        1. `cd /etc/systemd/system/`
        2. `nano server.service`
        3. Полулжить туда надо что-то вроде этого
        ```
        [Unit]
        Description=My test service
        After=multi-user.target

        [Service]
        Type=simple
        Restart=always
        ExecStart=/root/template-django/env/bin/python /root/template-django/manage.py runserver 0.0.0.0:8080

        [Install]
        WantedBy=multi-user.target
        ```
        3. `systemctl daemon-reload`
        4. `systemctl start server.service`

