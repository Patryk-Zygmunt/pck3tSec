import django
from django.conf import settings
from api import settings as appsettings


"""
Use this module when you need to set up django for external modul/ app to use ORM for example
"""

def django_external_setup():
    """
    Setup django to use django ORM external to django app itself
    """
    settings.configure(default_settings=appsettings, DEBUG=True)
    django.setup(set_prefix=False)


if __name__ == '__main__':
    django_external_setup()
