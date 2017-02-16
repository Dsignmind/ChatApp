import os
import flask
import flask_socketio

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
import models

@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'

all_numbers = []
@socketio.on('new number')
def on_new_number(data):
    print "Got an event for new number with data:", data
    all_numbers.append(data['number'])
    socketio.emit('all numbers', {
        'numbers': all_numbers
    })
    
all_messages = []
@socketio.on('new message')
def on_new_message(msg):
    print "Got a new message:", msg
    all_messages.append(msg['message'])
    socketio.emit('all messages', {
        'messages': all_messages
    })
if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

