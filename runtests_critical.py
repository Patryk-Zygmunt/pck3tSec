#!/usr/bin/env python

import argparse
from runcore import config_paths
config_paths()

from core.django_external_setup import django_external_setup
from testing import critical


def main(iface):
    django_external_setup()
    threat_test = critical.HostThreatTest(iface)
    try:
        threat_test.perform_test()
    except KeyboardInterrupt:
        threat_test.stop_app_threat()
    finally:
        threat_test.stop_app_threat()



if __name__ == '__main__':
    # TODO add file logger
    parser = argparse.ArgumentParser()
    parser.add_argument('interface')
    args = parser.parse_args()
    main(args.interface)
