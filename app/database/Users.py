from app.database import db
from uuid import uuid4

class User(db.Model):
    id = db.Column(db.UUID,primary_key=True,default=uuid4())
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    notes = db.relationship('Notes',back_populates='user',uselist=False,lazy=True)

    
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
    
