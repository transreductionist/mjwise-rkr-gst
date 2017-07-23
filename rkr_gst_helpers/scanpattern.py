from manage_tokens import ManageTokens
from rkr_hashtable import RKRHashtable


def scanpattern(mantok_t, mantok_p, search_length, maximal_matches):
    hashtable = RKRHashtable()

    # Find hash-value for all 5-tokens, advancing a token at a time, skipping over marked tokens.
    # Starting at the first unmarked token of t_tokens
    # For each unmarked t_tokens
    #     If distance to next tile < s:
    #         Advance to first unmarked token after next tile
    #     Else create the KR hash-value:
    #         For substring t_tokens[t:t+s-1]
    #         Add to hash table

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

    # Starting at the first unmarked token of p_tokens
    # For each unmarked p_token:
    #     If distance to next tile < search_length:
    #         Advance position to first unmarked token after next tile
    #     Else Create the KR hash-value:
    #         For substring p_tokens[p: p+search_length-1]
    #         Check hashtable for hash of KR hash-value
    #         For each hash-table entry with equal hashed KR hash-value
    #             While p_tokens[p+k] == t_tokens[t+k] AND unmarked(p+k) AND unmarked(t+k)
    #                   k = k + 1
    #                   Extend match until non-match or element marked
    #             If k > 2*search_table:
    #                 Abandon the scan. It will be restarted with search_length = k.
    #                 Return(k)
    #             Else record new maximal-match
    #                 The maximal match can be any number greater than search_length
    #                     And this because we have extended match until non-match or an element is marked
    #                 Return the length of longest maximal-match

    longest_maximal_match = 0

    idx_next_unmarked = mantok_p.index_of_next_unmarked_token(0)
    while idx_next_unmarked is not None:

        idx_next_marked = mantok_p.index_of_next_marked_token(idx_next_unmarked)
        if not idx_next_marked:
            distance_to_next_tile = mantok_p.length_of_tokens - idx_next_unmarked
        else:
            distance_to_next_tile = (idx_next_marked + 1) - idx_next_unmarked


        _idx_next_unmarked = idx_next_unmarked
        _idx_next_marked = idx_next_marked
        _distance_to_next_tile = distance_to_next_tile
        stop = 1

        if _distance_to_next_tile < search_length:
            if _idx_next_marked:
                _idx_next_unmarked = mantok_p.index_of_next_unmarked_token(idx_next_marked)
            else:
                _idx_next_unmarked = None


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
