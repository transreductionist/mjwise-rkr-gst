class ManageTokens:

    def __init__(self, tokens):
        self.tokens = tokens
        self.length_of_tokens = len(tokens)
        self.is_marked = [False]*len(tokens)

    def mark_token(self, idx):
        if idx >= self.length_of_tokens:
            raise ValueError('Index greater than list length')
        if idx < 0:
            raise ValueError('Index must be positive')
        self.is_marked[idx] = True
        return True

    def unmark_token(self, idx):
        if idx >= self.length_of_tokens:
            raise ValueError('Index greater than list length')
        if idx < 0:
            raise ValueError('Index must be positive')
        self.is_marked[idx] = False
        return False

    def is_token_marked(self, idx):
        if idx >= self.length_of_tokens:
            raise ValueError('Index greater than list length')
        if idx < 0:
            raise ValueError('Index must be positive')
        if self.is_marked[idx]:
            return True
        else:
            return False

    def is_token_unmarked(self, idx):
        if idx >= self.length_of_tokens:
            raise ValueError('Index greater than list length')
        if idx < 0:
            raise ValueError('Index must be positive')
        if not self.is_marked[idx]:
            return True
        else:
            return False

    def index_of_next_marked_token(self, idx):
        """ Returns distance to next marked token. """

        # Step through indices of token list and check to see if marked.
        distance = 0
        while idx + distance <= self.length_of_tokens - 1:
            if self.is_token_marked(idx + distance):
                return idx + distance
            else:
                distance = distance + 1
        return None

    def index_of_next_unmarked_token(self, idx):
        """ Returns index of next unmarked token. """

        # Step through indices of tokens and check to see if unmarked.
        distance = 0
        while idx + distance <= self.length_of_tokens - 1:
            if self.is_token_unmarked(idx + distance):
                return idx + distance
            else:
                distance = distance + 1
        return None

    def get_tile(self, i, j):
        """ Returns slice of tokens. """

        return self.tokens[i:j]
