from flask import Flask, render_template, request
import pymongo
import requests
from pymongo import MongoClient
import json
from datetime import datetime
import hashlib


class EcoleDirect:
    """Class to handle access Ecole Directe API."""

    def __init__(self, api_url: str, login: str, pwd: str, student_id: int):
        """ Initialize the communication with the ED API. """
        self.studen_id = student_id

        url_login = "{}login.awp".format(api_url)
        login_data = {"identifiant": login,
                      "motdepasse": pwd}
        auth_req = requests.post(url_login,
                                 data='data={}'.format(json.dumps(login_data)))

        self.api_url = api_url
        if(auth_req.status_code != requests.codes.ok):
            raise Exception("Cannot login")
        authentication = auth_req.json()
        self.token = authentication['token']

    def read_note(self):
        """ Read all notes from the ecole direct API. """
        url_notes = '{}eleves/{}/notes.awp?verbe=get&'.format(
            self.api_url, self.studen_id)
        notes_data = {"token": self.token}
        notes = requests.post(url_notes,
                              data='data={}'.format(json.dumps(notes_data))).json()
        return notes
