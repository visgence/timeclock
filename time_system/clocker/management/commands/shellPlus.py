import os
import time

from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--ipython', action='store_true', dest='ipython', help='Tells Django to use IPython, not BPython.')
        parser.add_argument('--plain', action='store_true', dest='plain', help='Tells Django to use plain Python, not BPython nor IPython.')
        parser.add_argument('--no-pythonrc', action='store_true', dest='no_pythonrc', help='Tells Django to use plain Python, not IPython.')
        parser.add_argument('--print-sql', action='store_true', default=False, help="Print SQL queries as they're executed")
        parser.add_argument('--dont-load', action='append', dest='dont_load', default=[], help='Ignore autoloading of some apps/models. Can be used several times.')

    help = "Like the 'shell' command but autoloads the models of all installed Django apps."

    requires_model_validation = True

    def handle(self, **options):
        # XXX: (Temporary) workaround for ticket #1796: force early loading of all
        # models from installed apps. (this is fixed by now, but leaving it here
        # for people using 0.96 or older trunk (pre [5919]) versions.
        from django.apps import apps
        # loaded_models = apps.get_models()

        use_ipython = options.get('ipython', False)
        use_plain = options.get('plain', False)
        use_pythonrc = not options.get('no_pythonrc', True)

        if options.get("print_sql", False):
            # Code from http://gist.github.com/118990
            from django.db.backends import util
            try:
                import sqlparse
            except ImportError:
                sqlparse = None

            class PrintQueryWrapper(util.CursorDebugWrapper):
                def execute(self, sql, params=()):
                    starttime = time.time()
                    try:
                        return self.cursor.execute(sql, params)
                    finally:
                        raw_sql = self.db.ops.last_executed_query(self.cursor, sql, params)
                        execution_time = time.time() - starttime
                        if sqlparse:
                            print(sqlparse.format(raw_sql, reindent=True))
                        else:
                            print(raw_sql)
                        print()
                        print('Execution time: %.6fs' % execution_time)
                        print()

            util.CursorDebugWrapper = PrintQueryWrapper

        # Set up a dictionary to serve as the environment for the shell, so
        # that tab completion works on objects that are imported at runtime.
        # See ticket 5082.
        from django.conf import settings
        from django.utils.module_loading import import_module
        imported_objects = {'settings': settings, 'import_module': import_module}

        dont_load_cli = options.get('dont_load')  # optparse will set this to [] if it doensnt exists
        dont_load_conf = getattr(settings, 'SHELL_PLUS_DONT_LOAD', [])
        dont_load = dont_load_cli + dont_load_conf

        # model_aliases = getattr(settings, 'SHELL_PLUS_MODEL_ALIASES', {})
        for app_mod in [import_module(appname) for appname in settings.INSTALLED_APPS]:
            app_models = apps.get_models(app_mod)
            if not app_models:
                continue
            app_name = app_mod.__name__
            if app_name in dont_load:
                continue

            model_labels = []
            for model in app_models:
                alias = model.__name__
                imported_objects[alias] = model
                model_labels.append(model.__name__)

            print(self.style.SQL_COLTYPE("From '%s' autoload: %s" % (app_mod.__name__, ", ".join(model_labels))))

        try:
            if use_plain:
                # Don't bother loading B/IPython, because the user wants plain Python.
                raise ImportError
            try:
                if use_ipython:
                    # User wants IPython
                    raise ImportError
                from bpython import embed
                embed(imported_objects)
            except ImportError:
                try:
                    from IPython import embed
                    embed(user_ns=imported_objects)
                except ImportError:
                    # IPython < 0.11
                    # Explicitly pass an empty list as arguments, because otherwise
                    # IPython would use sys.argv from this script.
                    try:
                        from IPython.Shell import IPShell
                        shell = IPShell(argv=[], user_ns=imported_objects)
                        shell.mainloop()
                    except ImportError:
                        # IPython not found at all, raise ImportError
                        raise
        except ImportError:
            # Using normal Python shell
            import code
            try:
                # Try activating rlcompleter, because it's handy.
                import readline
            except ImportError:
                pass
            else:
                # We don't have to wrap the following import in a 'try', because
                # we already know 'readline' was imported successfully.
                import rlcompleter
                readline.set_completer(rlcompleter.Completer(imported_objects).complete)
                readline.parse_and_bind("tab:complete")

            # We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
            # conventions and get $PYTHONSTARTUP first then import user.
            if use_pythonrc:
                pythonrc = os.environ.get("PYTHONSTARTUP")
                if pythonrc and os.path.isfile(pythonrc):
                    try:
                        exec(compile(open(pythonrc, "rb").read(), pythonrc, 'exec'))
                    except NameError:
                        pass
                # This will import .pythonrc.py as a side-effect
                import user
            code.interact(local=imported_objects)
