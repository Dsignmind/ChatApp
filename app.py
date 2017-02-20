import os
import flask
import flask_socketio
import requests

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
import models

@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('initial_connect')
def on_initial_connect():
    data = models.Message.query.all()
    all_msg = [{'img': x.img, 'user': x.user, 'text': x.text} for x in data]
    socketio.emit('event', all_msg)
    
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
    print msg['message'][0]['message_text']
    user_info = models.Message(msg['message'][0]['img'], msg['message'][0]['user'], msg['message'][0]['message_text'])
    models.db.session.add(user_info)
    models.db.session.commit()
    models.db.session.close()
    all_messages.append(msg['message'][0]['message_text'])
    # socketio.emit('all messages', {
    #     'messages': all_messages
    # })
    return_msg = {'img': msg['message'][0]['img'], 'user': msg['message'][0]['user'], 'message_text': msg['message'][0]['message_text']}
    print return_msg
    socketio.emit('all messages', {
        'messages': return_msg
    }, broadcast=True)
if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

