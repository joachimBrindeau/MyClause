from app import sqldb as db
from ..models.Clause import Clause

from sqlalchemy import or_, and_

class ClauseRepository:

    def __init__(self):
        print('initialized ClauseRepository..')

    def query_clauses(self, query, user_id, private_only):
        
        intermediate_query = Clause.query.search(query)

        if private_only:
            intermediate_query = intermediate_query.filter(Clause.clause_user == user_id)
        else:
            intermediate_query = intermediate_query.filter(or_(Clause.clause_user == user_id, Clause.clause_private == False))

        return intermediate_query.limit(20).all()


    def save_clause(self, clause_id, title, text, private, user_id):

        # check wheter it's a new one or not.
        if clause_id != None:

            clause = Clause.query.filter_by(clause_id = clause_id, clause_user = user_id).first()

            if clause == None:
                return (False, 'No clause found for user')

            clause.clause_title = title
            clause.clause_text = text
            clause.clause_private = private
            db.session.commit()

            return (True,"")


        # if a new clause, save it
        db.session.add(Clause(title, text, user_id, private))
        db.session.commit()

        return (True, "")


    def delete_clause(self, clause_id, user_id):

        if clause_id == None or user_id == None:
            return (False, "No clause selected..")

        clause = Clause.query.filter_by(clause_id = clause_id, clause_user = user_id).first()

        if clause == None:
            return (False, "No clause found to delete")
        
        db.session.delete(clause)
        db.session.commit()

        return (True, "")