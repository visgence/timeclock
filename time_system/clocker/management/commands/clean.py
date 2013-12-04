"""
" portcullis/management/commands/clean.py
" Contributing Authors:
" Jeremiah Davis (Visgence, Inc.)
"
" (c) 2012 Visgence, Inc., RegionIX Education Cooperative
"""

# django imports
from django.core.management.base import BaseCommand, CommandError

# system imports
import os
import re

class Command(BaseCommand):
    help = 'Removes all .pyc files in all subdirectories.  May do other deployment/cleanup tasks in future.'
    
    def handle(self, *args, **options):
        # Regular expression for .pyc files
        pycRe = re.compile(r'.*\.((pyc$)|(swp$))')
        tree = os.walk(os.getcwd())

        self.stdout.write('Cleaning up .pyc files from directory ' + os.getcwd() + '...\n')
        for root, directories, files in tree:
            if '.git' in directories:
                # Make sure we don't go into repository directories.
                directories.remove('.git')
                
            # remove files that end in .pyc
            for f in files:
                if pycRe.match(f) is not None:
                    filePath = '%s/%s' % (root, f)
                    self.stdout.write('Removing: ' + filePath + '\n')
                    os.remove(filePath)
        self.stdout.write('Done.\n')
