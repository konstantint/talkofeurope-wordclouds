# Talk of Europe Creative Camp #2 - Wordcloud project - Complete analysis script
# Copyright 2015, Konstantin Tretyakov, Ilya Kuzovkin, Alexander Tkachenko
# The timings below correspond to num_cores set to 130

# Create directories
mkdir -p data/ttl
mkdir data/textdb
mkdir data/zodb

export CONFIG=sample_config.py

# ---------- Download TURTLE files ----------
time bin/get_ttl

# real    9m41.706s
# user    1m35.027s
# sys     0m6.182s

# ---------- Extract text into CSV ----------
# This one requires a decent amount of memory (i.e. 2G may not be enough)
time bin/ttl2csv

# real    22m30.523s
# user    22m16.713s
# sys     0m13.281s

# ---------- Write into DB ----------
# We use SQLite in our experiments
time bin/csv2db

# real    3m56.119s
# user    2m24.342s
# sys     0m19.943s

# ---------- Autodetect language ----------
time bin/autodetect_language

# real    6m19.575s
# user    12m46.904s
# sys     7m18.482s

# ---------- Extract words from texts ----------
time bin/compute_features words

# real    34m45.589s
# user    126m25.077s
# sys     11m55.050s

# ---------- Compute set of common words to use in feature extraction ----------
time bin/collect_words

# real    5m12.383s
# user    17m29.505s
# sys     0m48.623s

# ---------- Extract country-specific words ----------
time bin/extract_significant_features words by_country

# real    3m49.683s
# user    38m27.360s
# sys     3m30.471s

# ---------- Extract month-specific words ----------
time bin/extract_significant_features words by_month

# real    4m6.577s
# user    118m20.409s
# sys     13m32.315s

# ---------- Extract year-specific words ----------
 time bin/extract_significant_features words by_year

# real    5m20.749s
# user    33m50.396s
# sys     3m36.261s


# If you used default config (sample_config.py), at this point the results are
# all written out to the file <root_dir>/data/resultsdb.sqlite
# This file is used by the talkofeuropeweb visualization webapp (it is bundled with it).