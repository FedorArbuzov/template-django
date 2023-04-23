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
2. Запустить ./ngrok http 8000 скопировать урл
3. Взять токен и урл и положить в /env/bin/activate
   ```
   TOKEN="6273372078:AAF8dC4SEhmaK1sJpQiSFEkNd00mGt-L_ew"
   export TOKEN
   HOST="https://6a45-185-172-136-20.ngrok-free.app"
   export HOST
   ```
4. Запустить сервис в vs code и написать своему боту /start
5. Все, у вас локально запущен бот, можно разрабатывать


## Настройка приложения на сервере
