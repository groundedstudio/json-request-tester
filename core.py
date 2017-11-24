import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.log import enable_pretty_logging

import logging
import os.path
import pycurl
from io import BytesIO
import bcrypt
import requests
import json

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        request_url = self.get_argument("url")
        request_json = self.get_argument("json")
        request_method = self.get_argument("method-select")
        if request_method == "GET":
            # Do get request to url and print response
            r = requests.get(request_url)
            try:
                response_body = r.json()
                self.render("response.html", response = response_body, original_url = request_url, original_json = request_json, errors = None)
            except ValueError as e:
                self.render("response.html", response = r, original_url = request_url, original_json = request_json, errors = "Response body was not in JSON")
        elif request_method == "POST":
            # Do post request and print response
            pass
        self.render("response.html", response = "The internet am I right", original_url = request_url, original_json = request_json)

app = tornado.web.Application(
    [(r"/", RootHandler),],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "secret",
    debug = True,
    )

def main():
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8080)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()
