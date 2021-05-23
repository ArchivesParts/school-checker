
from platform import release
import pwd
from flask import Flask, render_template, request
import pymongo
import requests
from pymongo import MongoClient
import json
from datetime import datetime
import hashlib
from ecole_direct import EcoleDirect
from note_service import NoteService
from stats import Stats

app = Flask(__name__)

app.config.from_pyfile("config.py")


@app.route('/index')
def index():
    return render_template('index.jinja')


@app.route('/refresh')
def refresh():
    ecole_direct = EcoleDirect(
        student_id=app.config.get('ED_STUDENT_ID'),
        api_url=app.config.get('ED_BASE_URL'),
        login=app.config.get('ED_LOGIN'),
        pwd=app.config.get('ED_PASSWORD'))
    notes = ecole_direct.read_note()

    service = NoteService(
        connection_string=app.config.get('MONGO_CONNEXION_STRING'),
        database=app.config.get('MONGO_DATABASE'),
        collection=app.config.get('MONGO_COLLECTION'))
    stats = Stats()
    for note in notes['data']['notes']:
        note['_id'] = hashlib.md5("{}_{}_{}_{}_{}_{}".format(
            note['codeMatiere'], note['codePeriode'], note['date'], note['devoir'], note['valeur'], note['minClasse'], note['moyenneClasse'], note['maxClasse'],).encode()).hexdigest()
        note['date'] = datetime.strptime(note['date'], '%Y-%m-%d')

        try:
            real_note = service.insert(note)
            print(real_note['new'])
            stats.add(real_note)
        except pymongo.errors.DuplicateKeyError:
            print('Duplicate note {}'.format(note['_id']))
    stats_results = stats.mean()
    print(stats_results)
    return render_template('refresh.jinja', created=stats_results['created'], updated=stats_results['updated'], total=stats_results['total'], coef=stats_results['coef'])


@app.route('/check/<note>')
def check(note):
    client = MongoClient(app.config.get('MONGO_CONNEXION_STRING'))
    collection = client.get_database(app.config.get(
        'MONGO_DATABASE')).get_collection(app.config.get('MONGO_COLLECTION'))
    query = {'_id': note}

    result = collection.update_one(
        filter=query, update={'$set': {'validated': True}})
    return "ok" if result.modified_count == 1 else "ko"


@app.route('/')
def home():
    return render_template('layout.jinja', value=7)


@app.route('/notes')
@app.route('/notes/<matiere>')
def notes(matiere=None):
    service = NoteService(
        connection_string=app.config.get('MONGO_CONNEXION_STRING'),
        database=app.config.get('MONGO_DATABASE'),
        collection=app.config.get('MONGO_COLLECTION'))
    read = request.args.get('read')
    noted = request.args.get('noted')
    notes = service.get(matiere=matiere, read=read, noted=noted)
    return render_template('notes.jinja', notes=notes)
