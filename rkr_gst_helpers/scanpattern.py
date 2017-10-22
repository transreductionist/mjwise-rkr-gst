from manage_tokens import ManageTokens
from rkr_hashtable import RKRHashtable


def scanpattern(mantok_t, mantok_p, search_length, maximal_matches):
    hashtable = RKRHashtable()

    idx_next_unmarked = mantok_t.index_of_next_unmarked_token(0)

    while idx_next_unmarked is not None:
        idx_next_marked = mantok_t.index_of_next_marked_token(idx_next_unmarked)

        if not idx_next_marked:
            distance_to_next_tile = mantok_t.length_of_tokens - idx_next_unmarked

        else:
            distance_to_next_tile = (idx_next_marked + 1) - idx_next_unmarked

        if distance_to_next_tile < search_length:
            if idx_next_marked:
                idx_next_unmarked = mantok_t.index_of_next_unmarked_token(idx_next_marked)
            else:
                idx_next_unmarked = None

        else:
            # Found a substring to calculate hash-value for.
            i = idx_next_unmarked
            j = idx_next_unmarked + search_length
            substring = ''.join(mantok_t.tokens[i:j])
            created_hash = hashtable.create_hash_value(substring)
            data = (i, j - 1)
            hashtable.add(created_hash, data)

            idx_next_unmarked = mantok_t.index_of_next_unmarked_token(idx_next_unmarked + 1)

        stop = 1
    stop = 2

    longest_maximal_match = 0

    idx_next_unmarked = mantok_p.index_of_next_unmarked_token(0)

    while idx_next_unmarked is not None:
        idx_next_marked = mantok_p.index_of_next_marked_token(idx_next_unmarked)

        if not idx_next_marked:
            distance_to_next_tile = mantok_p.length_of_tokens - idx_next_unmarked
        else:
            distance_to_next_tile = (idx_next_marked + 1) - idx_next_unmarked

        if distance_to_next_tile < search_length:
            if idx_next_marked:
                idx_next_unmarked = mantok_p.index_of_next_unmarked_token(idx_next_marked)
            else:
                idx_next_unmarked = None
        else:
            # Found a substring to calculate hash-value for.
            i = idx_next_unmarked
            j = idx_next_unmarked + search_length
            substring = ''.join(mantok_p.tokens[i:j])
            created_hash = hashtable.create_hash_value(substring)
            values = hashtable.get(created_hash)

            k = 0
            for value in values:
                m = value[0]
                t_token = mantok_t.tokens[m + k]
                p_token = mantok_p.tokens[i + k]
                t_unmarked = mantok_t.is_token_unmarked(m + k)
                p_unmarked = mantok_p.is_token_unmarked(i + k)
                while (p_token == t_token) and (p_unmarked and t_unmarked) and (m+k <= mantok_t.length_of_tokens-1 and i+k <= mantok_p.length_of_tokens-1):

                    # If at end of tokens allow increment because there was a match.
                    k = k + 1
                    if k > 2*search_length:
                        # Abandon the scan. It will be restarted with search_length = k.
                        return k

                    # If at end of tokens don't try to get next token because it will fail.
                    if (m+k != mantok_t.length_of_tokens and i+k != mantok_p.length_of_tokens):
                        t_token = mantok_t.tokens[m + k]
                        p_token = mantok_p.tokens[i + k]
                        t_unmarked = mantok_t.is_token_unmarked(m + k)
                        p_unmarked = mantok_p.is_token_unmarked(i + k)
                    else:
                        break

                maximal_matches.add(k, (m, i))

                stop = 1

            if k > longest_maximal_match:
                longest_maximal_match = k

            idx_next_unmarked = mantok_p.index_of_next_unmarked_token(idx_next_unmarked + 1)

            stop = 1
    stop = 2
    return longest_maximal_match
