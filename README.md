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

#### Установка Docker

Подробное описание процесса установки Docker можно найти в [официальной документации](https://docs.docker.com/engine/install/ubuntu/):

1. Создаем репозиторий

  1.1. Обновим apt и установим приложения для работы apt через HTTPS

```
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

```
  1.2 Добавляем ключи:

```
 sudo install -m 0755 -d /etc/apt/keyrings

 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

 sudo chmod a+r /etc/apt/keyrings/docker.gpg
 
```
  1.3 Настраиваем репозиторий

```
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

2. Устанавливаем Docker 
```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
При возникновении ошибки package docker-ce has no installation candidate можно попробовать команды [отсюда](https://askubuntu.com/questions/1030179/package-docker-ce-has-no-installation-candidate-in-18-04)

```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
sudo apt update
sudo apt install docker-ce
```

Или установить Docker  с помощью 
```
sudo snap install docker
```
#### Настройка Docker

Информацию о постустановочной настройке Docker можно найти [здесь](https://docs.docker.com/engine/install/linux-postinstall/)

Предоставим Docker права для запуска приложений:
1. Создадим новую группу

```
sudo groupadd docker
```

2. Добавим своего пользователя в группу:
```
sudo usermod -aG docker $USER

```

Перезапустим терминал и попробуем запустить команду ниже:

```
docker run hello-world
```
Если ошибок нет, то мы увидим сообщение:

![hello](https://github.com/atskayasatana/Images/blob/3a6d178cd48851dc0221b744e71bc536f368c393/docker%20hello-world.png)


Если появляется ошибка авторизации, то можно попробовать команду ниже:
```
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
```
#### Скачивание и запуск

Образ приложения лежит в DockerHub https://hub.docker.com/repository/docker/atskayasatana/notifications_bot/general

Загрузить его к себе можно командой docker pull
```
docker pull atskayasatana/notifications_bot
```
Образ можно переименовать в любое удобное для пользователя имя:

```
docker tag atskayasatana/notifications_bot <новое имя>
```

Для запуска на стороне пользователя нужен также файл с переменными окружения, где указаны следующие переменные:

 ```
TELEGRAM_BOT_TOKEN= #персональный токен для бота
DEVMAN_API_TOKEN=#токен для платформы
TELEGRAM_CHAT_ID=#id чата, куда будут отправляться уведомления о проверке
```

Запустить образ можно командой ниже
```
docker run --env-file path/to/.env <имя образа>
```














