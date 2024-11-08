import bcrypt
from uuid import uuid4,UUID
from app.database import db

# user class
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.UUID,primary_key=True,default=uuid4)
    username= db.Column(db.String(255),nullable=False,unique=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    notes = db.relationship('Notes',back_populates='user',uselist=True,lazy=True)
    password = db.relationship('Password',back_populates='user',uselist=False,lazy=True)

    
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
    
    @classmethod
    def create_user(cls,username,first_name,last_name,email,password):
        new_user = cls(username=username,first_name=first_name,last_name=last_name,email=email)
        db.session.add(new_user)
        db.session.commit()
        hashed_password = Password.hash_password(password)
        password_stored = Password.store_password(hashed_password,new_user.id)
        if password_stored:
            db.session.commit()
            return new_user
        db.session.rollback()
        return None
    
    @classmethod
    def get_by_email(cls,email):
        user = cls.query.filter(cls.email==email).first()
        return user
    

    def get_notes(self):
        return self.notes
    def to_json(self):
        # print(self.get_notes())
        print("User's notes:", self.notes)  # Debugging line
        return {'email': self.email,'first_name': self.first_name,'last_name': self.last_name,'notes': [note.to_json() for note in self.notes] if self.notes else []}

    @classmethod
    def get_by_id(cls, user_id):
        if isinstance(user_id, str):
            try:
                user_id = UUID(user_id)
            except ValueError:
                return None 
        return cls.query.filter(cls.id == user_id).first()

    @classmethod
    def delete_user(cls,user_id):
        user = cls.get_by_id(str(id))
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def get_all_users(cls):
        return cls.query.all()

# password
class Password(db.Model):
    __tablename__ = 'password'
    user_id = db.Column(db.UUID,db.ForeignKey('users.id'),nullable=False,primary_key=True)
    password = db.Column(db.String(255), nullable=False)

    user=db.Relationship('User',back_populates='password',lazy=True,uselist=False)

    @classmethod
    def store_password(cls,password,user_id):
        try:
            password = Password(password=password,user_id=user_id)
            db.session.add(password)
            return True
        except Exception:
            return None

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt() 
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password
    @staticmethod
    def verify_password(provided_password,stored_password):
         return bcrypt.checkpw(provided_password.encode(), stored_password)


# Notes class
class Notes(db.Model):
    id = db.Column(db.UUID,primary_key=True,default=uuid4)
    user_id = db.Column(db.UUID, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text,nullable=False)

    user = db.Relationship('User',back_populates='notes',lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.note}>'
    

    @classmethod
    def create_note(cls, user_id, note):
        try:
            user_id = UUID(user_id) 
            note = cls(user_id = user_id, note = note)
        except Exception:
            return False
        print(note)
        db.session.add(note)
        db.session.commit()
        return note

    def owner_email(self):
        return self.user.email
    
    def to_json(self):
        return {
            'id': self.id,
            'user_name': f'{self.user.first_name} {self.user.last_name}' if self.user else None,
            'content': self.note,
        }
    @classmethod
    def get_all_notes(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        if isinstance(id, str):
            try:
                id = UUID(id)
                return cls.query.filter(cls.id == id).first()
            except ValueError:
                return None
        return None
    @classmethod
    def delete_note(cls,note_id):
        note = cls.get_by_id(str(note_id))
        if note:
            db.session.delete(note)
            db.session.commit()
            return True
        return False