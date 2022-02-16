<h2>Task Manager | (Test task)</h2>

<h2>Подготовка места установки</h2>
<p>mkdir taskmanager && cd taskmanager</p>
<p>python -m venv venv</p>
<p>source venv/bin/activate</p>
<p>git clone this repo ...</p>

<h2>Установка зависимостей проекта</h2>
<p>pip install -r requirements.txt</p>

<h2>Остановите локальный postgresql</h2>
<p>sudo systemctl stop postgresql</p>

<h2>Запуск docker контейнера с postgresql</h2>
<p>docker-compose up -d --build</p>

<h2>Заполните конфигурационны файл config.ini</h2>
<p>password = qqqq1234</p>
<p>[smtp] заполните своей информацией</p>
<p>После заполнения</p>

<h2>Создайте модели(таблицу)<h2>
<p>python models.py</p>

<h2>Запустите handler.py</h2>
<p>python handler.py</p>

<h2>Работайте из командной строки консоли<h2>
<p>python client.py --help</p>
<p>python client.py insert "ls -la" --date "2022-02-16 16:07"</p>
<p>python client.py info-next --number 6</p>
<p>python client.py info-last --number 3</p>

<p></p>