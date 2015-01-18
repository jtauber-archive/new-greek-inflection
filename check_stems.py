#!/usr/bin/env python3

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
    elif stem.startswith(("εἰ", "εὐ", "ἠ", "ἡ", "ὑ", "ὠ")):
        return stem
    else:
        return None


def augment(stem):
    return _augment(stem) or "ἐ" + stem


redup_table = str.maketrans("φθ", "πτ")

def redup(stem):
    return _augment(stem) or stem[0].translate(redup_table) + "ε" + stem


def stems0a(lexeme):
    root1 = lexeme["root1"]

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1 + "σ",
        FP = root1 + "σ" + "θη" + "σ",
        A = augment(root1 + "σ"),
        AN = root1 + "σ",
        AP = augment(root1 + "σ" + "θη!"),
        APN = root1 + "σ" + "θη!",
        X = redup(root1 + "κ"),
        XM = redup(root1 + "σ"),
        Y = redup(root1 + "κ"),  # @@@
        YM = redup(root1),  # @@@
    )

    return stems


def stems0b(lexeme):
    root1 = lexeme["root1"]

    assert root1.endswith("ζ"), (lemma, root1)

    root1b = root1[:-1]

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1b + "σ",
        FP = root1b + "σ" + "θη" + "σ",
        A = augment(root1b + "σ"),
        AN = root1b + "σ",
        AP = augment(root1b + "σ" + "θη!"),
        APN = root1b + "σ" + "θη!",
        X = redup(root1 + "κ"),  # @@@
        XM = redup(root1b + "σ"),
        Y = redup(root1 + "κ"),  # @@@
        YM = redup(root1),  # @@@
    )

    return stems


def stems1ab(lexeme):
    root1 = lexeme["root1"]

    assert root1.endswith("ε"), (lemma, root1)

    root1b = root1[:-1] + "η"

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1b + "σ",
        FP = root1b + "θη" + "σ",
        A = augment(root1b + "σ"),
        AN = root1b + "σ",
        AP = augment(root1b + "θη!"),
        APN = root1b + "θη!",
        X = redup(root1b + "κ"),
        XM = redup(root1b),
        Y = redup(root1b + "κ"),  # @@@
        YM = redup(root1b),  # @@@
    )

    return stems


def stems1c(lexeme):
    root1 = lexeme["root1"]

    assert root1.endswith("ε"), (lemma, root1)

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1 + "σ",
        FP = root1 + "σ" + "θη" + "σ",
        A = augment(root1 + "σ"),
        AN = root1 + "σ",
        AP = augment(root1 + "σ" + "θη!"),
        APN = root1 + "σ" + "θη!",
        X = redup(root1 + "κ"),
        XM = redup(root1 + "σ"),
        Y = redup(root1 + "κ"),  # @@@
        YM = redup(root1),  # @@@
    )

    return stems


def stems2a(lexeme):
    root1 = lexeme["root1"]

    assert root1.endswith("α"), (lemma, root1)

    root1b = root1[:-1] + "η"

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1b + "σ",
        FP = root1b + "θη" + "σ",
        A = augment(root1b + "σ"),
        AN = root1b + "σ",
        AP = augment(root1b + "θη!"),
        APN = root1b + "θη!",
        X = redup(root1b + "κ"),
        XM = redup(root1b),
        Y = redup(root1b + "κ"),  # @@@
        YM = redup(root1b),  # @@@
    )

    return stems


def stems2b(lexeme):
    root1 = lexeme["root1"]

    assert root1.endswith("α"), (lemma, root1)

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1 + "σ",
        FP = root1 + "σ" + "θη" + "σ",
        A = augment(root1 + "σ"),
        AN = root1 + "σ",
        AP = augment(root1 + "σ" + "θη!"),
        APN = root1 + "σ" + "θη!",
        X = redup(root1 + "κ"),
        XM = redup(root1 + "σ"),
        Y = redup(root1 + "κ"),  # @@@
        YM = redup(root1),  # @@@
    )

    return stems


def stems2c(lexeme):
    root1 = lexeme["root1"]

    assert root1.endswith("α"), (lemma, root1)

    stems = dict(
        P = root1,
        I = augment(root1),
        F = root1 + "σ",
        FP = root1 + "θη" + "σ",
        A = augment(root1 + "σ"),
        AN = root1 + "σ",
        AP = augment(root1 + "θη!"),
        APN = root1 + "θη!",
        X = redup(root1 + "κ"),
        XM = redup(root1),
        Y = redup(root1 + "κ"),  # @@@
        YM = redup(root1),  # @@@
    )

    return stems


file_list = [
    "lexicon0a.yaml",
    "lexicon0b.yaml",
    "lexicon1a.yaml",
    "lexicon1b.yaml",
    "lexicon1c.yaml",
    "lexicon2a.yaml",
    "lexicon2b.yaml",
    "lexicon2c.yaml",
]


for filename in file_list:
    with open(filename) as f:
        for lemma, lexeme in yaml.load(f).items():
            if "prefix" in lexeme:
                continue

            assert "root1" in lexeme, lemma

            if filename in ["lexicon0a.yaml"]:
                stems = stems0a(lexeme)
            elif filename in ["lexicon0b.yaml"]:
                stems = stems0b(lexeme)
            elif filename in ["lexicon1a.yaml", "lexicon1b.yaml"]:
                stems = stems1ab(lexeme)
            elif filename in ["lexicon1c.yaml"]:
                stems = stems1c(lexeme)
            elif filename in ["lexicon2a.yaml"]:
                stems = stems2a(lexeme)
            elif filename in ["lexicon2b.yaml"]:
                stems = stems2b(lexeme)
            elif filename in ["lexicon2c.yaml"]:
                stems = stems2c(lexeme)

            for key in stems:
                if key in lexeme:
                    assert lexeme[key] == stems[key], (lemma, key, stems[key], lexeme[key])
