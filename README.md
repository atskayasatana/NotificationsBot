# Уведомления о проверке работ в Телеграмм

 Данный скрипт предназначен для отправки уведомлений о результатах проверки работы студента на платформе https://dvmn.org/
 
 ## Запуск
 
 Для работы понадобится Python3 и библиотеки из файла requirements.txt.
 Архив с проектом нужно скачать к себе на компьютер и распаковать в любую удобную директорию.
 
 Создать бота и получить токен к нему можно здесь:
 https://t.me/BotFather
 
 Отец ботов попросит ввести два имени. 
 Первое — как он будет отображаться в списке контактов, можно написать на русском. 
 Второе — имя, по которому бота можно будет найти в поиске. Должно быть английском и заканчиваться на bot (например, notification_bot)
 
 В работе используются данные, которые не должны быть доступны другим пользователям - персональные токены бота и платформы Девман.
 
 Поэтому, для работы в директорию проекта нужно будет сохранить .env файл с переменными:
 ```
TELEGRAM_BOT_TOKEN= #персональный токен для бота
DEVMAN_API_TOKEN=#токен для платформы
TELEGRAM_CHAT_ID=#id чата, куда будут отправляться уведомления о проверке
```
Запускаем командную строку и переходим в директорию проекта.

Устанавливаем зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
При запуске проекта обязательно нужно указать свой user_id в Телеграм, куда будут приходить уведомления о проверках.

```
python main.py [chat_id]
```
## Запуск на сервере

Для запуска серверной версии необходимо зайти на 81.163.28.229

<pre><font color="#729FCF"><b>~</b></font>$ ssh root@81.163.28.229</pre>

Репозиторий находится в папке opt:
<pre># cd /opt/NotificationsBot
</pre>

В файле .env устанавливаются необходимые значения токенов и id_chat. 

Юнит с настройками можно найти здесь:
<pre>cd /etc/systemd/system/
</pre>

Файл NotificationBot.service

Бот запускается командой 
<pre>systemctl start NotificationBot</pre>

## Запуск с помощью Docker 

Бот упакован в docker контейнер и также может быть запущен с помощью Docker. 
Установка Docker для Linux осуществляется с помощью команд ниже:

```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
sudo apt update
sudo apt install docker-ce
```
Предоставим Docker права для запуска приложений
```
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
```
Образ приложения лежит в DockerHub https://hub.docker.com/r/atskayasatana/notification_bot_deploy

Загрузить его к себе можно командой docker pull
```
docker pull atskayasatana/notification_bot_deploy
```
Запустить образ можно командой
```
docker run notification_bot_deploy
```














