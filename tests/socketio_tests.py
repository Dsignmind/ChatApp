import unittest
import sys
sys.path.append('..')
from project2 import app

class SocketIOTests(unittest.TestCase):
    def test_on_connect(self):
        client = app.socketio.test_client(app.app)
        response = client.get_received()
        server_msg = response[0]
        self.assertEquals(server_msg['name'], 'server test')
        data = server_msg['args'][0]
        self.assertEquals(data['message'], 'Server responding!')
        
    def test_on_initial_setup(self):
        client = app.socketio.test_client(app.app)
        client.emit('test initial connect')
        response = client.get_received()
        server_msg = response[1]
        self.assertEquals(server_msg['name'], 'initial setup test')
        data = server_msg['args'][0]
        self.assertEquals(data['message'], 'Succesful initial connect')

    def test_emit(self):
        client = app.socketio.test_client(app.app)
        client.emit('test message', {
            'message': 'This is my client test message'
        })
        response = client.get_received()
        result = response[1]
        self.assertEquals(result['name'], 'server sends test data back')
        self.assertEquals(result['args'][0]['from server']['message'], 'This is my client test message')
        
    def test_user_add(self):
        client = app.socketio.test_client(app.app)
        user_info = {'sesh_id': '1234', 'img': '1234', 'name': 'test_user'}
        client.emit('test new user', {
            'user_info': user_info
        })
        response = client.get_received()
        result = response[1]
        self.assertEquals(result['name'], 'server sent test user data')
        #self.assertEquals(result['args'][0]['users'][0][0], '1234 1234 test_user')
        
    def test_user_del(self):
        client = app.socketio.test_client(app.app)
        user_info = {'sesh_id': '1234', 'img': '1234', 'name': 'test_user'}
        client.emit('test del user', {
            'user_info': user_info
        })
        response = client.get_received()
        result = response[1]
        self.assertEquals(result['name'], 'server sent test user data')
        self.assertEquals(result['args'][0]['users'], 'deleted test user')

if __name__ == '__main__':
    unittest.main()