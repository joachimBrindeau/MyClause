import os
import flask_whooshalchemy

from flask import Flask, redirect, url_for, Blueprint, render_template, request, jsonify, session
from flask_dance.contrib.linkedin import linkedin

from ..utility.linkedin import protected_route, protected_api_endpoint
from app import linkedin_bp, sqldb as db

from ..db.models.Clause import Clause
from ..db.repository.ClauseRepository import ClauseRepository

bp = Blueprint('routes', __name__)

# repos
clause_repository = ClauseRepository()

@bp.route("/")
@protected_route
def index():
    return render_template('index.html')

@bp.route("/api/search")
@protected_api_endpoint
def search():
    # user_id
    user_id = session['user_id']
    # parse the query from the request
    query = request.args.get('q', None)
    private_only = request.args.get('private', None)
    # return the result (json format)
    results = clause_repository.query_clauses(query, user_id, private_only != None)

    if results == None:
        return jsonify({"count":0})

    # to json
    json_results = [{'id':result.clause_id, 'title':result.clause_title, 'text':result.clause_text[:200]} for result in results]
    # return result
    return jsonify({"count":len(json_results), "result":render_template("_results.html", results=json_results)})

@bp.route('/api/save', methods=["POST"])
@protected_api_endpoint
def save():
    # user_id
    user_id = session['user_id']
    
    # parse form parameters
    clause_id = request.form.get('clauseId', None)
    title = request.form.get('clauseTitle', None)
    text = request.form.get('clauseText', None)
    private = request.form.get('clausePrivate', False)

    result = clause_repository.save_clause(clause_id, title, text, private != False, user_id)

    return jsonify({'success':result[0], 'message':result[1]})

@bp.route('/api/delete/<id>')
@protected_api_endpoint
def delete(id):
    # user_id
    user_id = session['user_id']

    result = clause_repository.delete_clause(id, user_id)

    return jsonify({'success':result[0], 'message':result[1]})


@bp.route('/api/clause/<id>')
@protected_api_endpoint
def fetch_clause(id):
    # user_id
    user_id = session['user_id']

    result = clause_repository.get_clause(id)

    if(result == None):
        return jsonify({'success':False})

    return jsonify({'success':True, 'id':result.clause_id, 'title':result.clause_title, 'text':result.clause_text})

@bp.route('/login')
def login():
    if linkedin.authorized:
        return redirect(url_for('routes.index'))

    return render_template('login.html')

@bp.route('/logout')
def logout():
    del linkedin_bp.token
    return redirect(url_for('routes.login'))


