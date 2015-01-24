#!/usr/bin/env python

from lexicon import LEXICON

class_count = 0
root_count = 0
total_count = 0

for lemma, verb in LEXICON.items():
    total_count += 1
    if "class" in verb.lexeme:
        class_count += 1
    if "root1" in verb.lexeme:
        root_count += 1

    if "inherit" in verb.lexeme:
        if "class" in verb.inherit.lexeme:
            class_count += 1
        if "root1" in verb.inherit.lexeme:
            root_count += 1
        if "inherit" in verb.inherit.lexeme:
            if "class" in verb.inherit.inherit.lexeme:
                class_count += 1
            if "root1" in verb.inherit.inherit.lexeme:
                root_count += 1

print(class_count)
print(root_count)
print(total_count)
print(1853)
