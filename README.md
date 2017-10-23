# RKR-GST Algorithm
## Running Karp-Rabin Matching and Greedy String Tiling
The algorithm described here was implemented following the psuedo-code (see Appendix A) given in the paper by 
Michael J. Wise,  
[Running Karp-Rabin Matching and Greedy String Tiling](http://sydney.edu.au/engineering/it/research/tr/tr463.pdf) in 
the Basser Department of Computer Science Technical Report Number 463 (March 1993), which was submitted to 
Software-Practice and Experience.

The algorithm answers the question, given 2 strings what is the degree of similarity between them? Consider
2 articles which are tokenized into lists. The process of tokenization is not covered here, and may include removing
stop words, and other cleaning operations. Each word can be thought of as a tile, or token of the list. The algorithm 
begins by setting an initial search length, as well as a minimum match length. The first list is traversed in n-grams 
with a length of the initial search length. At each tiling of the text a hash is created and an entry made in a running 
hash table. After the first list is covered, the second list is traversed. An n-gram is pulled from the second list, 
a hash created, and a lookup done on the hash table. If a match is found the tiles in both lists will be marked. Once
the second list of tokens is completely traversed, the search length is decreased and the process repeated.

The algorithm is greedy. Consider the pass through the second list. If there is a match with the first list then 
the algorithm expands its search, and compares tiles beyond the search length. If there are additional tiles matching 
the first list then the maximal match length is incremented, and the tiles will be marked. 

The following will offer a more detailed view of the functions, classes, and process by which the algorithm arrives 
at a metric for the similarity between the 2 texts.

# Example Strings for Comparison
Below are 2 strings that will be used to describe the algorithm in detail. The first is a 17 word string and it
is represented by the object mantok_t (see below) of the class ManageTokens(): 

- T = Early today Lamar and Patty reached a deal to fund subsidies that were to be ended quickly

The comparison string is a modification to include text that is not copied as well as text that is. It is represented 
by the object mantok_p. The string is 19 tokens long:

- P = \[Early today Lamar and\] Barbara agreed that the \[subsidies that were to be ended quickly\] needed to be funded
 
The repeated n-grams have been highlighted with brackets \[ \] in the second string. Split the first string into a 
list and call it t. Split the second string into a list and call it p. The first set of matching tiles appear at 
t\[0:3\] and p\[0:3\]. The second set of repeated tiles appears at t\[10:16\] in the the first list and at p\[8:14\] 
in the second.

# Definitions
- Maximal-match: A substring P p starting at p matches a substring T t of starting at t. The match is assumed to be 
as long as possible, i.e until there is  no matching element, or an end-of-string is encountered. It might also occur
that one of the elements is found to be marked.
- Tile: A permanent and unique association of a substring from P with a matching substring from T. In the process of 
forming a tile, tokens of the two substrings are marked, and thereby become unavailable for further matches.
- Minimum-match-length: is deﬁned such that maximal-matches below this length are ignored. The minimum-match-length 
can be 1, but in general will be greater than this.

# Function factory()
The function factory() is the entry point for the algorithm, and initializes parameters and objects needed by the 
algorithm itself. For example, it gets the data, i.e. the articles, and tokenizes them. It sets the minimum matching 
n-gram search length, as well as the initial n-gram search size. The default values for the minimal search length is 
set to 3, and the initial search size is set to 20. For testing our 2 strings the program uses a minimal search 
length of 3, and an initial search size of 8.

The minimal search length, as well as the maximum search length can be viewed as hyperparameters, "high-level" 
properties of the algorithm, fixed before the evaluation progress is begun. Determining these parameters requires 
setting different values for them, comparing a corpus of texts, obtaining similarity results, and coming to an 
understanding as to what are the "best" values. The defaults given above seem to be common chosen values, but have 
not been validated in this context.

The module creates instances of ManageTokens() to manage the token lists throughout the process: mantok_t and mantok_p. 
From factory() the function rkr_gst() is called, which is the top level function for the RKR-GST algorithm. It makes 
use of scanpattern() that does the matching of tiles. When rkr_gst() returns, mantok_t and mantok_p contain the 
matched, i.e. marked tiles, and allow the computation of the similarity metric for characterizing the overlap of 
n-grams.

As mentioned, there are several helper functions and classes. Briefly, 
- Class LinkedList(): Efficient data structure for maintaining the maximal matches.
- Class ManageTokens(): Manages the list of tokens, specifically the marked, or matched tiles.
- mark_strings(): A function that takes the linked list and marks the matched tokens, while handling occluded tiles.
- Class RKRHashtable: A running hash table using XOR-shift to generate the hashes.

## Class ManageTokens(tokens)

### Attributes:
1. tokens: A list of tokens and is case sensitive, either t or p.
2. length_of_tokens: The length of the list of tokens. In the case of t this would be 17 and for p 19.
3. is_marked: A list to keep track of whether a token has been marked or not. This is the same 
length as the list of tokens. Each token corresponds to a Boolean in is_marked: token\[i\] corresponds 
is_marked\[i\] and is True or False.  

### Methods:
1. mark_token(self, idx): Set is_marked\[idx\] to True and return True.
2. unmark_token(self, idx): Set is_marked\[idx\] to False and return False.
3. is_token_marked(self, idx): Given the index idx function returns True or False.
4. is_token_unmarked(self, idx): Given the index idx function returns True or False.
5. index_of_next_marked_token(self, idx): Given the index idx function returns the next marked token.
6. index_of_next_unmarked_token(self, idx): Given the index idx function returns the next unmarked 
token.
7. get_tile(self, i, j): This just returns a slice over the token list and is used for retrieving a 
tiling.


# Function rkr_gst():

Given the hyperparameters and data this module drives the algorithm and returns the results contained within the 
ManageTokens() instantiated classes, e.g. mantok_t.is_marked and mantok_p.is_marked.

### Arguments:
1. mantok_t: This is an instance of ManageTokens() for the first tokenized text.
2. mantok_p: This is an instance of ManageTokens() for the second tokenized text.
3. mininum_match_length: As we look for n-grams, this will be the minimum size we consider.
4. initial_search_size: The initial tiling length for matching one slice of tokens to another.

The doubly-linked list is instantiated: maximal_matches = LinkedList()

### The Doubly Linked List

#### class Node(object):
Attributes:
1. maximal_match_length
2. next_node
3. prev_node
4. tiles

Methods:
1. get_next(self): Gets the next node.
2. set_next(self, next_node): Sets the next node.
3. get_prev(self): Gets the previous node.
4. set_prev(self, prev_node): Sets the previous node.
5. get_data(self): Gets the tiles for the node.
6. set_data(self, data): Sets the tiles on the node.
7. get_tiles(self): Gets the tiles for the node.
8. set_tiles(self, tiles): Sets the tiles on the node.

TODO: self.tiles and self.data seem to be redundant attributes and need to be reconciled.

#### class LinkedList(object):
Attributes:
1. root
2. size
3. curr_mml
4. maximal_match_lengths

Methods:
Some of the later methods are used for testing.
1. get_size(self): The size, number of nodes is set in the load_initial_data method. The load_initial_data method is
used for testing the linked list.
2. remove(self, maximal_match_length): Remove a node.
3. find(self, maximal_match_length): Find and return the node with the maximal_match_length.
4. add(self, maximal_match_length, data): Add a node.
5. set_root(self, maximal_match_length): Set the root node to the node with maximal_match_length.
6. move_to(self, maximal_match_length): Move to the node with maximal_match_length.
7. move_down(self): A test method that moves_down from the current root node.
8. move_up(self): A test method that moves_up from the current root node.
9. load_initial_data(self, maximal_match_length, data): Test method to load data.

A doubly linked list is used to maintain a list of nodes (class Node). Each node is associated with a maximal match 
length. The data for the node contains a nested list of matching string data, each of length maximal match length. 
The \_\_init\_\_() handles the creation of the list.

Importantly, the root node is set to the last position data was added or updated, and each node has an 
maximal match length attribute. The linked list keeps track of the current maximal match length to improve
efficiency. Given you are at a specific maximal match length, the next maximal match length is more than likely to be 
nearby.

# Function scanpattern():

This module compares 2 lists of tokens, and given an initial search size returns updated arguments:

### Arguments:
1. mantok_t: This is an instance of ManageTokens() for the first tokenized text.
2. mantok_p: This is an instance of ManageTokens() for the second tokenized text.
3. search_length: The length to begin the greedy tiling with.

### Returns:
1. maximal_matches: A doubly linked list of all the matches.

# Class RKRHashtable()

### Methods:
1. add(self, hash, data): Adds a key-value pair to the running hash table.
2. get(self, hash): Gets a value from a given key.
3. clear(self): Clears all key-value pairs from the dictionary.
4. create_hash_value(self, substring): It takes a substring and loops over each character creating a hash.


### Hash functions:
The hash is created summing the ordinal value of each character. For example, ord('a') returns the integer 97. 
Importantly, on each iteration the previous hash value is bitwise shifted left by one 1 bit.

Why the leftwise bit shift? The following is taken from a post about building 
[hash functions.](http://ticki.github.io/blog/designing-a-good-non-cryptographic-hash-function/)

The basic building blocks of good hash functions are difussions. A Difussion can be thought of as bijective hash 
functions, namely that input and output are uncorrelated. A bijective function is such that every input has one and 
only one output, and vice versa. 

Diffusions are often built using smaller, bijective components, which are called "subdiffusions". One must distinguish 
between the different kinds of subdiffusions. The first class to consider is the bitwise subdiffusions. These are 
quite weak when they stand alone, and thus must be combined with other types of subdiffusions. Bitwise subdiffusions 
might flip certain bits and/or reorganize them:

The second class is dependent bitwise subdiffusions. These are diffusions which permutes the bits and XOR them with 
the original value. Another similar often used subdiffusion in the same class is the XOR-shift:

- hash_value = ((hash_value << 1) + ord(c))

# RKR-GST by the Line

For the test case the minimum search length is set to 3, and the maximum initial search size is 8. With this initial 
search size and the 2 test strings given at the beginning of the document the first pass through the algorithm will 
find no matches. The first string is 17 tokens long:

- Early today Lamar and Patty reached a deal to fund subsidies that were to be ended quickly
- t = \[Early, today, Lamar, and, Patty, reached, a, deal, to, fund, subsidies, that, were, to, be, ended, quickly\]

The second string is 19 tokens long:

- Early today Lamar and Barbara agreed that the subsidies that were to be ended quickly needed to be funded
- p = \[Early, today, Lamar, and, Barbara, agreed, that, the, subsidies, that, were, to, be, ended, quickly, needed, to,
 be, funded\]
 
Note that the first set of matching tiles appears at t\[0:3\] and p\[0:3\]. It is 4 tiles long. The second set of 
repeated tiles appears at t\[10:16\] in the the first list of tokens, and at p\[8:14\] in the second. It is 7 tiles
long.

The second path through decreases the search length to 4, and here there are 2 matches. The first is a match across
4 tiles at the beginning. The second pass through finds a match of 4 tiles towards the end, but expanding the tiling 
looking for a longer match, a maximal match length of 7 is found. This is the greedy nature of the algorithm.

### Pass Through First List of Tokens
- Initialize the loop:
    - Looks for the next unmarked token: there are none.
- Token list for traversal is initialized to t\[0\]:
    - The next marked token is none, and the distance_to_next_tile returns the length of the list. 
    - Take the first 8 words and join them into a string.
    - From the string create a hash for t\[0:7\].
    - The next unmarked token is at t\[1\].
- Move to t\[1\] and then:
    - Next marked token is still none. It looks for next tile, and when it traverses the list and does not find one, 
    distance_to_next_tile returns the length of the list. 
    - Take the next 8-gram starting at t\[1\] and creates a hash for t\[1:8\].
    - The next unmarked tile is t\[2\].
- And it moves like this, one word down the set of tiles mapping t\[n, n+7\] until it gets to t\[9:16\].

At this point we have moved through all the 8-grams of the first string, and since it was the first time through there 
are no marked tokens going in or coming out. All the algorithm did was create hashses for all the 8-grams found in the
string. Now pass through the second string.

### Pass Through Second List of Tokens
The algorithm is looking for matches, and in particular matches of 8 tokens. It might actually find longer matches
then 8-tiles (not in this case) and it keeps track of this with the variable longest_maximal_match, which has been 
initialized to zero to keep track of these longer matches. The loop through the second string looks a lot like the 
traversal of the first string. It comes in and looks for the next unmarked tile starting at t\[0\].

- Initialize the loop:
    - Looks for the next unmarked token: there are none. 
- Token list for traversal is initialized to p\[0\]:
    - The next marked token is none, and the distance_to_next_tile returns the length of the list.
    - Take the first 8 words and join them into a string.
    - From the string create a hash for p\[0:7\].
    - Look for the hash, and it does not exists since there is no 8-gram match between our strings.
    - What is returned from the hash table is an empty list.
    - The next unmarked token is at p\[1\].
- Move to p\[1\] and then:
    - Next marked token is still none. It looks for next tile, and when it traverses the list and does not find one, 
distance_to_next_tile returns the length of the list.
    - Take the next 8-gram starting at p\[1\] and creates a hash for p\[1:8\].
    - Again look up the hash in the running hash table and there will be none for the 2 strings being considered.
    - What is returned from the hash table is an empty list.
    - The next unmarked token is now p\[2\].

In this way the algorithm works its way through the string. There are no matches across the strings and at the end of 
the traversing the second string the function scanpattern() returns to rkr_gst(). In rkr_gst() any strings that
were found are marked. In the first pass through in this case there were none found. 

### Decrease the Search Length in Half
The search length is shortened from 8 tiles to 4. You might be wondering why we didn't drop the search length to 7. The
algorithm is greedy and as it searches for matches across 4 tokens, if it finds longer ones it will handle those.
The function rkr_gst() returns us to scanpattern() and in traversing the strings there are 2 matches:
 - The first match is at t\[0:3\] and p\[0:3\] with longest_maximal_match equal to 4.
 - The second match is at t\[10:16\] and p\[8:14\] with longest_maximal_match equal to 7. 
 
For the second match in the list, the first 4 tokens are found to be the same, and the algorithm continues to compare 
tiles past t\[10:13\] and considers t\[10:14\]. It finds a match at this fifth tile, as well as the sixth and the
seventh. When it gets to the eighth tile there is no longer a match. The seven tiles are saved as a match, even though 
the initial search length was 4 tokens. This is the nature of the greedy string tiling. If you are familiar with 
regular expressions you will have seen this behavior before.

The function scanpattern() returns back to the rkr_gst() with the 2 sets of matching tiles. rkr_gst() calls 
mark_strings() and these tiles get marked and persisted in:
- mantok_t.is_marked = \[True, True, True, True, False, False, False, False, False, False, True, True, True, True, True, True, True\]
- mantok_p.is_marked = \[True, True, True, True, False, False, False, False, True, True, True, True, True, True, True, False, False, False, False\]

### Search Length set to Minimum Length
The search length is decreased to 3, its minimum value, and rk_gst() calls scanpattern(). Consider the traversal of the 
first string with the minimum search length. The 

- Initialize the loop:
    - Looks for the next unmarked token. Remember that therr was a match at t\[0:3\] and these tiles were marked after
    the last pass in scanpattern(). In that previous pass there were no matches and so the first unmarked tile was 
    none. Currently, the next unmarked tile is at t\[4\]. 
- Token list for traversal is at t\[4\]:
    - The next marked token is at t\[10\] because, again, in the previous pass through scanpattern() a match was found 
at t\[10:16\]. 
    - The distance to the next tile is (10+1)-4 or 7. This is greater than the search length of 3 and so there is work 
to do.
    - Take the first 3 words t\[4:6\] and join them into a string.
    - From the string create a hash.
    - The next unmarked token is at t\[5\].
- Move to t\[5\] and then:
    - Next marked token is t\[10\].
    - The distance to the next tile is (10+1)-5 or 6. This is greater than the search length of 3.
    - Take the next 3-gram starting at t\[5\] and create a hash for p\[5:7\].
    - The next unmarked token is now t\[6\].
- After creating the hash for t\[6:8\] the algorithm processes t\[7:9\], t\[8:10\], and ends up at t\[9\]:
    - Next marked token is t\[10\].
    - The distance to the next tile is (10+1)-9 or 2. This is less than the search length of 3.
    - Move to the next unmarked token.
    - The next unmarked token is none because the tiles t\[10:16\] have been marked previously.

At this point there are no more tiles to traverse, and the second string must be parsed looking for matches with the
search length 3. The process outlined above is continued, and there are no matches to find. scanpattern() returns to
rkr_gst() with no matches, and therefore no strings to mark. 

The function rkr_gst() has completed its task and returns to factory(). The last 2 strings have been compared and
matches stored in mantok_t. The last step is calculating the similarity metric. 

# Appendix A: Psuedo Code

The psuedo-code from the paper 
[Running Karp-Rabin Matching and Greedy String Tiling](http://sydney.edu.au/engineering/it/research/tr/tr463.pdf)
is provided here.

## Function rkr_gst()
The greedy string algorithm:

```
search-length s := initial-search-length
stop := false
Repeat
    L max := scanpattern(s)  # L max is size of largest maximal-matches found in iteration.
    if L max > 2 × s:
        s := L max  # Very long string; don’t mark tiles but try again with larger s
    else:
        markstrings(s)  # Create tiles from matches takes from list of queues
        if s > 2 × minimum_match_length:
            s := s div 2
        else if s > minimum_match_length:
            s := minimum_match_length
        else:
            stop := true
until stop
```

## Function scanpattern()
The Running Karp-Rabin matching algorithm is:

```
Starting at the ﬁrst unmarked token of T, for each unmarked T t do
    if distance to next tile ≤ s:
        advance t to ﬁrst unmarked token after next tile  # Just for efﬁciency.
    else:
        create the KR hash-value for substring T t ...  T t + s - 1 
        add to hashtable
Starting at the ﬁrst unmarked token of P, for each unmarked P p do
    if distance to next tile ≤ s:
        advance p to ﬁrst unmarked token after next tile
    else
        create the KR hash-value for substring P p ... P p + s - 1
        check hashtable for hash of KR hash-value
        for each hash-table entry with equal hashed KR hash-value do
            k: = s
            while P p + k = T t + k AND unmarked(P p + k ) AND unmarked(T t + k ) do
                k := k + 1  # Extend match until non-match or element marked.
            if k > 2 × s:
                return(k)  # Abandon scan. Will be restarted with s = k.
            else:
                record new maximal-match
return(length of longest maximal-match)
```

## Function mark_strings():
All matches must be tested element-by-element because just because 2 hash-values are the same does not guarantee
that the corresponding matches are the same. It has been observed that KR-hashing fails rarely and so the checking is
done here instead of in scanpattern, where it would normally reside, because it turns out to be far more efficient.

```
starting with the top queue, while there is a non-empty queue do
    if the current queue is empty:
        drop to next queue  # Corresponding to smaller maximal-matches
    else:
        remove match(p, t, L) from queue  # Assume the length of maximal-matches in the current queue is L.
        if match not occluded:
            if for all j: 0 . . . s - 1 ,P p + j = T t + j:  # Check that match is not hash artefact.
                for j:= 0 to L - 1 do
                    mark_token(P p + j )
                    mark_token(T t + j )
                    length_of_tokens_tiled := length_of_tokens_tiled + L
            else if L – L occluded ≥ s:  # This is the unmarked part remaining of the maximal-match.
                replace unmarked portion on list of queues
```

# Appendix B: Testing LinkedList()

Here is an example for loading and testing functionality of the doubly linked list.

- mylist = LinkedList()
- Load initial data.       
    - mylist.load_initial_data(2, '2')
    - mylist.load_initial_data(4, '4')
    - mylist.load_initial_data(6, '6')
    - mylist.load_initial_data(8, '8')
    - mylist.load_initial_data(10, '10')
- maximal_match_length = 10
    - Set root node: mylist.set_root(maximal_match_length)
    - Move down    : mylist.move_down()
- maximal_match_length = 2
    - Set root node: mylist.set_root(maximal_match_length)
- maximal_match_length = 7
    - Add data (11): mylist.add(maximal_match_length, '7')
- maximal_match_length = 2
- Set root node: mylist.set_root(maximal_match_length)
- print 'Move up      : mylist.move_up()
