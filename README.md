<h2>Task Manager | (Test task)</h2>



<h2>Подготовка места установки</h2>
<p>mkdir taskmanager && cd taskmanager</p>
<p>python -m venv venv</p>
<p>source venv/bin/activate</p>
<p>git clone this repo ...</p>

<h2>Установка зависимостей проекта</h2>
<p>pip install -r requirements.txt</p>

<h2>Заполните конфигурационны файл config.ini</h2>
<p>password = ваш sudo пароль без кавычек</p>
<p>[smtp] заполните своей информацией</p>
<p>После заполнения [smtp] раскоментируйте строки # 65 и 71 файла handler.py</p>

<h2>(вариант 1) Если работать с локальной базой данных( не докер!)</h2>
<p>Выполните команду: python create_db_local.py</p>
<p>Создайте таблицу моделей: python models.py</p>

<h2>(вариант 2) Если работать с Docker image Postgtres</h2>
<p>Остановите локальный postgresql: sudo systemctl stop postgresql</p>
<p>Запуск docker контейнера с postgresql: docker-compose up -d --build</p>
<p>Созздайте таблицу моделей: python models.py</p>



<h2>Собственно работа</h2>
<p>В одном окне терминала: Запустите: python handler.py</p>
<p>handler должен работать всегда как сервер!</p>

<h3>В другом окне терминала: Работайте из командной строки консоли</h3>
<p>python client.py insert "ls -la" --date "2022-02-16 16:07"</p>
<p>python client.py info-next --number 6</p>
<p>python client.py info-last --number 3</p>
<h3>Для назначения команды с правом sudo</h3>
<p>pyton client.py insert "sudo -S apt-get update" --date "2022-02-16 16:27"</p>

<h3>Help по коммандам</h3>
<p>python client.py --help</p>
<p>python client.py insert --help</p>
<p>python client.py info-next --help</p>
<p>python client.py info-last --help></p>


