from ipw import db

class Interested(db.Model):
    __tablename__ = 'interested'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Interested {}>'.format(self.time)

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    name = db.Column(db.String(80), index=False, unique=False, nullable=False)
    who = db.Column(db.String(80), index=False, unique=False, nullable=False)
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
