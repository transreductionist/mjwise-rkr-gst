from scanpattern import scanpattern
from mark_strings import mark_strings
from doubly_linked_list import LinkedList


def rkr_gst(mantok_t, mantok_p, minimum_match_length, initial_search_length):
    search_length = initial_search_length
    stop = False
    while not stop:
        # Parameter longest_maximal_match is size of largest maximal-matches found in this iteration.
        maximal_matches = LinkedList()
        longest_maximal_match = scanpattern(mantok_t, mantok_p, search_length, maximal_matches)

        # Very long string; don't mark tiles but try again with larger s.
        if longest_maximal_match > 2*search_length:
            search_length = longest_maximal_match
        else:
            # Create tiles from matches taken from list of queues.
            mark_strings(mantok_t, mantok_p, maximal_matches)

            if search_length > 2*minimum_match_length:
                search_length = search_length/2
            elif search_length > minimum_match_length:
                search_length = minimum_match_length
            else:
                stop = True
    debug = 1
