
It's strongly recommended to use virtualenvwrapper to create a virtualenv with --no-site-packages and install all python dependencies in it:

# aptitude install virtualenvwrapper
$ mkvirtualenv --distribute --no-site-packages AII
$ workon AII
(AII)$ #...
This will avoid possible module overshadowing between packages installed in the system and those required by the project. After activating the fresh virtualenv and installing all requirements, install the python dependencies:

(AII)$ pip install -r conf/requirements.txt
Next execute the following commands, this will make it so doing workon vestidia sets the system to use the correct development settings ((dirrecion donde esta AIIWEB)/settings/dev.py) and automatically cd to vestidia's directory:


(AII)$ echo export DJANGO_SETTINGS_MODULE=(dirrecion donde esta AIIWEB).settings.dev >> $VIRTUAL_ENV/bin/postactivate
(AII)$ echo unset DJANGO_SETTINGS_MODULE >> $VIRTUAL_ENV/bin/postdeactivate
Next check creating the database. After that the project should be ready to go.

Creating the database
----------------------

You should use PostgreSQL (9.1 if possible, package postgresql-9.1 in Ubuntu 11.10 and later). To install it in Debian/Ubuntu either use APT to install the postgresql package or download and compile PostgreSQL from source (install it in /usr/local/ in the latter case).

With the PostgreSQL server running, create the vestidia user and the vestidia database:

# su - postgres
$ createuser AII -d -R -S -P  # use "aii" password
$ createdb AII -O AII -E utf8
After the database and user are in place use Django to create the database schema and load the initial data fixtures:

$ python manage.py syncdb
$ python manage.py migrate
If the Django application has trouble connecting to PostgreSQL (you can run python manage.py dbshell to check it) edit /etc/postgresql/<version>/main/pg_hba.conf and make sure that the authentication method for local connections is md5 (and restart PostgreSQL after making changes to its configuration):

local    all    all    md5
