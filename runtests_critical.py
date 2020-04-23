import sys
from runcore import config_paths
from core import abstracts

config_paths()

print("here")
print(sys.path)
from core.django_external_setup import django_external_setup
from testing import critical


def main():
    django_external_setup()
    threat_test = critical.HostThreatTest()
    try:
        threat_test.perform_test()
    except KeyboardInterrupt:
        threat_test.stop_app_threat()
    finally:
        threat_test.stop_app_threat()



if __name__ == '__main__':
    # TODO add file logger
     main()
