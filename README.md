Instalar Postgresql
------------------------------------------------------
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib


# sudo -i -u postgres
$ createuser aii -d -R -S -P  # use "aii" password
$ createdb dbaii -O aii -E utf8

Instalar virtualenv
------------------------------------------------------

$ sudo pip install virtualenvwrapper
-Si tiene problema debera installar primero pip con:
	$ sudo apt-get install python-pip

$ export WORKON_HOME=$HOME/.virtualenvs
$ export PROJECT_HOME=$HOME/Devel
$ source /usr/local/bin/virtualenvwrapper.sh

-Si cada sesion no funciona workon debera editar el bashrc de la siguiente forma:
	$ sudo gedit .bashrc
	al final del documento incorporar los 3 ultimos comando

Crear virtualenv con pycharm nombrandolo AII luego iniciar terminal
$ workon AII
ir a la carpeta de projecto
(AII)$ sudo pip install -r AIIWeb/requeriments.txt
-En caso de fallo de psycopg2:
	$ sudo apt-get install -y postgis postgresql-9.3-postgis-2.1
	$ sudo apt-get install libpq-dev python-dev
Volver a ejecutar:
(AII)$ sudo pip install -r AIIWeb/requeriments.txt

(AII)$ echo export DJANGO_SETTINGS_MODULE=AIIWeb.settings.dev >> $VIRTUAL_ENV/bin/postactivate
(AII)$ echo unset DJANGO_SETTINGS_MODULE >> $VIRTUAL_ENV/bin/postdeactivate

(AII)$ python manage.py syncdb
(AII)$ python manage.py migrate

