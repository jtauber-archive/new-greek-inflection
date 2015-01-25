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
    elif stem.startswith("ῥ"):
        return "ἐρ" + stem[1:]  # @@@ or ἐρρ
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
    if stem.endswith(("βσ", "πσ", "φσ")):
        return stem[:-2] + "ψ"
    elif stem.endswith(("γσ", "κσ", "χσ")):
        return stem[:-2] + "ξ"
    else:
        return stem


class StemsBase:

    root1regex = ".+$"

    def stems(self, lexeme):
        self.root1 = lexeme["root1"]

        if re.match(self.root1regex, self.root1):

            if "root2" in lexeme:
                self.root2_override = lexeme["root2"]
            if "root3" in lexeme:
                self.root3_override = lexeme["root3"]
            if "root3post" in lexeme:
                self.root3post_override = lexeme["root3post"]
            if "root4" in lexeme:
                self.root4_override = lexeme["root4"]
            if "root4post" in lexeme:
                self.root4post_override = lexeme["root4post"]
            if "root5" in lexeme:
                self.root5_override = lexeme["root5"]
            if "root6" in lexeme:
                self.root6_override = lexeme["root6"]

            return {
                key: getattr(self, key)
                for key in ["P", "I", "F", "FP", "A", "AN", "AP", "APN", "X", "XM", "Y", "YM"]
            }


class Stems(StemsBase):

    root1regex = ".+$"

    @property
    def root2(self):
        if hasattr(self, "root2_override"):
            return self.root2_override
        else:
            return self.root1

    @property
    def root3(self):
        if hasattr(self, "root3_override"):
            return self.root3_override
        else:
            return self.root2

    @property
    def root4(self):
        if hasattr(self, "root4_override"):
            return self.root4_override
        else:
            return self.root2

    @property
    def root5(self):
        if hasattr(self, "root5_override"):
            return self.root5_override
        else:
            return self.root4

    @property
    def root6(self):
        if hasattr(self, "root6_override"):
            return self.root6_override
        else:
            return self.root3 + "θ"

    # first principal part

    @property
    def root1post(self):
        if hasattr(self, "root1post_override"):
            return self.root1post_override
        else:
            return self.root1

    @property
    def P(self): return self.root1post

    @property
    def I(self): return augment(self.root1post)

    # second principal part

    @property
    def root2post(self):
        if hasattr(self, "root2post_override"):
            return self.root2post_override
        else:
            return orthography(self.root2 + "σ")

    @property
    def F(self): return self.root2post

    # third principal part

    @property
    def root3post(self):
        if hasattr(self, "root3post_override"):
            return self.root3post_override
        else:
            return orthography(self.root3 + "σ")

    @property
    def AN(self): return self.root3post

    @property
    def A(self): return augment(self.root3post)

    # fourth principal part

    @property
    def root4post(self):
        if hasattr(self, "root4post_override"):
            return self.root4post_override
        else:
            return self.root4 + "κ"

    @property
    def X(self): return redup(self.root4post)

    @property
    def Y(self): return redup(self.root4post)

    # fifth principal part

    @property
    def root5post(self):
        if hasattr(self, "root5post_override"):
            return self.root5post_override
        else:
            return self.root5

    @property
    def XM(self): return redup(self.root5post)

    @property
    def YM(self): return redup(self.root5post)

    # sixth principal part

    @property
    def root6postA(self):
        if hasattr(self, "root6postA_override"):
            return self.root6postA_override
        else:
            return self.root6 + "η!"

    @property
    def root6postF(self):
        if hasattr(self, "root6postF_override"):
            return self.root6postF_override
        else:
            return self.root6 + "ησ"

    @property
    def APN(self): return self.root6postA

    @property
    def AP(self): return augment(self.root6postA)

    @property
    def FP(self): return self.root6postF


class Stems0a(Stems):

    root1regex = ".+[^αεουκλμνπρχφ!]$"

    @property
    def root5(self): return self.root4 + "σ"

    @property
    def root6(self): return self.root2 + "σθ"


class Stems0eu(Stems):

    root1regex = ".+ευ$"


class Stems0u(Stems):

    root1regex = ".*[^ε]υ$"


class Stems0u2(Stems):

    root1regex = ".+[^ε]υ$"

    @property
    def root6(self): return self.root2 + "σθ"


class Stems0b(Stems):

    root1regex = ".+ζ$"

    @property
    def root2(self): return self.root1[:-1]

    @property
    def root5(self): return self.root4 + "σ"

    @property
    def root6(self): return self.root2 + "σθ"


class Stems0wiz(Stems):

    root1regex = ".+ῳζ$"

    @property
    def root2(self): return self.root1[:-2] + "ω"

    @property
    def root5(self): return self.root2 + "σ"


class Stems0d(Stems):

    root1regex = ".+σκ$"

    @property
    def root2(self): return self.root1[:-2]


class Stems0e(Stems):

    root1regex = ".+πτ$"

    @property
    def root2(self): return self.root1[:-1]

    @property
    def root6(self): return self.root2[:-1] + "φθ"


class Stems0f(Stems):

    root1regex = ".+[^σ]κ$"

    @property
    def root6(self): return self.root1[:-1] + "χθ"


class Stems0g(Stems):

    root1regex = ".+χ$"

    @property
    def root5(self): return self.root1[:-1] + "κ"


class Stems0p(Stems):

    root1regex = ".+π$"

    @property
    def root6(self): return self.root1[:-1] + "φθ"


class Stems0ph(Stems):

    root1regex = ".+φ$"


class Stems1ab(Stems):

    root1regex = ".+ε$"

    @property
    def root2(self): return self.root1[:-1] + "η"


class Stems1c(Stems):

    root1regex = ".+ε$"

    @property
    def root5(self): return self.root2 + "σ"

    @property
    def root6(self): return self.root2 + "σθ"


class Stems2a(Stems):

    root1regex = ".+α$"

    @property
    def root2(self): return self.root1[:-1] + "η"


class Stems2b(Stems):

    root1regex = ".+α$"

    @property
    def root6(self): return self.root1 + "σθ"


class Stems2c(Stems):

    "α/α/α"

    root1regex = ".+α$"


class Stems3a(Stems):

    root1regex = ".+ο$"

    @property
    def root2(self): return self.root1[:-1] + "ω"


class Stems0l(Stems):

    root1regex = ".+λ$"

    @property
    def root2(self): return self.root1 + "η"


class Stems5l(Stems):

    root1regex = ".+λ$"

    @property
    def root2post(self): return self.root2 + "#"

    @property
    def root3post(self): return self.root3


class Stems5r(Stems):

    root1regex = ".+ρ$"

    @property
    def root2post(self): return self.root2 + "#"

    @property
    def root3post(self): return self.root3


class Stems5r2(Stems):

    root1regex = ".+ρ$"

    @property
    def root2(self): return self.root1 + "η"

    @property
    def root3post(self): return self.root3


class Stems5m(Stems):

    root1regex = ".+μ$"

    @property
    def root2(self): return self.root1 + "η"

    @property
    def root3post(self): return self.root3


class Stems5n(Stems):

    root1regex = ".+[^ιυ]ν$"

    @property
    def root2post(self): return self.root2 + "#"

    @property
    def root4(self): return self.root2 + "η"

    @property
    def root3post(self): return self.root3


class Stems5ain(Stems):

    root1regex = ".+αιν$"

    @property
    def root2(self): return self.root1.replace("αιν", "αν")

    @property
    def root2post(self): return self.root2 + "#"

    @property
    def root3post(self): return self.root3


class Stems5in(Stems):

    root1regex = ".+[^α]ν$"

    @property
    def root2post(self): return self.root2 + "#"

    @property
    def root3post(self): return self.root3


class Stems5un(Stems):

    root1regex = ".+υν$"

    @property
    def root2post(self): return self.root2 + "#"

    @property
    def root3post(self): return self.root3


class Stems6a(Stems):

    root1regex = ".+!$"

    @property
    def root2post(self): return self.root2.replace("!", "") + "σ"  # @@@

    @property
    def root3post(self): return self.root3

    @property
    def root6(self): return self.root2.replace("!", "") + "σθ"


class Stems6nu(Stems):

    root1regex = ".+[^ν]νυ!$"

    @property
    def root2(self): return self.root1.replace("νυ!", "")


class Stems6nnu(Stems):

    root1regex = ".+ννυ!$"

    @property
    def root2(self): return self.root1.replace("ννυ!", "")


class Stems0i_sk(Stems):

    root1regex = ".ι.+σκ$"

    @property
    def root3(self): return self.root1[2:-2]

    @property
    def root3post(self): return self.root3 + "!"


file_list = [
    "lexicon.yaml",
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
    "lexicon4w.yaml",
    "lexicon5w.yaml",
    "lexicon6w.yaml",
    "lexicon7w.yaml",
]


stem_classes = {
    "basic": Stems,
    "0a": Stems0a,
    "0b": Stems0b,
    "0wiz": Stems0wiz,
    "0d": Stems0d,
    "0e": Stems0e,
    "0f": Stems0f,
    "0g": Stems0g,
    "0eu": Stems0eu,
    "0p": Stems0p,
    "0ph": Stems0ph,
    "0u": Stems0u,
    "0u2": Stems0u2,
    "0i.sk": Stems0i_sk,
    "1a": Stems1ab,
    "1c": Stems1c,
    "2a": Stems2a,
    "2b": Stems2b,
    "2c": Stems2c,
    "3a": Stems3a,
    "0l": Stems0l,
    "5l": Stems5l,
    "5r": Stems5r,
    "5r2": Stems5r2,
    "5m": Stems5m,
    "5n": Stems5n,
    "5ain": Stems5ain,
    "5in": Stems5in,
    "5un": Stems5un,
    "6a": Stems6a,
    "6nu": Stems6nu,
    "6nnu": Stems6nnu,
}


for filename in file_list:
    with open(os.path.join("lexica", filename)) as f:
        for lemma, lexeme in yaml.load(f).items():
            if "inherit" in lexeme:
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
                    assert lexeme[key] == stems[key], (lemma, key, stems[key], lexeme[key], lexeme["class"])


filename = "lexicon.yaml"

with open(os.path.join("lexica", filename)) as f:
    for lemma, lexeme in sorted(yaml.load(f).items(), key=lambda x: c.sort_key(x[0])):
        if "inherit" in lexeme:
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
