"""
Code for loading in the lexicon.
"""

import os.path
import yaml

from verbs import Verb


LEXICA_DIR = "lexica"


LEXICON = {}

LEXICON_FILES = [
    "lexicon.yaml",
    "lexicon0a.yaml",
    "lexicon0b.yaml",
    "lexicon0x.yaml",
    "lexicon1a.yaml",
    "lexicon1b.yaml",
    "lexicon1c.yaml",
    "lexicon1x.yaml",
    "lexicon2a.yaml",
    "lexicon2b.yaml",
    "lexicon2c.yaml",
    "lexicon2x.yaml",
    "lexicon3a.yaml",
]

for lexicon_filename in LEXICON_FILES:
    with open(os.path.join(LEXICA_DIR, lexicon_filename)) as f:
        for lemma, lexeme in yaml.load(f).items():
            LEXICON[lemma] = Verb(lexeme)


for lemma, verb in LEXICON.items():
    if "inherit" in verb.lexeme:
        verb.inherit = LEXICON.get(verb.lexeme["inherit"])
    else:
        verb.inherit = None
