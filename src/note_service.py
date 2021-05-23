import string
from flask import Flask, render_template, request
import pymongo
import requests
from pymongo import MongoClient
import json
from datetime import datetime
import hashlib


class NoteService:
    """Class to handle access the Mongo Atlas database."""

    def __init__(self, connection_string, database, collection):
        """ Initialize the communication with the database. """
        client = MongoClient(connection_string)
        self.database = client.get_database(
            database).get_collection(collection)

    def get(self, matiere: str = None, read: str = None, noted: str = None):
        """ Get all notes."""
        query = {}
        if(read != None):
            query['validated'] = True if read == 'yes' else False
        if(noted != None and noted == 'no'):
            query['valeur'] = ''
        if(matiere != None):
            query['codeMatiere'] = matiere
        print(query)
        notes = self.database.find(query).sort(
            'date', direction=pymongo.DESCENDING)
        print(notes)
        return notes

    def insert(self, note):
        """ Drop all notes."""
        # print(note)
        existing = self.database.find_one({'_id': note['_id']})
        if existing == None:
            print("New note")
            note['validated'] = False
            note['new'] = True
            self.database.insert(note)
        else:
            print("Update note")
            note['new'] = False
            note['validated'] = existing.setdefault('validated', False)
            self.database.update({'_id': note['_id']}, note)
        return note

    def drop(self):
        """ Drop all notes."""
        return self.database.delete_many({})
