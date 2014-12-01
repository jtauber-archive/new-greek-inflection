from accentuation import recessive
from endings import PRIMARY_ACTIVE, PRIMARY_MIDDLE, SECONDARY_ACTIVE, SECONDARY_MIDDLE
from endings import PRIMARY_ACTIVE_MI, PRIMARY_MIDDLE_MI, SECONDARY_ACTIVE_MI, SECONDARY_MIDDLE_MI
from utils import remove, has_accent, remove_length


def ENDINGS(paradigm):

    def forward(stem, pn):
        if stem is None:
            return []

        forms = []
        for ending, stem_ending in paradigm[pn]:
            stem2, stem_ending = (stem[:-len(stem_ending)], remove(stem_ending)) if stem_ending else (stem, "")
            if stem.endswith(stem_ending):
                forms.append(stem2 + ending)
        return forms

    def reverse(form, pn):
        stems = []
        if pn in paradigm:
            endings = paradigm[pn]
            for ending, stem_ending in endings:
                if form.endswith(remove_length(ending)):
                    stems.append(form[:-len(ending)] + (stem_ending if stem_ending else ""))

        if stems:
            return stems
        else:
            raise Exception("got a {} of form {}".format(pn, form))

    return forward, reverse


primary_active, rev_primary_active = ENDINGS(PRIMARY_ACTIVE)
primary_middle, rev_primary_middle = ENDINGS(PRIMARY_MIDDLE)
secondary_active, rev_secondary_active = ENDINGS(SECONDARY_ACTIVE)
secondary_middle, rev_secondary_middle = ENDINGS(SECONDARY_MIDDLE)

primary_active_mi, rev_primary_active_mi = ENDINGS(PRIMARY_ACTIVE_MI)
primary_middle_mi, rev_primary_middle_mi = ENDINGS(PRIMARY_MIDDLE_MI)
secondary_active_mi, rev_secondary_active_mi = ENDINGS(SECONDARY_ACTIVE_MI)
secondary_middle_mi, rev_secondary_middle_mi = ENDINGS(SECONDARY_MIDDLE_MI)


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

    def PAI(self, pn): return primary_active(present(self), pn)
    def PMI(self, pn): return primary_middle(present(self), pn)
    def IAI(self, pn): return secondary_active(imperfect(self), pn)
    def IMI(self, pn): return secondary_middle(imperfect(self), pn)
    def FAI(self, pn): return primary_active(future(self), pn)
    def FMI(self, pn): return primary_middle(future(self), pn)
    def FPI(self, pn): return primary_middle(future_passive(self), pn)

    def rev_PAI(self, form, pn): return rev_present(rev_primary_active(form, pn))
    def rev_PMI(self, form, pn): return rev_present(rev_primary_middle(form, pn))
    def rev_IAI(self, form, pn): return rev_imperfect(rev_secondary_active(form, pn))
    def rev_IMI(self, form, pn): return rev_imperfect(rev_secondary_middle(form, pn))
    def rev_FAI(self, form, pn): return rev_future(rev_primary_active(form, pn))
    def rev_FMI(self, form, pn): return rev_future(rev_primary_middle(form, pn))
    def rev_FPI(self, form, pn): return rev_future_passive(rev_primary_middle(form, pn))


class Verb2(Verb1):

    def PAI(self, pn): return primary_active_mi(present(self), pn)
    def PMI(self, pn): return primary_middle_mi(present(self), pn)
    def IAI(self, pn): return secondary_active_mi(imperfect(self), pn)
    def IMI(self, pn): return secondary_middle_mi(imperfect(self), pn)

    def rev_PAI(self, form, pn): return rev_present(rev_primary_active_mi(form, pn))
    def rev_PMI(self, form, pn): return rev_present(rev_primary_middle_mi(form, pn))
    def rev_IAI(self, form, pn): return rev_imperfect(rev_secondary_active_mi(form, pn))
    def rev_IMI(self, form, pn): return rev_imperfect(rev_secondary_middle_mi(form, pn))


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
    result = getattr(lexeme, tvm)(pn)

    if isinstance(result, list):
        result = [conditional_recessive(x) for x in result]
    else:
        result = conditional_recessive(result)
    return result


def calculate_part(lexeme, form, parse):
    tvm, pn = parse.split(".")
    stem_key, results = getattr(lexeme, "rev_" + tvm)(form, pn)
    return stem_key, [remove(result) for result in results]
