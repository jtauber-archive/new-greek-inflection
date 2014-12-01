from accentuation import recessive
from endings import PRIMARY_ACTIVE, PRIMARY_ACTIVE_ALPHA, PRIMARY_ACTIVE_EPSILON, PRIMARY_ACTIVE_OMICRON
from endings import PRIMARY_MIDDLE, PRIMARY_MIDDLE_ALPHA, PRIMARY_MIDDLE_EPSILON, PRIMARY_MIDDLE_OMICRON
from endings import SECONDARY_ACTIVE, SECONDARY_ACTIVE_ALPHA, SECONDARY_ACTIVE_EPSILON, SECONDARY_ACTIVE_OMICRON
from endings import SECONDARY_MIDDLE, SECONDARY_MIDDLE_ALPHA, SECONDARY_MIDDLE_EPSILON, SECONDARY_MIDDLE_OMICRON
from utils import remove, has_accent, remove_length


def ENDINGS(default, alpha, epsilon, omicron):

    def forward(stem):
        if stem is None:
            return None

        stem2, paradigm = {
            "α": (stem[:-1], alpha),
            "ε": (stem[:-1], epsilon),
            "ο": (stem[:-1], omicron),
        }.get(stem[-1], (stem, default))

        return {
            pn: [stem2 + ending for ending, stem_ending in (endings if isinstance(endings, list) else [endings])]
            for pn, endings in paradigm.items()
        }

    def reverse(form, pn):
        stems = []
        for paradigm in [default, alpha, epsilon, omicron]:
            if pn in paradigm:
                endings = paradigm[pn]
                for ending, stem_ending in (endings if isinstance(endings, list) else [endings]):
                    if form.endswith(remove_length(ending)):
                        stems.append(form[:-len(ending)] + (stem_ending if stem_ending else ""))

        if stems:
            return stems
        else:
            raise Exception("got a {} of form {}".format(pn, form))

    return forward, reverse


primary_active, rev_primary_active = ENDINGS(PRIMARY_ACTIVE, PRIMARY_ACTIVE_ALPHA, PRIMARY_ACTIVE_EPSILON, PRIMARY_ACTIVE_OMICRON)
primary_middle, rev_primary_middle = ENDINGS(PRIMARY_MIDDLE, PRIMARY_MIDDLE_ALPHA, PRIMARY_MIDDLE_EPSILON, PRIMARY_MIDDLE_OMICRON)
secondary_active, rev_secondary_active = ENDINGS(SECONDARY_ACTIVE, SECONDARY_ACTIVE_ALPHA, SECONDARY_ACTIVE_EPSILON, SECONDARY_ACTIVE_OMICRON)
secondary_middle, rev_secondary_middle = ENDINGS(SECONDARY_MIDDLE, SECONDARY_MIDDLE_ALPHA, SECONDARY_MIDDLE_EPSILON, SECONDARY_MIDDLE_OMICRON)


def PART(stem_key):

    def forward(verb):
        stem = verb.lexeme[stem_key]
        if stem != "unknown":
            return stem
        else:
            return None

    def reverse(stem):
        return stem_key, stem

    return forward, reverse


present, rev_present = PART("P")
imperfect, rev_imperfect = PART("I")
future, rev_future = PART("F")
future_passive, rev_future_passive = PART("FP")


class Verb1:

    def __init__(self, lexeme):
        self.lexeme = lexeme

    def PAI(self): return primary_active(present(self))
    def PMI(self): return primary_middle(present(self))
    def IAI(self): return secondary_active(imperfect(self))
    def IMI(self): return secondary_middle(imperfect(self))
    def FAI(self): return primary_active(future(self))
    def FMI(self): return primary_middle(future(self))
    def FPI(self): return primary_middle(future_passive(self))

    def rev_PAI(self, form, pn): return rev_present(rev_primary_active(form, pn))
    def rev_PMI(self, form, pn): return rev_present(rev_primary_middle(form, pn))
    def rev_IAI(self, form, pn): return rev_imperfect(rev_secondary_active(form, pn))
    def rev_IMI(self, form, pn): return rev_imperfect(rev_secondary_middle(form, pn))
    def rev_FAI(self, form, pn): return rev_future(rev_primary_active(form, pn))
    def rev_FMI(self, form, pn): return rev_future(rev_primary_middle(form, pn))
    def rev_FPI(self, form, pn): return rev_future_passive(rev_primary_middle(form, pn))


def conditional_recessive(word):
    """
    only add recessive accent if there isn't already an accent
    """
    if has_accent(word):
        return remove_length(word)
    else:
        return remove_length(recessive(word))


def calculate_form(lexeme, parse):
    tvm, pn = parse.split(".")
    paradigm = getattr(lexeme, tvm)()
    if paradigm is None:
        return []
    else:
        result = paradigm[pn]

    if isinstance(result, list):
        result = [conditional_recessive(x) for x in result]
    else:
        result = conditional_recessive(result)
    return result


def calculate_part(lexeme, form, parse):
    tvm, pn = parse.split(".")
    stem_key, results = getattr(lexeme, "rev_" + tvm)(form, pn)
    return stem_key, [remove(result) for result in results]
