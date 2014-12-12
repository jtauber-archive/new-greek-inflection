import yaml
from verbs import Verb


LEXICON = {}


with open("lexicon.yaml") as f:
    for lemma, lexeme in yaml.load(f).items():
        LEXICON[lemma] = Verb(lexeme)


for lemma, verb in LEXICON.items():
    if "inherit" in verb.lexeme:
        verb.inherit = LEXICON.get(verb.lexeme["inherit"])
    else:
        verb.inherit = None
