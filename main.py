from http.server import HTTPServer, BaseHTTPRequestHandler

import utils


class App:
    """
    Our application app. Whole idea based on python flask framework.

    We have http request handler inside and routes decorator. Handler
    holds reference to app object, so it could routes incoming requests,
    """
    def __init__(self):
        self.routes = {}

    def get_request_handler(self, request, client_address, server):
        # move reference to the app here
        return App.RequestHandler(request, client_address, server, self)

    def route(self, path):
        """
        Just save URL path and action in dictionary.
        """
        def decor(f):
            self.routes[path] = f
            return f

        return decor

    def run(self, addr="localhost", port=8000):
        server_address = (addr, port)
        httpd = HTTPServer(server_address, self.get_request_handler)

        print(f"Starting httpd server on {addr}:{port}")
        httpd.serve_forever()

    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server, _app):
            # for unknown reason it doesn't work if I put _app after super() init
            self._app = _app
            super().__init__(request, client_address, server)

        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            self.wfile.write(self._app.routes[self.path]().encode())


app = App()


@app.route("/")
def index():
    return "index"


@app.route("/notes/")
def notes():
    return "<br/>".join(["Eat", "Drink", "Sleep"])


@app.route("/example/")
def example():
    return utils.render("./example.html")


app.run()
