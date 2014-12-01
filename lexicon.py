import yaml
from verbs import Verb1, Verb2


LEXICON = {}


with open("lexicon.yaml") as f:
    for lemma, lexeme in yaml.load(f).items():
        if lexeme["code"] in [1, 2, 3]:
            LEXICON[lemma] = Verb1(lexeme)
        elif lexeme["code"] in [4, 5]:
            LEXICON[lemma] = Verb2(lexeme)
