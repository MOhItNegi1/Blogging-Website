from extension import db




class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    
    email = db.Column(db.String(120))
    phone_no = db.Column(db.String(20))
    bio = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('profile', uselist=False))