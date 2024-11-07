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
    def create_user(cls,first_name,last_name,email):
        new_user = cls(first_name=first_name,last_name=last_name,email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @classmethod
    def get_by_email(cls,email):
        user = cls.query.filter(cls.email==email).first()
        return user
    

    def to_json(self):
        return {'email': self.email,'first_name': self.first_name,'last_name': self.last_name}

    @classmethod
    def get_by_id(cls,id):
        user = cls.query.filter(cls.id==id).first()
        return user

    @classmethod
    def delete_user(cls,user_id):
        user = cls.get_by_id(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
        



class Notes(db.Model):
    id = db.Column(db.UUID,primary_key=True,default=uuid4)
    user_id = db.Column(db.UUID, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text,nullable=False)

    user = db.Relationship('User',back_populates='notes',lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.note}>'
    
