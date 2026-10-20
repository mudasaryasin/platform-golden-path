import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError
from app.server import Handler

class ServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health_and_readiness(self):
        for path in ("/healthz", "/readyz"):
            with urlopen(self.url + path) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers['Content-Type'], 'application/json')
                self.assertIn('status', json.load(response))

    def test_unknown_route_is_404(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.url + '/missing')
        self.assertEqual(caught.exception.code, 404)
