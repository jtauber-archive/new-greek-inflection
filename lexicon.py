import yaml
from verbs import Verb


LEXICON = {}


with open("lexicon.yaml") as f:
    for lemma, lexeme in yaml.load(f).items():
        LEXICON[lemma] = Verb(lexeme)
