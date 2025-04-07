'''
' clocker/management/commands.setup.py
' Contributing Authors:
'    Jeremiah Davis (Visgence, Inc)
'
' (c) 2013 Visgence, Inc., RegionIx Education Cooperative
'''

# System Imports
from django.core.management import call_command
from django.core.management.base import BaseCommand
from settings import ENABLE_JOBS
import logging
logger = logging.getLogger(__name__)


# local imports


class Command(BaseCommand):
    help = 'Runs syncdb, git submodule, and sets up an admin user.'

    def handle(self, *args, **options):

        call_command('migrate', fake=False)

        logger.info("Loading fixtures...")
        fixtures = [
            [
                "clocker/fixtures/employees.json"
            ]
        ]

        if not ENABLE_JOBS:
            logger.info("Adding admin user and default job...")
            fixtures.append([
                    "clocker/fixtures/defaultJob.json"
                ])

        else:
            logger.info('Do you wish to load sample data?')
            user_resp = None
            user_resp = input('(y/n) ')
            while user_resp not in ['y', 'Y', 'n', 'N']:
                logger.info('Sorry, I did not understand your response.  Please enter \'y\' or \'n\'.')
                logger.info('Do you wish to load sample data?')
                user_resp = input('(y/n) ')

            if user_resp in ['y', 'Y']:
                fixtures.append([
                    "clocker/fixtures/jobs.json"
                ])
                fixtures.append([
                    "clocker/fixtures/shifts.json"
                ])
        # Load fixtures
        for apps in fixtures:
            for fixture in apps:
                call_command('loaddata', fixture, verbosity=1)
