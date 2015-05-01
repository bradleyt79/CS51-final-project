__author__ = 'bradleyt79'

import lexicon

# Note on Grammar Contents:
# Five English phrase types taken from Dictionary of English Grammar by Leech et al.
# Noun Phrase ​​​(det) + (modifier) + noun + (modifier)
# Verb Phrase ​​​(auxiliary) + verb
# Prepositional Phrase​​ preposition + noun phrase
# Adjective Phrase​​ (modifier) + adjective + (modifier)
# Adverb Phrase​​ (modifier) + adverb + (modifier)
#
# Clause​​​​ (conjunction) + (adverbial) + noun phrase + verb phrase + (indirect object)
# + (direct object) + (complement) + (adverbial)

# Note on Grammar Structure:
# The original inspiration was a CNF ( A -> B C) format of a CFG, although I have converted
# that to a series of classes that retain the A -> B C structure within their values. Still,
# this change means that any CNF CFGs would need to be modified to work with this parser.

# For Future Improvement:
# Modifiers and complements were taken out to simplify implementation.
# Needs better handling of abbreviations, e.g. Dr.

empty = ""

# Base Classes
class Terminal:
    def __init__(self):
        self.type = "Terminal"
        self.value = empty
        self.isempty = True

    def string(self):
        return self.value

    def structure(self):
        return None

    def parts(self):
        return [self.value]

    def add(self, token):
        self.value = token
        self.isempty = False
        return self.value

    def contains(self, wordtype):
        if self.type == wordtype:
            return True
        else:
            return False


class Phrase:
    def __init__(self):
        self.type = "Phrase"
        self.value = []
        self.isempty = True

    def string(self):
        return " ".join(x.string() for x in self.value)

    def structure(self):
        return [x.type for x in self.value]

    def parts(self):
        return [x.string() for x in self.value]

    def add(self, token):
        wordtype = lexicon.wordtype(token)
        # TODO clean bug with subphrases
        for x in self.value:
            if x.type == wordtype and x.value is empty:
                x.value = token
                return self
            elif x.type[-1] == "P":
                if x.add(token) is None:
                    continue
                else:
                    return self
            else:
                continue

        return None

    def contains(self, wordtype):
        for word in self.value:
            if word.type == wordtype:
                return True
            else:
                continue

        return False


# Terminal Subclasses
class N(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "N"


class V(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "V"
        
        
class Adj(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Adj"


class Adv(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Adv"
        

class Pron(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Pron"
    
    
class Prep(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Prep"
    
    
class Conj(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Conj"

    
class Aux(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Aux"
    
    
class Det(Terminal):
    def __init__(self):
        super().__init__()
        self.type = "Det"
    
    
# Phrase Subclasses (Non-Terminals)
class Mod(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "Mod"
        # self.value = PP() or AdvP() or AdjP()


class NP(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "NP"
        # self.value = [Det(), Mod(), N(), Mod()]
        self.value = [Det(), AdvP(), AdjP(), N()]


class VP(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "VP"
        self.value = [Aux(), V()]


class PP(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "PP"
        self.value = [Prep(), NP()]


class AdjP(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "AdjP"
        # self.value = [Mod(), Adj(), Mod()]
        self.value = [Adj()]


class AdvP(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "AdvP"
        # self.value = [Mod(), Adv(), Mod()]
        self.value = [Adv()]


class DO(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "DO"
        self.value = [NP()]


class IO(Phrase):
    def __init__(self):
        super().__init__()
        self.type = "IO"
        self.value = [PP()]


# Grammar Patterns - List of all Non-Terminal Patterns
patterns = [
    Conj(),
    NP(),
    VP(),
    PP(),
    AdjP(),
    AdvP()
]


# Clause Structure (Using clauses as roots, rather than sentences)
class C:
    def __init__(self):
        self.value = [Conj(), AdvP(), NP(), PP(), VP(), IO(), DO(), AdvP()]

empty_C = []

# Sentence Structure (implemented as clause lists)
S = []
empty_S = []


def print_grammar():
    for pattern in patterns:
        print(pattern)


def findphrase(word, phrasebank):
    wordtype = lexicon.wordtype(word)
    for phrase in phrasebank:
        if phrase.contains(wordtype):
            return phrase
        else:
            continue

    return None


def addtophrase(word, phrase):
    wordtype = lexicon.wordtype(word)
    if wordtype == phrase.type:
        # update phrase value
        phrase.add(word)
        return phrase
    elif type(phrase.value) is list:
        for subphrase in phrase.value:
            if wordtype == subphrase.type:
                # update phrase value
                phrase.add(word)
                return phrase
            else:
                continue
    else:
        return None

    return None


# Grammar Tests
def run_tests():
    test_sample = "The young boy in the chair is very hungry and eating a delicious hotdog quickly"
    test_tokens = test_sample.split()

    print(test_sample)
    # print_grammar()

    for token in test_tokens:
        # find wordtype
        wordtype = lexicon.wordtype(token)
        # print(wordtype)

        # find phrase
        found_phrase = findphrase(token, patterns)
        print("{}: {} - {}: {}".format(token, wordtype, found_phrase.type, found_phrase.structure()))

        # add to phrase
        new_phrase = addtophrase(token, found_phrase)
        print("{}: {} - {}".format(token, wordtype, new_phrase.parts()))


# run_tests()