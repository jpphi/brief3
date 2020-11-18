#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:45:17 2020

@author: jpphi
"""

#! /usr/bin/python
# -*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def accueil():
    client = MongoClient ('localhost',27017)
    db = client.test
    texte=list(db.offres_emploi.find())

    mots = ["bonjour", "à", "toi,", "visiteur."]
    return render_template('accueil.html', titre="Bienvenue !", mots=texte)

if __name__ == '__main__':
    app.run(debug=True)
    
    
