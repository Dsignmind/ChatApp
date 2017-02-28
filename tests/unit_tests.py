import unittest
import sys
sys.path.append('../')

import app
import models
import os


class ChatbotResponseTest(unittest.TestCase):
    def test_about_command(self):
        response = app.check_for_bot('!! about')
        self.assertEqual('Welcome to the HelloHello Chat App! I\'m here if you need me!', response)

    def test_unknown_command(self):
        response = app.check_for_bot('!! why')
        self.assertEqual('I don\'t know what you said! Try "!! help" for available commands.', response)
        
    def test_help_command(self):
        response = app.check_for_bot('!! help')
        self.assertEqual('The commands I understand begin with !! followed by: say, help, about, what time is it?, what\'s up bot?', response)

    def test_say_command(self):
        response = app.check_for_bot('!! say this is a test')
        self.assertEqual('this is a test', response)
        
    def test_empty_command(self):
        response = app.check_for_bot('!! ')
        self.assertEqual('Try \'!! help\' for available commands.', response)
        
class DatabaseTest(unittest.TestCase):
    dbArray = []
    def test_message_query(self):
        dbArray = []
        response = app.dbMsgQuery(dbArray)
        self.assertEqual(dbArray, response)
        
    def test_userlist_query(self):
        dbArray = []
        response = app.dbUsrQuery(dbArray)
        self.assertEqual(dbArray, response)
        
class FilePathTest(unittest.TestCase):
    def test_index(self):
        response = os.path.isfile('./templates/index.html')
        self.assertEqual(True, response)
        
    def test_bot_img(self):
        response = os.path.isfile('./static/img/bot.png')
        self.assertEqual(True, response)
        
    def test_scriptjs_exists(self):
        response = os.path.isfile('./static/script.js')
        self.assertEqual(True, response)
        
    def test_wepack_exists(self):
        response = os.path.isfile('./webpack.config.js')
        self.assertEqual(True, response)
        
if __name__ == '__main__':
    unittest.main()