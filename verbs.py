from accentuation import recessive
from endings import PRIMARY_ACTIVE, PRIMARY_MIDDLE, SECONDARY_ACTIVE, SECONDARY_MIDDLE
from endings import ACTIVE_SUBJUNCTIVE, MIDDLE_SUBJUNCTIVE
from endings import ACTIVE_OPTATIVE, MIDDLE_OPTATIVE
from endings import PRIMARY_ACTIVE_IMPERATIVE, PRIMARY_MIDDLE_IMPERATIVE
from endings import ACTIVE_INFINITIVE, MIDDLE_INFINITIVE
from utils import remove, has_accent, remove_length


def ENDINGS(paradigm):

    def forward(stems, pn=None):
        forms = []

        for stem in stems:
            if pn:
                pp = paradigm[pn]
            else:
                pp = paradigm
            for ending, stem_ending in pp:
                stem2, stem_ending = (stem[:-len(stem_ending)], remove(stem_ending)) if stem_ending else (stem, "")
                if stem.endswith(stem_ending):
                    forms.append(stem2 + ending)

        return forms

    def reverse(form, pn=None):
        stems = []

        if pn:
            if pn in paradigm:
                endings = paradigm[pn]
            else:
                endings = []
        else:
            endings = paradigm

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

active_subjunctive, rev_active_subjunctive = ENDINGS(ACTIVE_SUBJUNCTIVE)
middle_subjunctive, rev_middle_subjunctive = ENDINGS(MIDDLE_SUBJUNCTIVE)
active_optative, rev_active_optative = ENDINGS(ACTIVE_OPTATIVE)
middle_optative, rev_middle_optative = ENDINGS(MIDDLE_OPTATIVE)

primary_active_imperative, rev_primary_active_imperative = ENDINGS(PRIMARY_ACTIVE_IMPERATIVE)
primary_middle_imperative, rev_primary_middle_imperative = ENDINGS(PRIMARY_MIDDLE_IMPERATIVE)

active_infinitive, rev_active_infinitive = ENDINGS(ACTIVE_INFINITIVE)
middle_infinitive, rev_middle_infinitive = ENDINGS(MIDDLE_INFINITIVE)


def PART(stem_key):

    def forward(verb):
        stems = verb.lexeme.get(stem_key)
        if stems != "unknown" and stems is not None:
            return stems.split("/")
        else:
            return []

    def reverse(stem):
        return stem_key, stem

    return forward, reverse


present, rev_present = PART("P")
imperfect, rev_imperfect = PART("I")
future, rev_future = PART("F")
future_passive, rev_future_passive = PART("FP")
aorist, rev_aorist = PART("A")
aorist_passive, rev_aorist_passive = PART("AP")
aorist_infinitive, rev_aorist_infinitive = PART("AN")
aorist_passive_infinitive, rev_aorist_passive_infinitive = PART("APN")


class Verb:

    def __init__(self, lexeme):
        self.lexeme = lexeme

    def PAI(self, pn): return primary_active(present(self), pn)
    def PMI(self, pn): return primary_middle(present(self), pn)
    def IAI(self, pn): return secondary_active(imperfect(self), pn)
    def IMI(self, pn): return secondary_middle(imperfect(self), pn)
    def FAI(self, pn): return primary_active(future(self), pn)
    def FMI(self, pn): return primary_middle(future(self), pn)
    def FPI(self, pn): return primary_middle(future_passive(self), pn)

    def AAI(self, pn): return secondary_active(aorist(self), pn)
    def AMI(self, pn): return secondary_middle(aorist(self), pn)
    def API(self, pn): return secondary_active(aorist_passive(self), pn)

    def PAS(self, pn): return active_subjunctive(present(self), pn)
    def PMS(self, pn): return middle_subjunctive(present(self), pn)
    def PAO(self, pn): return active_optative(present(self), pn)
    def PMO(self, pn): return middle_optative(present(self), pn)
    def FAO(self, pn): return active_optative(future(self), pn)
    def FMO(self, pn): return middle_optative(future(self), pn)
    def FPO(self, pn): return middle_optative(future_passive(self), pn)

    def PAD(self, pn): return primary_active_imperative(present(self), pn)
    def PMD(self, pn): return primary_middle_imperative(present(self), pn)

    def PAN(self): return active_infinitive(present(self))
    def PMN(self): return middle_infinitive(present(self))
    def FAN(self): return active_infinitive(future(self))
    def FMN(self): return middle_infinitive(future(self))
    def FPN(self): return middle_infinitive(future_passive(self))
    def AAN(self): return active_infinitive(aorist_infinitive(self))
    def AMN(self): return middle_infinitive(aorist_infinitive(self))
    def APN(self): return active_infinitive(aorist_passive_infinitive(self))

    def rev_PAI(self, form, pn): return rev_present(rev_primary_active(form, pn))
    def rev_PMI(self, form, pn): return rev_present(rev_primary_middle(form, pn))
    def rev_IAI(self, form, pn): return rev_imperfect(rev_secondary_active(form, pn))
    def rev_IMI(self, form, pn): return rev_imperfect(rev_secondary_middle(form, pn))
    def rev_FAI(self, form, pn): return rev_future(rev_primary_active(form, pn))
    def rev_FMI(self, form, pn): return rev_future(rev_primary_middle(form, pn))
    def rev_FPI(self, form, pn): return rev_future_passive(rev_primary_middle(form, pn))

    def rev_AAI(self, form, pn): return rev_aorist(rev_secondary_active(form, pn))
    def rev_AMI(self, form, pn): return rev_aorist(rev_secondary_middle(form, pn))
    def rev_API(self, form, pn): return rev_aorist_passive(rev_secondary_active(form, pn))

    def rev_PAS(self, form, pn): return rev_present(rev_active_subjunctive(form, pn))
    def rev_PMS(self, form, pn): return rev_present(rev_middle_subjunctive(form, pn))
    def rev_PAO(self, form, pn): return rev_present(rev_active_optative(form, pn))
    def rev_PMO(self, form, pn): return rev_present(rev_middle_optative(form, pn))
    def rev_FAO(self, form, pn): return rev_future(rev_active_optative(form, pn))
    def rev_FMO(self, form, pn): return rev_future(rev_middle_optative(form, pn))
    def rev_FPO(self, form, pn): return rev_future_passive(rev_middle_optative(form, pn))

    def rev_PAD(self, form, pn): return rev_present(rev_primary_active_imperative(form, pn))
    def rev_PMD(self, form, pn): return rev_present(rev_primary_middle_imperative(form, pn))

    def rev_PAN(self, form): return rev_present(rev_active_infinitive(form))
    def rev_PMN(self, form): return rev_present(rev_middle_infinitive(form))
    def rev_FAN(self, form): return rev_future(rev_active_infinitive(form))
    def rev_FMN(self, form): return rev_future(rev_middle_infinitive(form))
    def rev_FPN(self, form): return rev_future_passive(rev_middle_infinitive(form))
    def rev_AAN(self, form): return rev_aorist_infinitive(rev_active_infinitive(form))
    def rev_AMN(self, form): return rev_aorist_infinitive(rev_middle_infinitive(form))
    def rev_APN(self, form): return rev_aorist_passive_infinitive(rev_active_infinitive(form))


def conditional_recessive(word):
    """
    only add recessive accent if there isn't already an accent
    """
    if has_accent(word):
        return remove_length(word)
    else:
        return remove_length(recessive(word))


def calculate_form(lexeme, parse):
    if parse[2] == "N":
        result = getattr(lexeme, parse)()
    else:
        tvm, pn = parse.split(".")
        result = getattr(lexeme, tvm)(pn)

    if isinstance(result, list):
        result = [conditional_recessive(x) for x in result]
    else:
        result = conditional_recessive(result)
    return result


def calculate_part(lexeme, form, parse):
    if parse[2] == "N":
        stem_key, results = getattr(lexeme, "rev_" + parse)(form)
    else:
        tvm, pn = parse.split(".")
        stem_key, results = getattr(lexeme, "rev_" + tvm)(form, pn)

    return stem_key, [remove(result) for result in results]
