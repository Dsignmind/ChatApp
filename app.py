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

user_info = []
allmsgs = []
@socketio.on('initial connect')
def on_initial_connect(data):
   # user_info.append({'user': json['name'], 'img': json['picture']['data']['url']})
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])
    json = response.json()
    data = models.Message.query.all()
    for row in data: 
        allmsgs.append({'img': json['picture']['data']['url'], 'user': row.user, 'text': row.text})
        print row
    
    socketio.emit('initial setup', {'messages': allmsgs, 'userInfo': user_info})
    
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
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + msg['facebook_user_token'])
    json = response.json()
    user_info = models.Message(msg['facebook_user_token'], json['name'], msg['message'][0]['message_text'])
    models.db.session.add(user_info)
    models.db.session.commit()
    models.db.session.close()
    all_messages.append(msg['message'][0]['message_text'])
    return_msg = {'img': json['picture']['data']['url'], 'user': json['name'], 'message_text': msg['message'][0]['message_text']}
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

