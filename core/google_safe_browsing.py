from typing import Tuple, Dict
import requests
import json
import logging
from typing import List

logger = logging.getLogger()


class GoogleSafeBrowsing:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key={}".format(self.api_key)
        self.headers = {"Content-Type": "application/json"}
        self.request_template = {'client': {'clientId': 'pck3tSec', 'clientVersion': '0.1'},
                                'threatInfo': {'platformTypes': ['ANY_PLATFORM'],
                                                'threatEntries': [],
                                                'threatEntryTypes': ['URL'],
                                                'threatTypes': ['MALWARE']}}

    def _prepare_threat_entries(self, urls: list):
        return [{'url': x} for x in urls]

    def api_call(self, urls: List[str]) -> Tuple[bool, Dict]:
        logger.info("api call to google for host {}".format(urls))
        self.request_template['threatInfo']['threatEntries'] = self._prepare_threat_entries(urls)
        response = requests.post(self.url, json=self.request_template, headers=self.headers)
        if response.status_code != 200:
            msg = "request failed for {}".format(urls)
            logger.error(msg)
            raise requests.HTTPError(msg)
        details = json.loads(response.text)
        return not bool(details), details


if __name__ == '__main__':
    google_safe = GoogleSafeBrowsing("AIzaSyDyYREKVRoPgXSFvcRZuqFGZHlSFymDa80")
    r = google_safe.api_call(["testsafebrowsing.appspot.com/s/malware.html"])
    print(r)
