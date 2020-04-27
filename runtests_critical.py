import sys
from runcore import config_paths
from core import abstracts
import argparse

config_paths()


from core.django_external_setup import django_external_setup
from testing import critical




def main(is_ci):
    django_external_setup()
    threat_test = critical.HostThreatTest(is_ci=is_ci)
    try:
        threat_test.perform_test()
    finally:
        threat_test.stop_app_threat()



if __name__ == '__main__':
    # TODO add file logger
    parser = argparse.ArgumentParser()
    parser.add_argument("--ci", default=False, action='store_true')
    args = parser.parse_args()
    main(args.ci)
