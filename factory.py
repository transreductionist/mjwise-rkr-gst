from rkr_gst_helpers.articles import strings
from rkr_gst_helpers.rkr_gst import rkr_gst
from rkr_gst_helpers.manage_tokens import ManageTokens
import math
import pickle
import ipdb

import matplotlib.pyplot as plt
import numpy as np

articles = pickle.load(open( "data_20170719.p", "rb" ))

mininum_match_length = 3
initial_search_size = 20

del articles[4]
del articles[15]

tmp_articles = articles[0:50]

ipdb.set_trace()

articles = [tmp_articles[16], tmp_articles[8]]

# article1 = articles[16]
# article1 = articles[8]

# Traceback (most recent call last):
#   File "factory.py", line 24, in <module>
#     for article1 in articles:
#   File "/home/apeters/github/nlp-projects/rkr-gst/rkr_gst_helpers/rkr_gst.py", line 12, in rkr_gst
#     longest_maximal_match = scanpattern(mantok_t, mantok_p, search_length, maximal_matches)
#   File "/home/apeters/github/nlp-projects/rkr-gst/rkr_gst_helpers/scanpattern.py", line 105, in scanpattern
#     p_token = mantok_p.tokens[i + k]
# IndexError: list index out of range

res = []
m = 0
n = 0
for article1 in articles:
    tmp_res = []
    n = 0
    for article2 in articles:
        print '%s  %s' % (m, n)
        t_tokens = article1
        p_tokens = article2

        mantok_t = ManageTokens(t_tokens)
        mantok_p = ManageTokens(p_tokens)

        rkr_gst(mantok_t, mantok_p, mininum_match_length, initial_search_size)

        tiles = {}
        i = 0
        for token in mantok_t.is_marked:
            if token:
                i += 1
            elif not token and i > 0:
                if i in tiles:
                    tiles[i] += 1
                else:
                    tiles[i] = 1
                i = 0

        normalization = (mantok_t.length_of_tokens + mantok_p.length_of_tokens)/2.0
        similarity = 0
        for tile_length, total in tiles.items():
            similarity += total*tile_length*math.log(tile_length + 1)

        normalized_similarity = similarity/normalization
        tmp_res.append(normalized_similarity)
        n += 1
    m += 1
    res.append(tmp_res)

pickle.dump(res, open( "res_20170719.p", "wb" ))
