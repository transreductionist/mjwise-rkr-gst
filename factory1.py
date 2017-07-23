from rkr_gst_helpers.articles import strings
from rkr_gst_helpers.rkr_gst import rkr_gst
from rkr_gst_helpers.manage_tokens import ManageTokens
import math
import pickle
import ipdb

import matplotlib.pyplot as plt
import numpy as np

articles = pickle.load(open( "data_20170719.p", "rb" ))

article_1 = articles[0]
article_2 = articles[4]

print article_1
print ''
print article_2
print ''
ipdb.set_trace()

mininum_match_length = 3
initial_search_size = 20

t_tokens = article_1
p_tokens = article_2

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

print normalized_similarity
