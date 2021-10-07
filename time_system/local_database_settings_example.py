import os

# Custom database settings go here.
DATABASE_HOST = os.getenv('PG_PORT_5432_TCP_ADDR', 'localhost')
DATABASE_PORT = os.getenv('PG_PORT_5432_TCP_PORT', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timeclock',
        'USER': 'timeclock',
        'PASSWORD': 'password',
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}
