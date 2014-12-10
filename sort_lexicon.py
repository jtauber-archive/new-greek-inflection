#!/usr/bin/env python

from pyuca import Collator
c = Collator()

preverbs = {}

with open("preverbs.txt") as f:
    for line in f:
        key, analysis = line.strip().split("|")
        preverbs[key] = analysis.split("+")


def sort_key(s):
    if s in preverbs:
        return c.sort_key(preverbs[s][-1] + "/" + s)
    else:
        return c.sort_key(s)

lexemes = []

current = None

with open("lexicon.yaml") as f:
    for line in f:
        if line[0] == " ":
            if current is None:
                raise Exception()
            current.append(line.rstrip())
        else:
            if current is not None:
                lexemes.append((sort_key(current[0].rstrip(":")), current))
            current = [line.rstrip()]
    # handle last current
    lexemes.append((sort_key(current[0].rstrip(":")), current))

for key, lexeme in sorted(lexemes):
    if lexeme[0].rstrip(":") in preverbs:
        print(lexeme[0] + "  #" + "+".join(preverbs[lexeme[0].rstrip(":")]))
    else:
        print(lexeme[0])
    print("\n".join(lexeme[1:]))
