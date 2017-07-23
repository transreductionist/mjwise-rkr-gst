
def mark_strings(mantok_t, mantok_p, maximal_matches):

    # Starting with the top queue, while there is a non-empty queue
    #     If the current queue is empty:
    #         Drop to next queue: this corresponds to smaller maximal-matches
    #     Else:
    #         Remove match(p, t, L) from queue:
    #         <Assume length of maximal-matches in current queue is L>
    #     If match not occluded:
    #         If for all j: 0, 1, 2, ... search_length - 1, p_tokens[p + j] == t_tokens[t + j]:
    #             Match is not hash artifact
    #             for j = 0 to L - 1:
    #                 mark_token(p_tokens[p + j])
    #                 mark_token(t_tokens[t + j])
    #                 <The length_of_tokens_tiled = length_of_tokens_tiled + L>
    #     Else L - L_occluded >= search_length then
    #        <This is the unmarked part remaining of the maximal-match>
    #        Replace unmarked portion on list of queues

    for maximal_match_length in maximal_matches.maximal_match_lengths:
        queue = maximal_matches.find(maximal_match_length)
        matches = queue.data
        maximal_matches.remove(maximal_match_length)
        for match in matches:  # while queue is not empty
            for j in range(0, maximal_match_length):
                mantok_t.mark_token(match[0] + j)
                mantok_p.mark_token(match[1] + j)
        stop = 1
    stop = 0


def is_occluded(match, tiles):
    """Returns true if the match is already occluded by another match 
        in the tiles list.

        Note that "not occluded" is taken to mean that none of the tokens 
        Pp to Pp+maxmatch-1 and Tt to Tt+maxmatch-1 has been marked during
        the creation of an earlier tile. However, given that smaller tiles
        cannot be created before larger ones, it suffices that only the ends
        of each new putative tile be testet for occlusion, rather than the whole
        maxmimal match. 
        [String Similarity via Greedy String Tiling and Running Karp-Rabin Matching
        http://www.pam1.bcs.uwa.edu.au/~michaelw/ftp/doc/RKR_GST.ps]
    """
    for m in tiles:
        if m[0] + m[2] == match[0] + match[2] and m[1] + m[2] == match[1] + match[2]:
            return True
    return False
