# Starknet-delegator

### Settings

Смотри data/settings.json file

~~~json
"RPC": {
    "starknet"  : ["https://starknet-mainnet.public.blastapi.io/rpc/v0_6"] //Какую ноду использовать
},


"useProxies": false, // использовать ли прокси
"amount": 30, // сколько strk врапать
"lock": true, // врапать ли strk
"delegate": true, // делегировать ли стрк
"ErrorSleepeng": [2, 3], // задержка при ошибках
"ThreadRunnerSleep": [2, 3], // задержка перед запуском кошельков
"RetriesLimit": 4, // ретраи при ошибках
"Provider": "argent", // провайдер кошелька
"MaxFee": 1, // не трогать
"========= END =========": ""

~~~

Чтобы начать работу:
 - Загрузи приватники в файл secrets.txt
 - Настрой
 - запусти main.py

### How to run script
1. Устанавливаем Python: https://www.python.org/downloads/, я использую версию 3.9.8
2. При установке ставим галочку на PATH при установке

>![ScreenShot](https://img2.teletype.in/files/19/03/19032fbe-1912-4bf4-aed6-0f304c9bf12e.png)

3. После установки скачиваем бота, переносим все файлы в одну папку (создаете сами, в названии и пути к папке не должно быть кириллицы и пробелов)
4. Запускаем консоль (win+r -> cmd)
5. Пишем в консоль:
cd /d Директория
* Директория - путь к папке, где лежит скрипт (само название скрипта писать не нужно)
7. Запускаем софт:
python main.py

Скрипт запустился.
