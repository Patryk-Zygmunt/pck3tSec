import django
import os
import logging
from django.conf import settings
from api import settings as appsettings

logger = logging.getLogger()

"""
Use this module when you need to set up django for external modul/ app to use ORM for example
"""


def django_external_setup():
    """
    Setup django to use django ORM external to django app itself
    """
    if not check_django_set():
        logger.info("setting up django externally")
        settings.configure(default_settings=appsettings, DEBUG=True)
        django.setup(set_prefix=False)
        os.environ['DJANGO_SET'] = str(True)
    else:
        logger.info('django already set')


def check_django_set() -> bool:
    try:
        value = os.environ['DJANGO_SET']
        return True if value == str(True) else False
    except KeyError:
        return False


if __name__ == '__main__':
    django_external_setup()
