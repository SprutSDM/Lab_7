import asynchat_server
import sys
import os
import argparse


class AsyncWSGIServer(asynchat_server.AsyncServer):
    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


class AsyncWSGIRequestHandler(asynchat_server.AsyncHTTPRequestHandler):
    def get_environ(self):
        env = {}
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = sys.stdin
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        env['REQUEST_METHOD'] = self.method
        env['PATH_INFO'] = self.request_uri
        env['SERVER_NAME'] = args.host
        env['SERVER_PORT'] = str(args.port)
        return env

    def start_response(self, status, response_headers, exc_info=None):
        print(response_headers)
        code, resp_msg = status.split()[:2]
        self.send_response(code, resp_msg)
        for (key, value) in response_headers:
            self.send_header(key, value)
        self.end_headers()

    def handle_request(self):
        env = self.get_environ()
        result = server.get_app()(env, self.start_response)
        self.finish_response(result)

    def finish_response(self, result):
        print(result)
        [body] = result
        print(body)
        self.send(body)
        self.close()

def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default="/")
    parser.add_argument("-app", dest="application", help="application:module")
    return parser.parse_args()

#args = None
if __name__ == '__main__':
    args = parse_args()
    
    module, application = args.application.split(':')
    module = __import__(module)
    application = getattr(module, application)
    server = AsyncWSGIServer(handler=AsyncWSGIRequestHandler)
    server.set_app(application)
    server.serve_forever()    