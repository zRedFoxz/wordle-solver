from WordleWords import get_all_words

class Wordle:
    def __init__(self):
        self.letters = set()
        self.inv_letters = set()
        self.placement = {}
        self.inv_placement = {}

    def __add__(self, other):
        if other is None:
            return self

        # merge the two new sets of correct & incorrect letters
        self.letters = self.letters.union(other.letters)
        self.inv_letters = self.inv_letters.union(other.inv_letters)

        # combine all placement data:
        # combine the individual letter arrays 
        new_placement = {**self.placement, **other.placement}
        for c in new_placement:
            if c in self.placement and c in other.placement:
    	        new_placement[c] = self.placement[c].union(other.placement[c])
    
        new_inv_placement = {**self.inv_placement, **other.inv_placement}
        for c in new_inv_placement:
            if c in self.inv_placement and c in other.inv_placement:
    	        new_inv_placement[c] = self.inv_placement[c].union(other.inv_placement[c])
    
        self.placement = new_placement
        self.inv_placement = new_inv_placement
        return self

    def __str__(self):
        return f'Letters:{self.letters}\nInvalid Letters:{self.inv_letters}\nplacement:{self.placement}\ninvalid placement:{self.inv_placement}'

    @staticmethod
    def the_game(answer, guess):
        result = Wordle()
        pos = 0
        for c in guess:
            if c in answer:
                result.letters.add(c)
                if answer[pos] == guess[pos]:
                    if c in result.placement:
                        result.placement[c].add(pos)
                    else:
                        result.placement[c] = {pos}
                else:
                    if c in result.inv_placement:
                        result.inv_placement[c].add(pos)
                    else:
                        result.inv_placement[c] = {pos}
            else:
                result.inv_letters.add(c)
            pos = pos + 1

        return result

    # Suppose you don't know the word, but want to play the game for real
    # gen-info, given your guess, and the result of the guess, will return the "info"
    # structure used to feed the rest of the program.
    # The "result" format must be the same length as guess, and must only use X Y or G:
    # X means "invalid letter" for that position
    # Y means "Yellow" letter for that position (valid but wrong placement)
    # G means "Green" letter for that placement (valid and correct placement)
    @staticmethod
    def guess_info(result, guess):
        result = result.lower()
        info = Wordle()
        pos = 0
    
        for c in result:
            if c == "x":
                info.inv_letters.add(guess[pos])
            elif c == "g":
                info.letters.add(guess[pos])
                if guess[pos] in placement:
                    info.placement[guess[pos]].add(pos)
                else:
                    info.placement[guess[pos]] = {pos}
            elif c == "y":
                info.letters.add(guess[pos])
                if guess[pos] in info.inv_placement:
                    info.inv_placement[guess[pos]].add(pos)
                else:
                    info.inv_placement[guess[pos]] = {pos}
            else:
                print("Results format invalid: '{}'".format(result))
                return None
            pos = pos + 1

        return info

def guess_iterative(the_word, valid_words, init_guess = None):
    info = Wordle()
    correct = False
    guessable_words = valid_words
    if init_guess is None:
        guess = guessable_words[0]
    else:
        guess = init_guess
    guesses = 1
    while not correct:
        print("Guess #" + str(guesses) + ": " + guess)
        result = Wordle.the_game(the_word, guess)
        guesses = guesses + 1

        info = info + result

        guessable_words = filter_words(guessable_words, info)
        guess = guessable_words[0]
        # check if incorrect set is empty - in which case guess is correct
        if not result.inv_letters:
            print("Got it!")
            correct = True
            print(info)

#def merge_info(cumulative, new):
def filter_words(valid_words, info):
    filtered = []
    for word in valid_words:
        # If there are invalid letters, use that information too
        if filter_incorrect(word, info.inv_letters):
            continue

        if filter_invalid_placement(word, info.inv_placement):
            continue

        if not filter_letters(word, info.letters):
            continue

        # If there is placement information - use it to sort:
        if not filter_placement(word, info.placement):
            continue

        filtered.append(word)
    return filtered

# Returns true if word meets placement criteria
def filter_placement(word, placement):
    # For each letter in the placement mapping, check to see if the word
    # meets the letter placement criteria (if any)
    for c in placement:
        for position in placement[c]:
            if word[position] is not c:
                return False
    return True

# returns true if word contains any character placed in the placement criteria
def filter_invalid_placement(word, placement):
    for c in placement:
        for position in placement[c]:
            if word[position] == c:
                return True
    return False

# Returns true if any letter in the list are in 'word'
def filter_incorrect(word, incorrect):
    for c in incorrect:
        if c in word:
            return True
    return False

# Returns true if all letters in the list are in 'word'
def filter_letters(word, letters):
    for c in letters:
        if c not in word:
            return False
    return True

# User WordleWords to get the list of available words
all_words = get_all_words()
sorted_all_words = sorted(all_words)
the_word = "ulcer"
guess = "crane"
the_word = the_word.lower()
guess = guess.lower()

guess_iterative(the_word, sorted_all_words, guess)