import flask_sqlalchemy, app, os


app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chatapp:chatapp@localhost/chatdb'
db = flask_sqlalchemy.SQLAlchemy(app.app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100))
    user = db.Column(db.String(30))
    text = db.Column(db.String(200))
    
    def __init__ (self, i, u, t):
        self.img = i
        self.user = u
        self.text = t
        
    def __repr__(self):
        return '<%i %u: Message text: %s>' % self.img, self.user, self.text
