from test_2_strings import str1
from test_2_strings import str2
from rkr_gst_helpers.rkr_gst import rkr_gst
from rkr_gst_helpers.manage_tokens import ManageTokens
import math
import pickle

def factory():
    article_1 = [str.strip() for str in str1.split(' ') if str != '']
    article_2 = [str.strip() for str in str2.split(' ') if str != '']

    mininum_match_length = 3  # default: 3
    initial_search_size = 8  # default: 20

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

if __name__ == '__main__':
    factory()
