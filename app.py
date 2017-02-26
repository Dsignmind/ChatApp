import os
import flask
import flask_socketio 
import requests
import random
from datetime import datetime
import flask_socketio

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
import models

#Database queries-----------
def dbMsgQuery(dbarray):
    data = models.Message.query.all()
    for row in data: 
        dbarray.append({'img': row.img, 'user': row.user, 'message_text': row.text})
        
def dbUsrQuery(dbarray):
    data = models.UserList.query.all()
    for row in data: 
        dbarray.append({'img': row.img, 'user': row.user})
        
# Chatbot------------------
all_words = []
bot_say_response = ''

WHATSUP_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]
HELP_RESPONSE = ["The commands I understand begin with !! followed by: say, help, about, what time is it?, what's up bot?"]
ABOUT_RESPONSE = ["Welcome to the HelloHello Chat App! I'm here if you need me!"]
TIME_RESPONSE = "I don't know about where you are but it's " + datetime.now().strftime('%H:%M') + " here."

def check_for_bot(sentence):
    all_words = sentence.split()
    bot_say_response = ''
    #for word in sentence.words:
        #all_words.append(word)
    if not all_words[1]:
        print "bot response: no strings passed!"
        return "Try '!! help' for available commands."
    elif all_words[1] == "what's" and all_words[2] == "up":
        print "bot response: ", random.choice(WHATSUP_RESPONSES)
        return random.choice(WHATSUP_RESPONSES)
    elif all_words[1] == "help":
        print "bot response: ", HELP_RESPONSE
        return HELP_RESPONSE
    elif all_words[1] == "about":
        print "bot response: ", ABOUT_RESPONSE
        return ABOUT_RESPONSE
    elif all_words[1] == "what" and all_words[2] == "time":
        print "bot response: ", TIME_RESPONSE
        return TIME_RESPONSE
    elif all_words[1] == "say":
        print "bot response: ", bot_say_response . join(all_words[2:])
        return bot_say_response . join(all_words[2:])
    else:
        print "bot response: Unknown command"
        return "I don't know what you said! Try '!! help' for available commands."
        
                
        

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
    if msg['message'][0]['message_text'][0:2] == "!!":
        name_to_return = "ChatBot"
        #picture_to_return = "http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/3d-glossy-blue-orbs-icons-business/075873-3d-glossy-blue-orb-icon-business-robot.png"
        picture_to_return = "static/img/bot.png"
        message_to_return = check_for_bot(msg['message'][0]['message_text'])
    else:
        picture_to_return = json['picture']['data']['url']
        name_to_return = json['name']
        message_to_return = msg['message'][0]['message_text']
    # response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token=' + msg['facebook_user_token'])
    # json = response.json()
    msg_info = models.Message(picture_to_return, name_to_return, message_to_return)
    models.db.session.add(msg_info)
    models.db.session.commit()
    models.db.session.close()
    dbMsgQuery(newmsgs)
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

