#! /usr/bin//env python

import sys
import os
import logging
import argparse

def config_paths():
    cwd = os.path.dirname(os.path.abspath(__file__))
    api_path = os.path.join(cwd, 'api')
    sys.path.append(api_path)


config_paths()
from core.django_external_setup import django_external_setup
django_external_setup()

from core.stat_analyzer import StatAnalyzer
from core.analyze_dispatcher import AnalyzeDispatcher
from core.google_safe_browsing import GoogleSafeBrowsing
from core.host_analyzer import HostAnalyzer
from core.packet_reader import PacketReader
from core.threat_observer import ThreatObserver
from api.settings import LOGGING

logger = logging.getLogger()


def prepare_app(interface):
    django_external_setup()
    logging.config.dictConfig(LOGGING)
    # threat analyzer
    google_safe = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
    host_analyzer = HostAnalyzer(google_safe)
    threat_observer = ThreatObserver()
    host_analyzer.register_observer(threat_observer)

    # stat analyzer
    stat_analyzer = StatAnalyzer()

    # rest
    reader = PacketReader(interface)
    dispatcher = AnalyzeDispatcher(reader)
    dispatcher.register_analyzer(host_analyzer)
    dispatcher.register_analyzer(stat_analyzer)
    return dispatcher


def main(interface):
    dispatcher = prepare_app(interface)
    try:
        dispatcher.run()
    except KeyboardInterrupt:
        logger.info("stopping app")
    except Exception:
        logger.exception("app failed")
    finally:
        dispatcher.finish()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('interface', help='interface to sniff on')
    parser.add_argument('--log-debug', action='store_true')
    print("Warinig! this script needs root privileges")
    args = parser.parse_args()
    if args.log_debug:
        LOGGING['root']['level'] = 'DEBUG'
    main(args.interface)
