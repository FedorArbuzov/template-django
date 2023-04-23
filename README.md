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
