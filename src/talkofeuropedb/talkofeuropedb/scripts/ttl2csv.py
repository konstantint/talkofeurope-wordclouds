"""
Talk of Europe Creative Camp #2 :: Wordcloud project :: ttl2csv script
The script parses LinkedPolitics gzipped TURTLE files, extracts English texts
and writes those out in a CSV file.

Stores the gzipped csv file in <textdb_dir>/English.csv.gz

   Usage: ttl2csv [-h]

Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko.
License: MIT
"""

import rdflib, csv, os, gzip, sys
from talkofeuropedb.config import get_config
from docopt import docopt
from clint.textui import progress


files = ['Schema.ttl.gz',
         'Events_and_structure.ttl.gz',
         'MembersOfParliament_background.ttl.gz',
         'English.ttl.gz']


def main():
    args = docopt(__doc__)
    c = get_config()

    # create new Graph object
    g = rdflib.Graph()

    print "Loading files: ",
    sys.stdout.flush()

    # parse data files (could take a while: 4,000,000 triples will take ~10 minutes )
    for fn in files:
        print fn,
        sys.stdout.flush()
        with gzip.open(os.path.join(c.ttl_dir, fn)) as f:
            result = g.parse(f, format='turtle')

    print "\nQuerying..."

    # compile query
    qres = g.query("""
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX lp: <http://purl.org/linkedpolitics/>
        PREFIX lpv: <http://purl.org/linkedpolitics/vocabulary/>
        PREFIX xml: <http://www.w3.org/XML/1998/namespace>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT ?date ?speaker ?firstname ?lastname ?country ?text
        WHERE {
            ?sessionday dcterms:hasPart ?agendaitem.
            ?sessionday dc:date ?date.
            ?agendaitem dcterms:hasPart ?speech.
            ?speech lpv:speaker ?speaker.
            ?speaker lpv:countryOfRepresentation ?countryobj.
            ?countryobj lpv:acronym ?country.
            ?speaker foaf:givenName ?firstname.
            ?speaker foaf:familyName ?lastname.
            ?speech lpv:text ?text.
        }
    """)

    # The query is actually executed now, it takes a while (~3 min)
    print "Found %d records" % len(qres)

    # Write out csv file
    with gzip.open(os.path.join(c.textdb_dir, 'English.csv.gz'), 'wb') as csvfile:
        csv_headers = ['Date', 'SpeakerURI', 'Firstname', 'Lastname', 'Country', 'Speech']
        speechwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        speechwriter.writerow(csv_headers)

        for row in progress.bar(qres, label='Writing CSV ', expected_size=len(qres), every=1000):
            csv_line = [x.encode('utf8').strip() for x in row]
            speechwriter.writerow(csv_line)

    print 'Done'

