"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: autodetect_language script
Unfortunately, the language labeling given in the original TalkOfEurope dataset is wrong,
many texts labeled as "english" are either not english or have mixed languages.

This script reads the Speech records from <db_url>, attempts to detect language using
TextBlob language detection features and writes the result in the "lang" field of the database.

Runs the process in multiple cores, the number of cores is given by <num_cores> parameter.

   Usage: autodetect_language [-h]

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""
from multiprocessing import Pool
import signal
from textblob import TextBlob
from talkofeuropedb.model import Speech, open_db
from talkofeuropedb.config import get_config
from docopt import docopt
from clint.textui import progress


def init_worker():
    # Ignore keyboard interrupts (will catch those in parent)
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def detect_language(s):
    return (s.id, TextBlob(s.speech).detect_language())


def main():
    args = docopt(__doc__)
    c = get_config()
    session = open_db()
    speeches = session.query(Speech).all()
    total_speeches = len(speeches)  # For progress bar purposes

    print "Computing using %d cores..." % c.num_cores
    pool = Pool(c.num_cores, init_worker)
    try:
        for id, lang in progress.bar(pool.imap_unordered(detect_language, speeches), label='Progress ', expected_size=total_speeches, every=1000):
            session.query(Speech).get(id).lang = lang
    except KeyboardInterrupt:
        print "Terminating pool.."
        pool.terminate()
        pool.join()

    print "Committing..."
    session.commit()

    num_english_texts = session.query(Speech).filter(Speech.lang == 'en').count()
    print "Done. English texts: %d" % num_english_texts