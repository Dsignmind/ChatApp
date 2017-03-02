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
        


if __name__ == '__main__':
    unittest.main()