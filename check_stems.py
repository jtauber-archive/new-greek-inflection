#!/usr/bin/env python3

import os.path
import re
import yaml

from pyuca import Collator
c = Collator()


def _augment(stem):
    if stem.startswith("ἀ"):
        return "ἠ" + stem[1:]
    elif stem.startswith("ἁ"):
        return "ἡ" + stem[1:]
    elif stem.startswith("αἰ"):
        return "ᾐ" + stem[2:]
    elif stem.startswith("αἱ"):
        return "ᾑ" + stem[2:]
    elif stem.startswith("αὐ"):
        return "ηὐ" + stem[2:]
    elif stem.startswith("ἐ"):
        return "ἠ" + stem[1:]
    elif stem.startswith("ἑ"):
        return "ἡ" + stem[1:]
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


def orthography(stem):
    if stem.endswith(("πσ", "φσ")):
        return stem[:-2] + "ψ"
    elif stem.endswith(("κσ", "χσ")):
        return stem[:-2] + "ξ"
    else:
        return stem


class Stems:

    root1regex = ".+$"

    @property
    def root1b(self): return self.root1
    @property
    def root1c(self): return self.root1b
    @property
    def root1d(self): return self.root1c

    @property
    def P(self): return self.root1
    @property
    def I(self): return augment(self.root1)
    @property
    def F(self): return orthography(self.root1b + "σ")
    @property
    def FP(self): return self.root1c + "θη" + "σ"
    @property
    def A(self): return augment(self.AN)
    @property
    def AN(self): return orthography(self.root1b + "σ")
    @property
    def AP(self): return augment(self.APN)
    @property
    def APN(self): return self.root1c + "θη!"
    @property
    def X(self): return redup(self.root1b + "κ")
    @property
    def XM(self): return redup(self.root1d)
    @property
    def Y(self): return redup(self.root1b + "κ")
    @property
    def YM(self): return redup(self.root1b)  # @@@ or root1d?

    def stems(self, lexeme):
        self.root1 = lexeme["root1"]

        if re.match(self.root1regex, self.root1):
            return {
                key: getattr(self, key)
                for key in ["P", "I", "F", "FP", "A", "AN", "AP", "APN", "X", "XM", "Y", "YM"]
            }


class Stems0a(Stems):

    "//σ"

    root1regex = ".+[^υλρκχπφαεο]$"

    @property
    def root1c(self): return self.root1b + "σ"


class Stems0eu(Stems):

    "ευ/ευ/ευ"

    root1regex = ".+ευ$"


class Stems0u(Stems):

    "υ/υ/υ"

    root1regex = ".+υ$"


class Stems0u2(Stems):

    "υ/υ/υσ"

    root1regex = ".+υ$"

    @property
    def root1c(self): return self.root1b + "σ"


class Stems0b(Stems):

    "ζ//σ"

    root1regex = ".+ζ$"

    @property
    def root1b(self): return self.root1[:-1]

    @property
    def root1c(self): return self.root1b + "σ"


class Stems0c(Stems):

    "λ/λ/λη"

    root1regex = ".+λ$"

    @property
    def root1c(self): return self.root1b + "η"


class Stems0r(Stems):

    "ρ/ρη/ρη"

    root1regex = ".+ρ$"

    @property
    def root1b(self): return self.root1 + "η"


class Stems0d(Stems):

    "σκ//"

    root1regex = ".+σκ$"

    @property
    def root1b(self): return self.root1[:-2]


class Stems0e(Stems):

    "πτ/π/φ"

    root1regex = ".+πτ$"

    @property
    def root1b(self): return self.root1[:-1]

    @property
    def root1c(self): return self.root1[:-2] + "φ"


class Stems0f(Stems):

    "κ/κ/χ"

    root1regex = ".+[^σ]κ$"

    @property
    def root1c(self): return self.root1[:-1] + "χ"


class Stems0g(Stems):

    "χ/χ/χ/κ"

    root1regex = ".+χ$"

    @property
    def root1d(self): return self.root1[:-1] + "κ"


class Stems0p(Stems):

    "π/π/π"

    root1regex = ".+π$"


class Stems0ph(Stems):

    "φ/φ/φ"

    root1regex = ".+φ$"


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
    "lexicon0w.yaml",
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
    "0c": Stems0c,
    "0r": Stems0r,
    "0d": Stems0d,
    "0e": Stems0e,
    "0f": Stems0f,
    "0g": Stems0g,
    "0eu": Stems0eu,
    "0p": Stems0p,
    "0ph": Stems0ph,
    "0u": Stems0u,
    "0u2": Stems0u2,
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

            if "class" not in lexeme:
                continue
            # assert "class" in lexeme, lemma

            stems = stem_classes[lexeme["class"]]().stems(lexeme)

            if stems is None:
                raise Exception("{} doesn't match class".format(lemma))

            for key in stems:
                if key in lexeme:
                    assert lexeme[key] == stems[key], (lemma, key, stems[key], lexeme[key])


filename = "lexicon0w.yaml"

with open(os.path.join("lexica", filename)) as f:
    for lemma, lexeme in sorted(yaml.load(f).items(), key=lambda x: c.sort_key(x[0])):
        if "prefix" in lexeme:
            continue

        assert "root1" in lexeme, lemma
        first = True

        for stem_class in stem_classes.values():
            fail = False
            stems = stem_class().stems(lexeme)

            if stems:
                for key in stems:
                    if key in lexeme:
                        if lexeme[key] != stems[key]:
                            fail = True
                            break
                if not fail:
                    if "class" in lexeme:
                        continue
                    if first:
                        print("{}:".format(lemma))
                    first = False
                    print("    {}".format(stem_class.__name__))
