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


# local imports


class Command(BaseCommand):
    help = 'Runs syncdb, git submodule, and sets up an admin user.'

    def handle(self, *args, **options):

        call_command('migrate', fake=False)

        if not ENABLE_JOBS:
            call_command('loaddata', "clocker/fixtures/defaultJob.json", verbosity=1)

        else:
            print("Loading fixtures...")
            fixtures = [
                [
                    "clocker/fixtures/employees.json"
                ]
            ]

            print('Do you wish to load sample data?')
            user_resp = None
            user_resp = input('(y/n) ')
            while user_resp not in ['y', 'Y', 'n', 'N']:
                print('Sorry, I did not understand your response.  Please enter \'y\' or \'n\'.')
                print('Do you wish to load sample data?')
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
