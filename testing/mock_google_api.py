import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger()


class GoogleSBMock(BaseHTTPRequestHandler):
    post_count = 0

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write('<html>empty</html>'.encode(encoding='utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        js = json.loads(post_data)
        print(f"js {js}")
        threat_url = js['threatInfo']['threatEntries'][0]['url']
        print(f"threat url {threat_url}")
        print(f"req line {self.requestline}")
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        if threat_url == "localhost" and GoogleSBMock.post_count < 1:
            GoogleSBMock.post_count += 1
            self.wfile.write('{"matches":[{"threatType": "MALWARE", "platformType": "ANY_PLATFORM", "threat": {"url": "localhost/some-test-threat-ci"}, "cacheDuration": "300s", "threatEntryType": "URL"}]}'.encode(encoding='utf-8'))
        else:
            self.wfile.write('{}'.encode('utf-8'))



def run(server_class=HTTPServer, handler_class=GoogleSBMock):
    server_address = ('', 8123)
    httpd = server_class(server_address, handler_class)
    logger.info("starting mock http server")
    httpd.serve_forever()


if __name__ == '__main__':
    print('!!!! SERVER !!!!')
    run()
