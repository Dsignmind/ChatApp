import flask_sqlalchemy, app, os


app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = flask_sqlalchemy.SQLAlchemy(app.app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(300))
    user = db.Column(db.String(300))
    text = db.Column(db.String(200))
    
    def __init__ (self, i, u, t):
        self.img = i
        self.user = u
        self.text = t
        
    def __repr__(self):
        return '%s %s %s' % (self.img, self.user, self.text)
        
class UserList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sesh_id = db.Column(db.String(300))
    img = db.Column(db.String(300))
    user = db.Column(db.String(300))
    
    def __init__ (self, s, i, u):
        self.sesh_id = s
        self.img = i
        self.user = u
        
    def __repr__(self):
        return '%s %s %s' % (self.sesh_id, self.img, self.user)
