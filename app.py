import os
import flask
import flask_socketio 
import requests
from flask_socketio import emit

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
import models

def dbMsgQuery(dbarray):
    data = models.Message.query.all()
    for row in data: 
        dbarray.append({'img': row.img, 'user': row.user, 'message_text': row.text})
        
def dbUsrQuery(dbarray):
    data = models.UserList.query.all()
    for row in data: 
        dbarray.append({'img': row.img, 'user': row.user})

@app.route('/')
def hello():
    return flask.render_template('index.html')

user_info = []
@socketio.on('initial connect')
def on_initial_connect():
    allmsgs = []
    dbMsgQuery(allmsgs)
    socketio.emit('initial setup', {'messages': allmsgs})
    
@socketio.on('connect')
def on_connect():
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'

all_users = []
@socketio.on('new user')
def on_new_user(data):
    all_users = []
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])
    json = response.json()
    print "Got new user:", json['name']
    user_info = models.UserList(json['picture']['data']['url'], json['name'])
    models.db.session.add(user_info)
    models.db.session.commit()
    models.db.session.close()
    dbUsrQuery(all_users)
    socketio.emit('all users', {
        'users': all_users
    })
    

@socketio.on('new message')
def on_new_message(msg):
    newmsgs = []
    print "Got a new message:", msg
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + msg['facebook_user_token'])
    json = response.json()
    msg_info = models.Message(json['picture']['data']['url'], json['name'], msg['message'][0]['message_text'])
    models.db.session.add(msg_info)
    models.db.session.commit()
    models.db.session.close()
    #return_msg = {'img': json['picture']['data']['url'], 'user': json['name'], 'message_text': msg['message'][0]['message_text']}
    dbMsgQuery(newmsgs)
    # socketio.emit('all messages', {
    #     'messages': return_msg
    # }, broadcast=True)
    socketio.emit('new messages', {
        'messages': newmsgs
    }, broadcast=True)
    
    
if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

