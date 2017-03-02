import os
import flask
import flask_socketio 
import requests
import random
import urllib3
import string
import json


from datetime import datetime


app = flask.Flask(__name__)
with app.app_context():
    socketio = flask_socketio.SocketIO(app)
    import models

#Database queries-----------
def dbMsgQuery(dbarray):
    data = models.Message.query.all()
    for row in data: 
        dbarray.append({'img': row.img, 'user': row.user, 'message_text': row.text})
    return dbarray
        
def dbUsrQuery(dbarray):
    data = models.UserList.query.all()
    for row in data: 
        dbarray.append({'img': row.img, 'user': row.user})
    return dbarray
        
# Chatbot------------------
all_words = []
bot_say_response = ''

WHATSUP_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]
HELP_RESPONSE = 'The commands I understand begin with !! followed by: say, help, about, what time is it?, what\'s up bot?, what should I wear?'
ABOUT_RESPONSE = 'Welcome to the HelloHello Chat App! I\'m here if you need me!'
TIME_RESPONSE = 'I don\'t know about where you are but it\'s ' + datetime.now().strftime('%H:%M') + ' here.'

def check_for_bot(sentence):
    all_words = sentence.split()
    bot_say_response = ' '
    if len(all_words) == 1:
        print 'bot response: no strings passed!'
        return 'Try \'!! help\' for available commands.'
    elif all_words[1].lower() == "what's" and all_words[2].lower() == "up":
        print 'bot response: ', random.choice(WHATSUP_RESPONSES)
        return random.choice(WHATSUP_RESPONSES)
    elif all_words[1].lower() == "help":
        print 'bot response: ', HELP_RESPONSE
        return HELP_RESPONSE
    elif all_words[1].lower() == "about":
        print 'bot response: ', ABOUT_RESPONSE
        return ABOUT_RESPONSE
    elif all_words[1].lower() == "what" and all_words[2].lower() == "time":
        print 'bot response: ', TIME_RESPONSE
        return TIME_RESPONSE
    elif all_words[1].lower() =="what" and all_words[2].lower() == "should"and all_words[3].lower() == "i":
            return 'I don\'t know I\'m a robot! But the weather report says ' + get_weather()
    elif all_words[1].lower() == "say":
        print 'bot response: ', bot_say_response . join(all_words[2:])
        return bot_say_response.join(all_words[2:])
    else:
        print 'bot response: Unknown command'
        return 'I don\'t know what you said! Try "!! help" for available commands.'
        
#weather api--------------
def get_weather():
    http = urllib3.PoolManager()
    DARK_SKY = os.getenv('DARK_SKY')
    getIP = http.request('GET','http://ip-api.com/json/')
    longitude = json.loads(getIP.data)['lon'] 
    latitude = json.loads(getIP.data)['lat']
    apiURL = 'https://api.darksky.net/forecast/' + DARK_SKY + '/'+ str(latitude) + ',' + str(longitude)
    response = http.urlopen('GET',apiURL)
    response_data = json.loads(response.data)['hourly']['summary']
    return response_data
       

                
        

@app.route('/')
def hello():
    return flask.render_template('index.html')
    
@app.route('/test')
def hello_test():
    return 'Hello, world!'

user_info = []
@socketio.on('initial connect')
def on_initial_connect():
    allmsgs = []
    dbMsgQuery(allmsgs)
    socketio.emit('initial setup', {'messages': allmsgs})
    
    
@socketio.on('connect')
def on_connect():
    print 'Someone connected!'
    socketio.emit('server test', {
        'message': 'Server responding!'
    })

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'
    models.UserList.query.filter_by(sesh_id=flask.request.sid).delete()
    print 'removing id: ', flask.request.sid
    models.db.session.commit()
    models.db.session.close()

session_id = ''
all_users = []
@socketio.on('new user')
def on_new_user(data):
    session_id = flask.request.sid
    all_users = []
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + data['facebook_user_token'])
    json = response.json()
    print "Got new user:", json['name']
    print "session id is: ", session_id
    user_info = models.UserList(session_id, json['picture']['data']['url'], json['name'])
    models.db.session.add(user_info)
    models.db.session.commit()
    models.db.session.close()
    dbUsrQuery(all_users)
    socketio.emit('all users', {
        'users': all_users
    })
    
@socketio.on('delete user')
def on_delete_user():
    print 'Deleting user!'
    models.UserList.query.filter_by(sesh_id=flask.request.sid).delete()
    print 'removing id: ', flask.request.sid
    models.db.session.commit()
    models.db.session.close()
    

@socketio.on('new message')
def on_new_message(msg):
    newmsgs = []
    message_to_return = ""
    picture_to_return = ""
    name_to_return = ""
    print "Got a new message:", msg
    print "session id is: ", flask.request.sid
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + msg['facebook_user_token'])
    json = response.json()
    picture_to_return = json['picture']['data']['url']
    name_to_return = json['name']
    message_to_return = msg['message'][0]['message_text']
    msg_info = models.Message(picture_to_return, name_to_return, message_to_return)
    models.db.session.add(msg_info)
    models.db.session.commit()
    models.db.session.close()
    dbMsgQuery(newmsgs)
    socketio.emit('new messages', {
        'messages': newmsgs
    }, broadcast=True)
    if msg['message'][0]['message_text'][0:2] == "!!":
        newmsgs = []
        name_to_return = "ChatBot"
        picture_to_return = "static/img/bot.png"
        message_to_return = check_for_bot(msg['message'][0]['message_text'])
        msg_info = models.Message(picture_to_return, name_to_return, message_to_return)
        models.db.session.add(msg_info)
        models.db.session.commit()
        models.db.session.close()
        dbMsgQuery(newmsgs)
        socketio.emit('new messages', {
            'messages': newmsgs
        }, broadcast=True)
    
@socketio.on('test message')
def on_new_test_message(data):
    socketio.emit('server sends test data back', {
        'from server': data
    })
    

@socketio.on('test new user')
def on_new_testuser(data):
    test_user = []
    print "Got new test user:", data['user_info']['name']
    print "session id is: ", data['user_info']['sesh_id']
    user_info = models.UserList(data['user_info']['sesh_id'], data['user_info']['img'], data['user_info']['name'])
    models.db.session.add(user_info)
    models.db.session.commit()
    models.db.session.close()
    test_user.append(models.UserList.query.filter_by(sesh_id='1234'))
    print test_user
    socketio.emit('server sent test user data', {
        'users': test_user
    })
    
@socketio.on('test del user')
def on_del_testuser(data):
    test_user = []
    print "Got test user to del:", data['user_info']['name']
    print "session id is: ", data['user_info']['sesh_id']
    #user_info = models.UserList(data['user_info']['sesh_id'], data['user_info']['img'], data['user_info']['name'])
    models.UserList.query.filter_by(sesh_id='1234').delete()
    models.db.session.commit()
    models.db.session.close()
    print test_user
    socketio.emit('server sent test user data', {
        'users': 'deleted test user'
    })
    
@socketio.on('test initial connect')
def on_initial_test_connect():
    allmsgs = []
    dbMsgQuery(allmsgs)
    socketio.emit('initial setup test', {
        'message': 'Succesful initial connect'
    })
    

    
    
if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

