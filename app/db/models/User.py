from app import sqldb as db

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    user_firstname = db.Column(db.String(250)) 
    user_lastname = db.Column(db.String(250)) 
    user_email = db.Column(db.String(300))

    def __init__(self, first_name, last_name, email):
        self.user_firstname = first_name
        self.user_lastname = last_name
        self.user_email = email

