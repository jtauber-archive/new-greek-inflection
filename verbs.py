import re

from accentuation import recessive, on_penult
from endings import PRIMARY_ACTIVE, PRIMARY_MIDDLE, SECONDARY_ACTIVE, SECONDARY_MIDDLE
from endings import ACTIVE_SUBJUNCTIVE, MIDDLE_SUBJUNCTIVE
from endings import PRIMARY_ACTIVE_OPTATIVE, PRIMARY_MIDDLE_OPTATIVE
from endings import SECONDARY_ACTIVE_OPTATIVE, SECONDARY_MIDDLE_OPTATIVE
from endings import PRIMARY_ACTIVE_IMPERATIVE, PRIMARY_MIDDLE_IMPERATIVE
from endings import SECONDARY_ACTIVE_IMPERATIVE, SECONDARY_MIDDLE_IMPERATIVE
from endings import ACTIVE_INFINITIVE, MIDDLE_INFINITIVE
from utils import remove, has_accent, remove_length, remove_smooth


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
        stems = set()

        if pn:
            if pn in paradigm:
                endings = paradigm[pn]
            else:
                endings = []
        else:
            endings = paradigm

        for ending, stem_ending in endings:
            if remove(form).endswith(remove(remove_length(ending))):
                stems.add(form[:-len(ending)] + (stem_ending if stem_ending else ""))

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
primary_active_optative, rev_primary_active_optative = ENDINGS(PRIMARY_ACTIVE_OPTATIVE)
primary_middle_optative, rev_primary_middle_optative = ENDINGS(PRIMARY_MIDDLE_OPTATIVE)
secondary_active_optative, rev_secondary_active_optative = ENDINGS(SECONDARY_ACTIVE_OPTATIVE)
secondary_middle_optative, rev_secondary_middle_optative = ENDINGS(SECONDARY_MIDDLE_OPTATIVE)

primary_active_imperative, rev_primary_active_imperative = ENDINGS(PRIMARY_ACTIVE_IMPERATIVE)
primary_middle_imperative, rev_primary_middle_imperative = ENDINGS(PRIMARY_MIDDLE_IMPERATIVE)
secondary_active_imperative, rev_secondary_active_imperative = ENDINGS(SECONDARY_ACTIVE_IMPERATIVE)
secondary_middle_imperative, rev_secondary_middle_imperative = ENDINGS(SECONDARY_MIDDLE_IMPERATIVE)

active_infinitive, rev_active_infinitive = ENDINGS(ACTIVE_INFINITIVE)
middle_infinitive, rev_middle_infinitive = ENDINGS(MIDDLE_INFINITIVE)


def PART(stem_key):

    def forward(verb):
        stems = verb.lexeme.get(stem_key)
        if stems != "unknown" and stems is not None:
            return stems.split("/")
        else:
            if verb.inherit is not None:
                if "prefix" in verb.lexeme:
                    return ["{}++{}".format(verb.lexeme["prefix"], s) for s in forward(verb.inherit)]
                else:
                    return forward(verb.inherit)
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
    def PAO(self, pn): return primary_active_optative(present(self), pn)
    def PMO(self, pn): return primary_middle_optative(present(self), pn)
    def FAO(self, pn): return primary_active_optative(future(self), pn)
    def FMO(self, pn): return primary_middle_optative(future(self), pn)
    def FPO(self, pn): return primary_middle_optative(future_passive(self), pn)

    def AAS(self, pn): return active_subjunctive(aorist_infinitive(self), pn)
    def AMS(self, pn): return middle_subjunctive(aorist_infinitive(self), pn)
    def APS(self, pn): return active_subjunctive(aorist_passive_infinitive(self), pn)
    def AAO(self, pn): return secondary_active_optative(aorist_infinitive(self), pn)
    def AMO(self, pn): return secondary_middle_optative(aorist_infinitive(self), pn)
    def APO(self, pn): return secondary_active_optative(aorist_passive_infinitive(self), pn)

    def PAD(self, pn): return primary_active_imperative(present(self), pn)
    def PMD(self, pn): return primary_middle_imperative(present(self), pn)

    def AAD(self, pn): return secondary_active_imperative(aorist_infinitive(self), pn)
    def AMD(self, pn): return secondary_middle_imperative(aorist_infinitive(self), pn)
    def APD(self, pn): return secondary_active_imperative(aorist_passive_infinitive(self), pn)

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
    def rev_PAO(self, form, pn): return rev_present(rev_primary_active_optative(form, pn))
    def rev_PMO(self, form, pn): return rev_present(rev_primary_middle_optative(form, pn))
    def rev_FAO(self, form, pn): return rev_future(rev_primary_active_optative(form, pn))
    def rev_FMO(self, form, pn): return rev_future(rev_primary_middle_optative(form, pn))
    def rev_FPO(self, form, pn): return rev_future_passive(rev_primary_middle_optative(form, pn))

    def rev_AAS(self, form, pn): return rev_aorist_infinitive(rev_active_subjunctive(form, pn))
    def rev_AMS(self, form, pn): return rev_aorist_infinitive(rev_middle_subjunctive(form, pn))
    def rev_APS(self, form, pn): return rev_aorist_passive_infinitive(rev_active_subjunctive(form, pn))
    def rev_AAO(self, form, pn): return rev_aorist_infinitive(rev_secondary_active_optative(form, pn))
    def rev_AMO(self, form, pn): return rev_aorist_infinitive(rev_secondary_middle_optative(form, pn))
    def rev_APO(self, form, pn): return rev_aorist_passive_infinitive(rev_secondary_active_optative(form, pn))

    def rev_PAD(self, form, pn): return rev_present(rev_primary_active_imperative(form, pn))
    def rev_PMD(self, form, pn): return rev_present(rev_primary_middle_imperative(form, pn))

    def rev_AAD(self, form, pn): return rev_aorist_infinitive(rev_secondary_active_imperative(form, pn))
    def rev_AMD(self, form, pn): return rev_aorist_infinitive(rev_secondary_middle_imperative(form, pn))
    def rev_APD(self, form, pn): return rev_aorist_passive_infinitive(rev_secondary_active_imperative(form, pn))

    def rev_PAN(self, form): return rev_present(rev_active_infinitive(form))
    def rev_PMN(self, form): return rev_present(rev_middle_infinitive(form))
    def rev_FAN(self, form): return rev_future(rev_active_infinitive(form))
    def rev_FMN(self, form): return rev_future(rev_middle_infinitive(form))
    def rev_FPN(self, form): return rev_future_passive(rev_middle_infinitive(form))
    def rev_AAN(self, form): return rev_aorist_infinitive(rev_active_infinitive(form))
    def rev_AMN(self, form): return rev_aorist_infinitive(rev_middle_infinitive(form))
    def rev_APN(self, form): return rev_aorist_passive_infinitive(rev_active_infinitive(form))


def conditional_recessive(word, parse):
    """
    only add recessive accent if there isn't already an accent and don't let
    accent cross $ boundary
    """

    if has_accent(word):
        return remove_length(word)
    else:
        if parse in ["AAN", "APN", "PAN"]:
            return remove_length(on_penult(word))
        if "$" in word:
            prefix, body = word.split("$")
            return prefix + "$" + remove_length(recessive(body))
        else:
            if parse[2] == "O":
                return remove_length(recessive(word, False))
            else:
                return remove_length(recessive(word))


def calculate_form(lexeme, parse):
    if parse[2] == "N":
        result = getattr(lexeme, parse)()
    else:
        tvm, pn = parse.split(".")
        result = getattr(lexeme, tvm)(pn)

    new_result = []
    for r in result:
        if "++" in r:
            prefix, body = r.split("++")

            prefix = re.sub(r"ἀντί\+ἀ", "ἀντα", prefix)
            prefix = re.sub(r"ἀπό\+ἐ", "ἀπε", prefix)
            prefix = re.sub(r"ἐκ\+ἀ", "ἐξα", prefix)
            prefix = re.sub(r"ἐν\+κ", "ἐγκ", prefix)
            prefix = re.sub(r"ἐν\+π", "ἐμπ", prefix)
            prefix = re.sub(r"ἐπί\+ἀ", "ἐπα", prefix)
            prefix = re.sub(r"ἐπί\+ἐ", "ἐπε", prefix)
            prefix = re.sub(r"ἐπί\+εἰ", "ἐπει", prefix)
            prefix = re.sub(r"κατά\+ἐ", "κατε", prefix)
            prefix = re.sub(r"παρά\+ἐ", "παρε", prefix)
            prefix = re.sub(r"παρά\+εἰ", "παρει", prefix)
            prefix = re.sub(r"πρό\+ἐ", "προε", prefix)
            prefix = re.sub(r"πρό\+ὑ", "προϋ", prefix)
            prefix = re.sub(r"πρός\+ἀ", "προσα", prefix)
            prefix = re.sub(r"σύν\+ἀ", "συνα", prefix)
            prefix = re.sub(r"σύν\+ἐ", "συνε", prefix)
            prefix = re.sub(r"σύν\+εἰ", "συνει", prefix)
            prefix = re.sub(r"σύν\+ὑ", "συνυ", prefix)
            prefix = re.sub(r"σύν\+κ", "συγκ", prefix)
            prefix = re.sub(r"σύν\+π", "συμπ", prefix)
            prefix = re.sub(r"ὑπέρ\+ἐ", "ὑπερε", prefix)
            prefix = re.sub(r"\+", "", prefix)

            prefix = remove(prefix)
            body = remove_smooth(body)
            new_r = prefix + "++" + body

            new_r = re.sub(r"ἀντι\+\+ἑ", "ἀνθε", new_r)
            new_r = re.sub(r"ἀντι\+\+ἱ", "ἀνθι", new_r)
            new_r = re.sub(r"ἀντι\+\+ὁ", "ἀνθο", new_r)
            new_r = re.sub(r"ἀντι\+\+ὡ", "ἀνθω", new_r)
            new_r = re.sub(r"ἀπο\+\+ἑ", "ἀφε", new_r)
            new_r = re.sub(r"ἀπο\+\+ἡ", "ἀφη", new_r)
            new_r = re.sub(r"ἀπο\+\+ἱ", "ἀφι", new_r)
            new_r = re.sub(r"ἀπο\+\+ὁ", "ἀφο", new_r)
            new_r = re.sub(r"ἀπο\+\+ὡ", "ἀφω", new_r)
            new_r = re.sub(r"ἀπο\+\+αἱ", "ἀφαι", new_r)
            new_r = re.sub(r"ἀπο\+\+\$εἱ", "ἀφ$ει", new_r)
            new_r = re.sub(r"ἐπι\+\+ἱ", "ἐφι", new_r)
            new_r = re.sub(r"κατα\+\+ἑ", "καθε", new_r)
            new_r = re.sub(r"κατα\+\+αἱ", "καθαι", new_r)
            new_r = re.sub(r"κατα\+\+\$εἱ", "καθ$ει", new_r)
            new_r = re.sub(r"κατα\+\+\$ἡ", "καθ$η", new_r)
            new_r = re.sub(r"κατα\+\+ἱ", "καθι", new_r)
            new_r = re.sub(r"κατα\+\+ὁ", "καθο", new_r)
            new_r = re.sub(r"μετα\+\+ἑ", "μεθε", new_r)
            new_r = re.sub(r"μετα\+\+ἱ", "μεθι", new_r)

            new_r = re.sub(r"\+\+ἁ", "++α", new_r)
            new_r = re.sub(r"\+\+ἑ", "++ε", new_r)
            new_r = re.sub(r"\+\+ἡ", "++η", new_r)
            new_r = re.sub(r"\+\+ἱ", "++ι", new_r)
            new_r = re.sub(r"\+\+ὁ", "++ο", new_r)
            new_r = re.sub(r"\+\+ὑ", "++υ", new_r)
            new_r = re.sub(r"\+\+ὡ", "++ω", new_r)
            new_r = re.sub(r"\+\+\$ἡ", "++$η", new_r)
            new_r = re.sub(r"\+\+αἱ", "++αι", new_r)
            new_r = re.sub(r"\+\+\$εἱ", "++$ει", new_r)
            new_r = re.sub(r"\+\+\$εὑ", "++$ευ", new_r)

            new_r = re.sub(r"προ\+\+(\$?[αεηῃοω])", r"προ\1", new_r)
            new_r = re.sub(r"προ\+\+ι", r"προϊ", new_r)
            new_r = re.sub(r"περι\+\+(\$?[αεηῃ])", r"περι\1", new_r)
            new_r = re.sub(r"περι\+\+ι", r"περιϊ", new_r)
            new_r = re.sub(r"[αιο]\+\+(\$?[αεηῃιοωῳ]|οι)", r"\1", new_r)
            new_r = re.sub(r"κ\+\+(\$?[αεηῃιοω])", r"ξ\1", new_r)
            new_r = re.sub(r"ς\+\+", "σ", new_r)
            new_r = re.sub(r"α\+\+β", "αβ", new_r)
            new_r = re.sub(r"ν\+\+([βπφμ])", r"μ\1", new_r)
            new_r = re.sub(r"ν\+\+([κχ])", r"γ\1", new_r)
            new_r = re.sub(r"ν\+\+λ", "λλ", new_r)
            new_r = re.sub(r"συν\+\+σ", "συσ", new_r)
            new_r = re.sub(r"ν\+\+ζ", "ζ", new_r)

            new_result.append(new_r)
        else:
            new_result.append(r)
    result = new_result

    result = [r.replace("++", "") for r in result]

    if isinstance(result, list):
        result = [conditional_recessive(x, parse) for x in result]
    else:
        result = conditional_recessive(result, parse)

    result = [r.replace("$", "") for r in result]

    result = [re.sub(r"~ή", "ή", r) for r in result]
    result = [re.sub(r"~́η", "ῆ", r) for r in result]
    result = [re.sub(r"~ώ", "ώ", r) for r in result]
    result = [re.sub(r"~́ω", "ῶ", r) for r in result]
    result = [re.sub(r"~́ει", "εῖ", r) for r in result]

    return result


def calculate_part(lexeme, form, parse):
    if parse[2] == "N":
        stem_key, results = getattr(lexeme, "rev_" + parse)(form)
    else:
        tvm, pn = parse.split(".")
        stem_key, results = getattr(lexeme, "rev_" + tvm)(form, pn)

    return stem_key, set(remove(result) for result in results)
