import unicodedata


def remove_diacritic(*diacritics):
    """
    Given a collection of Unicode diacritics, return a function that takes a
    string and returns the string without those diacritics.
    """
    def _(text):
        return unicodedata.normalize("NFC", "".join(
            ch
            for ch in unicodedata.normalize("NFD", text)
            if ch not in diacritics)
        )
    return _


def has_diacritic(*diacritics):
    """
    Given a collection of Unicode diacritics, return a function that takes a
    string and returns a boolean indicating if any of those diacritics exist
    in the string.
    """
    def _(text):
        for ch in unicodedata.normalize("NFD", text):
            if ch in diacritics:
                return True
        return False
    return _


OXIA = ACUTE = "\u0301"
VARIA = GRAVE = "\u0300"
PERISPOMENI = CIRCUMFLEX = "\u0342"

remove = remove_diacritic(ACUTE, GRAVE, CIRCUMFLEX)
has_accent = has_diacritic(ACUTE, GRAVE, CIRCUMFLEX)

SHORT = "\u0306"
LONG = "\u0304"

remove_length = remove_diacritic(SHORT, LONG)
