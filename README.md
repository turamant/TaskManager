<h2>Task Manager | v.001</h2>
<ul>Linux Operating System Command Manager:
 <li>Create a task for execution (console command and
schedule are passed as a parameter)</li>
  <li>Get information on the last completed tasks (the number of tasks
is passed as a parameter) containing information about:
    <ul>
      <li>Start date of execution</li>
      <li>Completion date of execution</li>          
      <li>Console command output</li>
    </ul>
    <li> To receive information about the nearest commands for execution (the number of tasks is transmitted as a parameter) containing information about:</li>
    <ul>
        <li>Console command</li>
        <li>Date of the next launch</li>
    </ul>
    <li> When performing a task to the email specified in the application settings
an email is sent with the result of executing the console command</li>
</ul>

<p>(c) Askvart</p>


<h2>Preparing the installation location on the local computer</h2>
<p>mkdir taskmanager && cd taskmanager</p>
<p>python -m venv venv</p>
<p>source venv/bin/activate</p>
<p>git clone this repo ...</p>

<h2>Installing project dependencies</h2>
<p>pip install -r requirements.txt</p>

<h2>Create file .env and fill in the configuration</h2>
<p>SECRET_KEY = your sudo password without quotes</p>

<h3>if you want to send an e-mail, then fill in the file .env</h3>
<p>SERVER = your smtp.server</p>
<p>FROM_ADDR = your programm@domain.com</p>
<p>SUBJECT = HEAD mail test task-manager</p>
<p>TO_ADDR = your@mail.com</p>
<h3>if you don't need to send emails, then don't fill out </h3>


<h2>(option 1) If you work with a local database (not docker!)</h2>
<p>Run the command: python create_db_local.py</p>
<p>Create a Model table: python models.py</p>

<h2>(option 2) If you work with Docker image Postgres</h2>
<ul>Create file .env.db and fill in the configuration for exaple:
<li>POSTGRESQL_USERNAME=postgres</li>
<li>POSTGRESQL_PASSWORD=postgres</li>
<li>POSTGRESQL_DATABASE=task1</li>
<li>ALLOW_EMPTY_PASSWORD=yes</li>
</ul>
<p>Stop it: sudo systemctl stop postgresql</p>
<p>Launching a docker container: docker-compose up -d --build</p>
<p>Create a Model table: python models.py</p>


<h2>The actual work</h2>
<p>In one terminal window run: python handler.py</p>
<p>handler should always work as a server!</p>
<h3>In another terminal window - work from the console command line</h3>
<p>python client.py insert "ls -la" --date "2022-02-16 16:07"</p>
<p>python client.py info-next --number 6</p>
<p>python client.py info-last --number 3</p>
<p>python client.py delete-incorrect-task</p>
<h3>To assign a command with the sudo</h3>
<p>pyton client.py insert "sudo -S apt-get update" --date "2022-02-16 16:27"</p>

<h3>Help by commands</h3>
<p>python client.py --help</p>
<p>python client.py insert --help</p>
<p>python client.py info-next --help</p>
<p>python client.py info-last --help</p>


