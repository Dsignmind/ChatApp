import app
import urllib2
from flask import Flask
import flask_testing
import requests
import unittest

class ServerIntegrationTest(flask_testing.LiveServerTestCase):
    def create_app(self):
        return app.app

    def test_root_url(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEquals(response.code, 200)
        
class MyTest(flask_testing.TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

if __name__ == '__main__':
    unittest.main()