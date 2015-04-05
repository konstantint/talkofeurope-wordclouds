# Sample configuration file
# Specifies parameters used by scripts in talkofeuropedb & talkofeuropewords packages.
import os

root_dir = os.path.abspath(os.path.dirname(os.getenv('CONFIG')))

# Directory for downloading TURTLE files
ttl_dir = root_dir + '/data/ttl'

# Directory for storing CSV & SQLITE files with text data
textdb_dir = root_dir + '/data/textdb'

# Directory for keeping the zodb.fs file with precomputed feature vectors
zodb_dir = root_dir + '/data/zodb'

# Database URL for importing Speech data
db_url = "sqlite:///%s/english.sqlite" % textdb_dir

# Database URL for storing overrepresentation analysis results (extract_significant_features script)
resultsdb_url = "sqlite:///%s/data/resultsdb.sqlite" % root_dir

# Number of cores to use for parallel tasks
num_cores = 130


# Config parameters used in Flask config
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(root_dir, 'src/talkofeuropeweb/data/resultsdb.sqlite')
DEBUG = True
SQLALCHEMY_ECHO = True
