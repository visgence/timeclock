'''
' clocker/management/commands/rebuild.py
' Contributing Authors:
'    Jeremiah Davis (Visgnece, Inc.)
'    Bretton Murphy (Visgence, Inc.)
'
' (c) 2013 Visgence, Inc.
'''

# System Imports
import sys
import os

# Django Imports
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        if settings.DATABASES['default']['NAME'].rpartition('/')[2] != 'timeclock.db':
            logger.info('It appears you are using custom database settings.  This command only works for timeclock.db.')
            sys.exit(1)

        logger.info('This command will wipe your database and start fresh.  Are you sure you want to continue?')
        user_resp = None
        user_resp = input('(Y/n) ')
        while user_resp not in ['Y', 'n']:
            logger.info('Did not understand your response.  Please enter \'Y\' or \'n\'.')
            logger.info('This command will wipe your database and start fresh.  Are you sure you want to continue?')
            user_resp = input('(Y/n) ')

        if user_resp == 'n':
            logger.info('Bye!')
            sys.exit(0)

        assert user_resp == 'Y', 'Something Bad Happened!'

        # Make sure to clean up first
        call_command('clean')

        baseDir = os.path.dirname(os.path.abspath(os.sys.modules[settings.SETTINGS_MODULE].__file__))
        try:
            os.remove(baseDir + "/timeclock.db")
        except OSError:
            logger.info('timeclock.db does not exist.  Creating new db.')
        call_command('setup', interactive=True)
