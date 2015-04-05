"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: collect_words
Compute the set of words that will be considered for extracting significant ones.

Inputs word features extracted using ``compute_features words`` and stored in
<zodb_dir>. Selects a set of words that is common for five largest countries (by speech counts).
Subtracts from that stopwords for numerous languages.

Writes output into ZODB variable root.all_words as a python set object.

   Usage: collect_words [-h]

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""
from multiprocessing import Pool
import signal
from sqlalchemy import func, desc
from docopt import docopt
from unidecode import unidecode
import transaction
import nltk
from talkofeuropedb.model import Speech, open_db
from talkofeuropedb.config import get_config
from talkofeuropewords.zodb import open_zodb


def init_worker():   # Ignore keyboard interrupts (will catch those in parent)
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def country_words(country_code):
    session = open_db()
    zodb_root = open_zodb(read_only=True)
    ids = session.query(Speech.id).filter(Speech.lang == 'en').filter(Speech.country == country_code).all()
    all_words = set()
    for (id,) in ids:
        all_words = all_words.union(zodb_root.features['words'][id].keys())
    return all_words


def main():
    args = docopt(__doc__)
    c = get_config()
    session = open_db()

    print "Finding 5 most active countries"
    countries = session.query(Speech.country, func.count(Speech.id)).filter(Speech.lang == 'en').group_by(Speech.country).order_by(desc(func.count(Speech.id))).limit(5).all()
    print countries
    country_codes = [c[0] for c in countries]

    print "Collecting words used by each country using 5 cores"
    pool = Pool(5, init_worker)
    try:
        word_sets = pool.map(country_words, country_codes)
    except KeyboardInterrupt:
        print "Terminating pool.."
        pool.terminate()
        pool.join()

    print "Collected word sets with sizes: ", map(len, word_sets)
    print "Computing intersection..."
    word_set = reduce(lambda x, y: x & y, word_sets)
    print "Result size: ", len(word_set)

    print "Subtracting stopwords..."
    nltk.download('stopwords')
    langs = ['english', 'dutch', 'french', 'italian', 'portuguese', 'swedish', 'german', 'spanish']
    all_stopwords = reduce(lambda x, y: x | y, [set(nltk.corpus.stopwords.words(lng)) for lng in langs])
    all_stopwords = set(map(unidecode, all_stopwords))
    word_set = word_set - all_stopwords
    print "Resulting word set size: ", len(word_set)

    print "Saving..."
    zodb_root = open_zodb()
    zodb_root.all_words = word_set
    transaction.commit()
    print "Done"