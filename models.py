import flask_sqlalchemy, app


app.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chatapp:chatapp@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app.app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30))
    text = db.Column(db.String(200))
    
    def __init__ (self, u, t):
        self.user = u
        self.text = t
        
    def __repr__(self):
        return '<%u: Message text: %s>' % self.user, self.text
