#!/usr/bin/env python

from utils import remove
from augmentation import augment

with open("lexicon.txt") as f:
    for line in f:
        record = line.strip().split("#")[0].strip()
        if not record:
            continue
        p0, p1, p2, p3, p4, p5, p6, p7, code = record.split("|")
        print("{}:".format(p0))

        present = remove(p1[:-1]) if p1 != "?" else "unknown"
        future = remove(p2[:-1]) if p2 != "?" else "unknown"
        imperfect = augment(remove(p1[:-1])) if p1 != "?" else "unknown"
        future_passive = remove(p7[:-4]) if p7 != "?" else "unknown"

        print("    code: {}".format(code))
        print("    P: {}".format(present))
        print("    I: {}".format(imperfect))
        print("    F: {}".format(future))
        print("    FP: {}".format(future_passive))
