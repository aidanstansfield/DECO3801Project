from ipw import db

class Interested(db.Model):
    __tablename__ = 'interested'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Interested {}>'.format(self.time)