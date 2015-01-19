#!/usr/bin/env python3

import os.path
import re
import yaml


def _augment(stem):
    if stem.startswith("ἀ"):
        return "ἠ" + stem[1:]
    elif stem.startswith("ἁ"):
        return "ἡ" + stem[1:]
    elif stem.startswith("αἰ"):
        return "ᾐ" + stem[2:]
    elif stem.startswith("αὐ"):
        return "ηὐ" + stem[2:]
    elif stem.startswith("ἐ"):
        return "ἠ" + stem[1:]
    elif stem.startswith("ὀ"):
        return "ὠ" + stem[1:]
    elif stem.startswith("ὁ"):
        return "ὡ" + stem[1:]
    elif stem.startswith("οἰ"):
        return "ᾠ" + stem[2:]
    elif stem.startswith(("εἰ", "εὐ", "ἠ", "ἡ", "ἰ", "ἱ", "ὑ", "ὠ")):
        return stem
    else:
        return None


def augment(stem):
    return _augment(stem) or "ἐ" + stem


redup_table = str.maketrans("φθ", "πτ")


def redup(stem):
    return _augment(stem) or stem[0].translate(redup_table) + "ε" + stem


class Stems:

    root1regex = ".+$"

    @property
    def root1b(self): return self.root1
    @property
    def root1c(self): return self.root1b

    @property
    def P(self): return self.root1
    @property
    def I(self): return augment(self.root1)
    @property
    def F(self): return self.root1b + "σ"
    @property
    def FP(self): return self.root1c + "θη" + "σ"
    @property
    def A(self): return augment(self.root1b + "σ")
    @property
    def AN(self): return self.root1b + "σ"
    @property
    def AP(self): return augment(self.root1c + "θη!")
    @property
    def APN(self): return self.root1c + "θη!"
    @property
    def X(self): return redup(self.root1b + "κ")
    @property
    def XM(self): return redup(self.root1c)
    @property
    def Y(self): return redup(self.root1b + "κ")
    @property
    def YM(self): return redup(self.root1b)  # @@@ or root1c?

    def stems(self, lexeme):
        self.root1 = lexeme["root1"]

        if re.match(self.root1regex, self.root1):
            return {
                key: getattr(self, key)
                for key in ["P", "I", "F", "FP", "A", "AN", "AP", "APN", "X", "XM", "Y", "YM"]
            }


class Stems0a(Stems):

    "//σ"

    @property
    def root1c(self): return self.root1b + "σ"


class Stems0b(Stems):

    "ζ//σ"

    root1regex = ".+ζ$"

    @property
    def root1b(self): return self.root1[:-1]

    @property
    def root1c(self): return self.root1b + "σ"


class Stems1ab(Stems):

    "ε/η/η"

    root1regex = ".+ε$"

    @property
    def root1b(self): return self.root1[:-1] + "η"


class Stems1c(Stems):

    "ε/ε/εσ"

    root1regex = ".+ε$"

    @property
    def root1c(self): return self.root1b + "σ"


class Stems2a(Stems):

    "α/η/η"

    root1regex = ".+α$"

    @property
    def root1b(self): return self.root1[:-1] + "η"


class Stems2b(Stems):

    "α/η/ησ"

    root1regex = ".+α$"

    @property
    def root1c(self): return self.root1 + "σ"


class Stems2c(Stems):

    "α/α/α"

    root1regex = ".+α$"


class Stems3a(Stems):

    "ο/ω/ω"

    root1regex = ".+ο$"

    @property
    def root1b(self): return self.root1[:-1] + "ω"


file_list = [
    "lexicon0a.yaml",
    "lexicon0b.yaml",
    "lexicon1a.yaml",
    "lexicon1b.yaml",
    "lexicon1c.yaml",
    "lexicon2a.yaml",
    "lexicon2b.yaml",
    "lexicon2c.yaml",
    "lexicon3a.yaml",
]


stem_classes = {
    "0a": Stems0a,
    "0b": Stems0b,
    "1a": Stems1ab,
    "1c": Stems1c,
    "2a": Stems2a,
    "2b": Stems2b,
    "2c": Stems2c,
    "3a": Stems3a,
}


for filename in file_list:
    with open(os.path.join("lexica", filename)) as f:
        for lemma, lexeme in yaml.load(f).items():
            if "prefix" in lexeme:
                continue

            assert "root1" in lexeme, lemma
            assert "class" in lexeme, lemma

            stems = stem_classes[lexeme["class"]]().stems(lexeme)

            for key in stems:
                if key in lexeme:
                    assert lexeme[key] == stems[key], (lemma, key, stems[key], lexeme[key])


# filename = "lexiconxx.yaml"
#
# with open(os.path.join("lexica", filename)) as f:
#     for lemma, lexeme in yaml.load(f).items():
#         if "prefix" in lexeme:
#             continue
#
#         assert "root1" in lexeme, lemma
#
#         print("{}:".format(lemma))
#         for stem_class in [Stems0a, Stems0b, Stems1ab, Stems1c, Stems2a, Stems2b, Stems2c, Stems3a]:
#             fail = False
#             stems = stem_class().stems(lexeme)
#
#             if stems:
#                 for key in stems:
#                     if key in lexeme:
#                         if lexeme[key] != stems[key]:
#                             fail = True
#                             break
#                 if not fail:
#                     print("    {}".format(stem_class.__name__))
