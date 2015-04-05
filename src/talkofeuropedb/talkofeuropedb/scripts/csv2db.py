"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: csv2db script
The script loads the CSV file produced by ttl2csv into a database.

Reads the file <textdb_dir>/English.csv.gz, writes to database given by <db_url>.
Creates the necessary tables (dropping them if they exist)

   Usage: csv2db [-h]

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""

import csv, gzip, os
from docopt import docopt
from clint.textui import progress
from talkofeuropedb.model import *
from talkofeuropedb.config import get_config


def main():
    args = docopt(__doc__)
    c = get_config()
    e = create_engine(c.db_url)
    Base.metadata.drop_all(e)
    Base.metadata.create_all(e)
    Session = sessionmaker(e)
    s = Session()
    with gzip.open(os.path.join(c.textdb_dir, 'English.csv.gz'), 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        reader.next()   # Skip header
        for row in progress.mill(reader, label='Writing to DB ', expected_size=254253, every=1000):
            sp = Speech(date=datetime.strptime(row[0], '%Y-%m-%d'),
                        speaker_uri=unicode(row[1], 'utf-8'),
                        first_name=unicode(row[2], 'utf-8'),
                        last_name=unicode(row[3], 'utf-8'),
                        country=row[4],
                        speech=unicode(row[5], 'utf-8'))
            s.add(sp)
    print "Committing..."
    s.commit()
    print "Done"

