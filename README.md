# WhereToGo Django Project #
## Prerequisites ##

- python >= 2.5
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment ###
Create a virtual python enviroment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv --no-site-packages wheretogo-env
```

#### For virtualenv ####
```bash
virtualenv --no-site-packages wheretogo-env
cd wheretogo-env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone https://vasyabigi@github.com/equeny/wheretogo.git wheretogo
```

### Install requirements ###
```bash
cd wheretogo
pip install -r requirements.txt
```

### Configure project ###
```bash
cp wheretogo/__local_settings.py wheretogo/local_settings.py
vi wheretogo/local_settings.py
```

### Sync database ###
```bash
python manage.py syncdb
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000
