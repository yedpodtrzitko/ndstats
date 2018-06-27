import os
import sys

from ndbattle import __versionstr__
from ndbattle.settings.base import *

# server-specific settings
settings_path = os.environ.get('SERVER_SETTINGS_PATH', False)
if settings_path:
    sys.path.insert(0, settings_path)
    try:
        from prod import *
    finally:
        del sys.path[0]

# finally local settings overides all
# overrides anything
try:
    from ndbattle.settings.local import *
except ImportError:
    pass

# append package version to STATIC_URL to invalidate old statics
VERSION_STAMP = __versionstr__.replace(".", "")
STATIC_URL = '%sversion%s/' % (STATIC_URL, VERSION_STAMP)

# try to bump cache version by project version
try:
    CACHES['default']['VERSION'] = VERSION_STAMP
except KeyError:
    pass
