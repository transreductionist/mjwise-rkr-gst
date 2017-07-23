
import os
import re
import nltk
import operator
from collections import Counter
from bs4 import BeautifulSoup
import pickle
import requests

import webhoseio

api_key = os.getenv('WEBHOSEIO_API_SERVER_KEY')
webhoseio.config(token=api_key)
output = webhoseio.query("filterWebContent", {"q": "\"samuel dubose\" language:english", "ts":1494202251730  })

print ''
print 'total results: ', output['totalResults']
print ''
data = []

# 2017-06-06: The counting is wrong.
#             You are missing the last batch.
while output['moreResultsAvailable']:
    for post_idx, post in enumerate(output['posts']):
        raw = post['text']
        nltk.data.path.append('./nltk_data/')  # set the path
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)

        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if nonPunct.match(w)]
        raw_word_count = Counter(raw_words)

        # Dont remove stop words because n-grams are important
        # no_stop_words = [w for w in raw_words if w.lower() not in stops]
        # no_stop_words_count = Counter(no_stop_words)

        # save the results
        # results = sorted(
        #     raw_word_count.items(),
        #     key=operator.itemgetter(1),
        #     reverse=True
        # )

        results = raw_words
        data.append(results)

    print 'remaining    : ', output['moreResultsAvailable']
    output = webhoseio.get_next()

pickle.dump(data, open( "data_20170719.p", "wb" ))


