import yaml
from verbs import Verb1


LEXICON = {}


# with open("lexicon.txt") as f:
#     for line in f:
#         record = line.strip().split("#")[0].strip()
#         if not record:
#             continue
#         p0, p1, p2, p3, p4, p5, p6, p7, code = record.split("|")
#         if code in ["1", "2", "3"]:
#             LEXICON[p0] = Verb1([p1, p2, p3, p4, p5, p6, p7])
#         else:
#             assert False


with open("lexicon.yaml") as f:
    for lemma, lexeme in yaml.load(f).items():
        LEXICON[lemma] = Verb1(lexeme)
