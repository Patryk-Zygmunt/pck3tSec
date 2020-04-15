import django
from django.conf import settings
from api.api import settings as appsettings


def django_external_setup():
    """
    Setup django to use django ORM external to django app itself
    """
    settings.configure(default_settings=appsettings, DEBUG=True)
    django.setup(set_prefix=False)


if __name__ == '__main__':
    django_external_setup()
    # Now this script or any imported module can use any part of Django it needs.
    from api.rest.models import BlackListItem

    i = BlackListItem(id=1, host="123")
    x = BlackListItem.objects.all()
    print(x)