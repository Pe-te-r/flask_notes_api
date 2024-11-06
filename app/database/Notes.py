from app.database import db
from uuid import uuid4

class Notes(db.Model):
    id = db.Column(db.UUID,primary_key=True,default=uuid4())
    user_id = db.Column(db.UUID, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text,nullable=False)

    user = db.Relationship('User',back_populates='notes',lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.note}>'
    
