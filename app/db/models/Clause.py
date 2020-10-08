from datetime import datetime

import flask_whooshalchemy

from app import sqldb as db, app

from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy import Table, Column, Integer, ForeignKey
from whoosh.analysis import StemmingAnalyzer

class Clause(db.Model):

    __tablename__= 'clause'
    __searchable__ = ['clause_title', 'clause_text']
    __analyzer__ = StemmingAnalyzer()

    clause_id = db.Column(db.Integer, primary_key=True)
    clause_title = db.Column(db.String(720)) 
    clause_text = db.Column(db.String)
    # combination of title and text for search
    clause_user = db.Column(db.Integer, ForeignKey('user.user_id'))
    clause_private = db.Column(db.Boolean)
    clause_created = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship("User")

    def __init__(self, title, text, user_id, private):
        # ensure title is not longer than 720 characters
        self.clause_title = title[:720]
        self.clause_text = text
        # combine title and text in 'search string'
        self.clause_user = user_id
        self.clause_private = private

    def __repr__(self):
        return self.clause_title