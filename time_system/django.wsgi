#!/usr/bin/env python

import os
import re
import sys

# Activate your virtual env
activate_env=os.path.expanduser("/home/visgence_apps/app_env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# in order to run more than one instance on an Apache server, we
# need to figure out our path dynamically
program_path = os.path.realpath(__file__)
APP_PATH = re.sub('django.wsgi$','',program_path);
sys.path.append(APP_PATH)

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
