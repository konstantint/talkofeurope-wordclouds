# -*- coding: UTF-8 -*-
"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: Visualization webapp
Views.

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""
from flask import render_template, request, jsonify
from .main import app
from .model import db, ByCountry, ByMonth, ByYear
from sqlalchemy import *
from math import log

MAX_WORDS = 150

# ----------------------------------- Logic ------------------------------------- #
class WordSizer(object):
    '''Given a list of words (each represented as a dict with 'odds' field representing the odds score of the word),
       computes suitable wordcloud sizes, adding the 'size' field to each object)'''

    tol = 1e-10
    MIN_SIZE = 12
    MAX_SIZE = 70

    def __call__(self, words):
        if len(words) == 0:
            return words
        sizes = [log(max(w['odds'], self.tol)) for w in words]
        max_size = max(sizes)
        min_size = min(sizes)
        if (max_size == min_size):
            max_size = min_size + 1
        a = (self.MAX_SIZE - self.MIN_SIZE)/(max_size - min_size)
        b = self.MIN_SIZE - a*min_size
        sizes = [a*s + b  for s in sizes]
        for i, w in enumerate(words):
            w['size'] = sizes[i]
        return words

wsizer = WordSizer()

# ----------------------------------- Views ------------------------------------- #
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------------ By Country ------------------------------ #

@app.route('/by_country')
def by_country():
    countries = [c for (c,) in db.session.query(distinct(ByCountry.foreground_group_name)).order_by(ByCountry.foreground_group_name)]
    return render_template('by_country.html', countries=countries)

@app.route('/words/by_country/<code>')
def words_by_country(code):
    assert len(code) == 2
    unique = int(request.args.get('unique', 0))
    if int(unique) != 0:
        results = db.session.query(ByCountry).filter(ByCountry.foreground_group_name == code).\
            filter(text("word not in (select word from words_bycountry where foreground_group_name != '%s')" % code)).order_by(ByCountry.pval, desc(ByCountry.odds)).limit(MAX_WORDS)
    else:
        results = db.session.query(ByCountry).filter(ByCountry.foreground_group_name == code).order_by(ByCountry.pval, desc(ByCountry.odds)).limit(MAX_WORDS)
    words = [{'text': o.word, 'odds': min(float(o.odds), 100), 'pval': float(o.pval)} for o in results]
    return jsonify(words = wsizer(words))

@app.route('/wordstats/by_country/<word>')
def wordstats_by_country(word):
    countries = [c[0] for c in db.session.query(distinct(ByCountry.foreground_group_name)).order_by(ByCountry.foreground_group_name)]
    val = {c.foreground_group_name: min(float(c.odds), 100) for c in db.session.query(ByCountry).filter(ByCountry.word == word)}
    data = [{"country": cn, "value": val.get(cn, None)} for cn in countries]
    return jsonify(data=data)

# ------------------------------ By Month ------------------------------ #
@app.route('/by_month')
def by_month():
    return render_template('by_month.html', min_year=1999, max_year=2014)

@app.route('/words/by_month/<code>')
def words_by_month(code):
    results = db.session.query(ByMonth).filter(ByMonth.foreground_group_name == code).order_by(ByMonth.pval, desc(ByMonth.odds)).limit(MAX_WORDS)
    words = [{'text': o.word, 'odds': min(float(o.odds), 100), 'pval': float(o.pval)} for o in results]
    return jsonify(words = wsizer(words))

@app.route('/wordstats/by_month/<word>')
def wordstats_by_month(word):
    months = [c for (c,) in db.session.query(distinct(ByMonth.foreground_group_name)).order_by(ByMonth.foreground_group_name)]
    val = {c.foreground_group_name: min(float(c.odds), 100) for c in db.session.query(ByMonth).filter(ByMonth.word == word)}
    data = [{"month": m, "value": val.get(m, None)} for m in months]
    return jsonify(data=data)

# ------------------------------ By Year ------------------------------ #
@app.route('/by_year')
def by_year():
    return render_template('by_year.html', min_year=1999, max_year=2014)

@app.route('/words/by_year/<code>')
def words_by_year(code):
    results = db.session.query(ByYear).filter(ByYear.foreground_group_name == code).order_by(ByYear.pval, desc(ByYear.odds)).limit(MAX_WORDS)
    words = [{'text': o.word, 'odds': min(float(o.odds), 100), 'pval': float(o.pval)} for o in results]
    return jsonify(words = wsizer(words))

@app.route('/wordstats/by_year/<word>')
def wordstats_by_year(word):
    years = [c for (c,) in db.session.query(distinct(ByYear.foreground_group_name)).order_by(ByYear.foreground_group_name)]
    val = {c.foreground_group_name: min(float(c.odds), 100) for c in db.session.query(ByYear).filter(ByYear.word == word)}
    data = [{"year": y, "value": val.get(y, None)} for y in years]
    return jsonify(data=data)




# ------------------------------------ Error handlers ---------------------------------------- #
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
