import os
import sys
import ndbattle

PROJECT = 'ndbattle'


def cli():
    os.environ.setdefault('SERVER_SETTINGS_PATH',
                          '/var/www/%s/config' % PROJECT)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % PROJECT)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


def bump_version():
    v = ndbattle.__version__
    new_version = v[:-1] + (v[-1] + 1, )
    new_version_str = '.'.join(map(str, new_version))
    initfile = os.path.join(os.path.dirname(ndbattle.__file__), '__init__.py')

    with open(initfile, 'r') as ifile:
        print("Reading old package init file...")
        istr = ifile.read()
        istr = istr.replace(str(v), str(new_version))

    with open(initfile, 'w') as ifile:
        print("Writing new init file with version %s..." % new_version_str)
        ifile.write(istr)

    with open('version', 'w') as ifile:
        ifile.write(new_version_str)

main = cli
