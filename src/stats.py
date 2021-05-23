from flask import Flask, render_template, request
import pymongo
import requests
from pymongo import MongoClient
import json
from datetime import datetime
import hashlib


class Stats:
    """Class to calculate some stats on notes."""

    def __init__(self):
        self.notes = []

    def add(self, note):
        self.notes.append(note)
        return len(self.notes)

    def mean(self):
        print("=====MEAN=====")
        created = 0
        updated = 0
        total = 0
        coef = 0
        for note in self.notes:
            if(note['valeur']):
                n = 20*float(note['valeur'].replace(',', '.')) / \
                    float(note['noteSur'].replace(',', '.'))
                c = float(note['coef'].replace(',', '.'))
                total = total + n*c
                coef = coef+c
            print("C:{} U:{} <= {}".format(created, updated, note['new']))
            created = created+(1 if note['new'] == True else 0)
            updated = updated+(1 if note['new'] == False else 0)
        return {"created": created, "updated": updated, "total": total, "coef": coef}
