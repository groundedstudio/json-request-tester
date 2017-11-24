import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.log import enable_pretty_logging

import logging
import os.path
import pycurl
from io import BytesIO
import requests
import json

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        request_url = self.get_argument("url")
        request_json_string = self.get_argument("json")
        request_method = self.get_argument("method-select")
        if request_method == "GET":
            # Do get request to url and print response
            try:
                r = requests.get(request_url)
                try:
                    response_body = r.json()
                    self.render("response.html", response = response_body, original_url = request_url, original_json = request_json_string, errors = None)
                except ValueError as e:
                    self.render("response.html", response = r, original_url = request_url, original_json = request_json_string, errors = "Response body was not in JSON")
            except Exception as e:
                self.render("response.html", response = "", original_url = request_url, original_json = request_json_string, errors = "URL not formatted properly")
        elif request_method == "POST":
            # Do post request and print response
            try:
                request_json = json.loads(request_json_string)
                try:
                    r = requests.post(request_url, json = request_json)
                    try:
                        response_body = r.json()
                        self.render("response.html", response = response_body, original_url = request_url, original_json = request_json_string, errors = None)
                    except ValueError as e:
                        self.render("response.html", response = r, original_url = request_url, original_json = request_json_string, errors = "Response body was not in JSON")
                except Exception as e:
                    self.render("response.html", response = "", original_url = request_url, original_json = request_json_string, errors = "URL not formatted properly")
            except Exception as e:
                self.render("response.html", response = r, original_url = request_url, original_json = request_json_string, errors = "JSON was not correctly fomatted")

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
