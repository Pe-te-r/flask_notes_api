from app.database import db
from uuid import uuid4

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.UUID,primary_key=True,default=uuid4)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    notes = db.relationship('Notes',back_populates='user',uselist=False,lazy=True)

    
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
    
    @classmethod
    def create_user(cls,session,first_name,last_name,email):
        new_user = cls(first_name=first_name,last_name=last_name,email=email)
        session.add(new_user)
        session.commit()
        session.remove()
        return new_user

    def to_json(self):
        return {'email': self.email,'first_name': self.first_name,'last_name': self.last_name}



class Notes(db.Model):
    id = db.Column(db.UUID,primary_key=True,default=uuid4)
    user_id = db.Column(db.UUID, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text,nullable=False)

    user = db.Relationship('User',back_populates='notes',lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.note}>'
    
