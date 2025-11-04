# ВК и ТГ бот для тех. поддержки сервиса.

Боты снижают нагрузку на администраторов, отвечая на подготовленные заранее вопросы без участия человека.

Пример работы в ТГ:

![Анимация_ТГбота](https://github.com/GenmaHimmuro/tg_bot_speech_recognition/blob/master/gifs/Анимация_ВКбота.gif)

Пример работы в ВК:

![Анимация_ВКбота](https://github.com/GenmaHimmuro/tg_bot_speech_recognition/blob/master/gifs/Анимация_ТГбота.gif)


## Как установить

Версия [Python  3.9](https://www.python.org/downloads/release/python-3925)

Создаем виртуальное окружение командой:
```
python -m venv .venv
```
Активируем его:
```
.venv\Scripts\activate.bat
```
Устанавливаем зависимости:
```
pip install -r requirements.txt
```

Далее добавьте в папку с проектом файл `.env` и скопируйте туда следующий код:

```
TG_BOT_TOKEN=
DIALOG_FLOW_PROJECT_ID=
VK_BOT_TOKEN=
ADMIN_CHAT_ID_TG=
```

`VK_BOT_TOKEN` - необходимо получить на сайте [ВК](https://vk.com/) во вкладке API в настройках созданной группы. 

`TG_BOT_TOKEN` - необходимо получить у FatherBot.

`DIALOG_FLOW_PROJECT_ID` - id проекта, дается при создании [агента](https://dialogflow.cloud.google.com).

`ADMIN_CHAT_ID_TG` - id чата админа, куда будут поступать уведомления об сбоях в работе ботов.

### Настройка Google Cloud CLI
- Установить [Google Cloud CLI](https://cloud.google.com/sdk/docs/install). 
- Включить [API DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup#api). 
- Получить [файл с ключами](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk) от вашего Google-аккаунта. 
- Создать [токен DialogFlow](https://cloud.google.com/docs/authentication/api-keys) командой:

```
gcloud auth application-default login
```

## Как включить
Запуск скрипта осуществляется через консоль. 
Телеграм бот:
```
python speech_rec_tg_bot.py
```
ВКонтакте бот:
```
python speech_rec_vk_bot.py
```

Телеграм бот отвечает на каждое сообщение пользователя, а вк, только на те, на которые он обучен. Обучение ботов осуществляется командой в cmd:
```
python create_intent.py --file 'название json-файла'.json
```

### Пример json файла для создания интентов
```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
}
```
