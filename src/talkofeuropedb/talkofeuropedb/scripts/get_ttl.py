"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: get_ttl script
The script downloads the LinkedPolitics TURTLE files necessary for further analysis.

Stores the gzipped ttl files into the directory specified by the
"ttl_dir" configuration parameter in $CONFIG.

   Usage: get_ttl [-h]

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""

from docopt import docopt
from talkofeuropedb.config import get_config
import os
import gzip
import urllib
import requests
from clint.textui import progress


graph_list = ['http://purl.org/linkedpolitics/Schema',
              'http://purl.org/linkedpolitics/English',
              'http://purl.org/linkedpolitics/Events_and_structure',
              'http://purl.org/linkedpolitics/MembersOfParliament_background']


def download_gzipped(source_url, target_file):
    r = requests.get(source_url, stream=True)
    with gzip.open(target_file, 'wb') as f:
        total_length = int(r.headers.get('content-length', 0))
        bar = progress.mill if total_length == 0 else progress.bar
        for chunk in bar(r.iter_content(chunk_size=1024), label='Downloading', expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def main():
    args = docopt(__doc__)
    c = get_config()
    print "Downloading files into %s" % c.ttl_dir
    for g in graph_list:
        target_file = os.path.join(c.ttl_dir, g.split('/')[-1] + '.ttl.gz')
        source_url = "http://linkedpolitics.ops.few.vu.nl/api/export_graph?graph=%s&mimetype=text%%2Fplain&format=turtle" % urllib.quote(g, '')
        print "Downloading %s..." % g
        download_gzipped(source_url, target_file)
    print "Done"
