import re


### CODE


def f(x):
    if x == "":
        return "", ""
    m = re.search(r"\|([^>]+)>", x)
    if m:
        stem_ending = m.group(1)
    else:
        stem_ending = None
    x = re.sub(r"\|[^>]+>", "", x)
    x = re.sub(r"<[^|]+\|", "", x)
    x = re.sub(r"\+", "", x)
    return x, stem_ending


def g(x, y):
    return [
        f(z.format(*x))
        for z in y
    ]


### CONNECTING VOWELS


C0 = [
    "|!>+{0}", "|α!>η+{0}", "|ᾰ!>η+{0}", "|ε!>η+{0}", "|ο!>ω+{0}",
]

C1e = [
    "ε+{0}",
    "|α>ᾱ<ε|+{0}", "|ε>ει<ε|+{0}", "|ο>ου<ε|+{0}",  # @@@
    "|α>ά<έ|+{0}", "|ε>εί<έ|+{0}", "|ο>ού<έ|+{0}",  # @@@
    "|ά>ᾶ<ε|+{0}", "|έ>εῖ<ε|+{0}", "|ό>οῦ<ε|+{0}",  # @@@
    "|ή>ῆ<ε|+{0}",
    "|#>εῖ<ε|+{0}",
]

C1o = [
    "ο+{0}",
    "ό+{0}",
    "|α>ω<ο|+{0}", "|ε>ου<ο|+{0}", "|ο>ου<ο|+{0}",  # @@@
    "|α>ώ<ό|+{0}", "|ε>ού<ό|+{0}", "|ο>ού<ό|+{0}",  # @@@
    "|ά>ῶ<ο|+{0}", "|έ>οῦ<ο|+{0}", "|ό>οῦ<ο|+{0}",  # @@@
    "|η>ω<ο|+{0}",
    "|#>οῦ<ο|+{0}",
]

C2 = [
    "|!>+{0}",
    "|σ>σα+{0}", "|ξ>ξα+{0}", "|ψ>ψα+{0}",
    "|θ>θα+{0}",  # @@@
    "|κ>κα+{0}",
    "|λ>λα+{0}", "|ρ>ρα+{0}",
    "|μ>μα+{0}", "|ν>να+{0}",
    "|π>πα+{0}",  # @@@
]

mosubj = [
    "ω+{0}",
    "|ά>ῶ+{0}", "|έ>ῶ+{0}", "|ό>ῶ+{0}",
    "|ά!>ῶ+{0}", "|έ!>ῶ+{0}", "|ό!>ῶ+{0}",
    "|ᾰ!>ῶ+{0}",
    "|α>ω+{0}", "|ε>ω+{0}", "|ο>ω+{0}",  # because of ώμεθα
    "|α!>ω+{0}", "|ε!>ω+{0}", "|ο!>ω+{0}",  # because of ώμεθα
]

mesubj = [
    "η+{0}",
    "|ά>ᾶ+{0}", "|έ>ῆ+{0}", "|ό>ῶ+{0}",
    "|ό!>ῶ+{0}", "|έ!>ῆ+{0}", "|ά!>ῆ+{0}",
    "|ᾰ!>ῆ+{0}",
]

Cpao1 = [
    "οι+{0}",
    "|ά>ῷ+{0}", "|έ>οῖ+{0}", "|ό>οῖ+{0}",
    "|!>ῖ+{0}",
]


Cpao2 = [
    "|ά>ῴη+{0}", "|έ>οιη+{0}", "|ο>οιη+{0}",
    "|!>ιη+{0}",
]


Cpopt = [
    "οι+{0}",
    "|α>~ῳ+{0}", "|ε>~οι+{0}", "|ο>~οι+{0}",
    "|α!>~αι+{0}", "|ε!>~ει+{0}", "|ο!>~οι+{0}",
    "|α!>αι+{0}",  # @@@
]


Copt = [
    "αι+{0}",
    "οι+{0}",
    "|α!>αι+{0}",
    "|η!>~ει+{0}",
    "|ε!>ει+{0}",
    "|ο!>οι+{0}",
    "|ο!>ῳ+{0}",
    "|ω!>οι+{0}",
]

Cpai = [
    "ε+{0}",
    "|α>~α+{0}", "|ε>~ει+{0}", "|ο>~ου+{0}",
    "|!>+{0}", "|οἰ!>οἰ+ε+{0}",
]

Cp3P = [
    "ου+{0}", "|ά>ῶ<ου|+{0}", "|έ>οῦ<ου|+{0}", "|ό>οῦ<ου|+{0}", "|#>οῦ<ου|+{0}",
    "|!>α+{0}", "|α!>ᾶ<α|+{0}", "|ᾰ!>ᾶ<α|+{0}", "|ε!>ᾶ<α|+{0}", "|ε!>ου+{0}",
    "+{0}",  # @@@
]

Casubjo = [
    "ω+{0}",
    "|ά>ῶ+{0}", "|έ>ῶ+{0}", "|ό>ῶ+{0}",
    "|ό!>ῶ+{0}", "|έ!>ῶ+{0}", "|ά!>ῶ+{0}",
    "|ᾰ!>ῶ+{0}",
    "|η!>ῶ+{0}", "|ω!>ῶ+{0}",
]

Casubje = [
    "η+{0}",
    "|ά>ᾶ+{0}", "|έ>ῆ+{0}", "|ό>οῦ+{0}", "|ό>ῶ+{0}",
    "|ό!>ῶ+{0}", "|έ!>ῆ+{0}", "|ά!>ῆ+{0}",
    "|ω!>ῶ+{0}",
    "|ᾰ!>ῆ+{0}",
    "|η!>ῆ+{0}", "|η!>η+{0}",  # @@@
]

Casubjei = [
    "ῃ+{0}",
    "|ά>ᾷ+{0}", "|έ>ῇ+{0}", "|ό>οῖ+{0}",
    "|ό!>ῷ+{0}", "|έ!>ῇ+{0}", "|ά!>ῇ+{0}",
    "|ᾰ!>ῇ+{0}",
    "|η!>ῇ+{0}", "|ω!>ῷ+{0}",
]

Cpmo = [
    "ο+{0}",
    "|ά>ῶ<ο|+{0}", "|έ>οῦ<ο|+{0}", "|έ>έο<ο|+{0}", "|ό>οῦ<ο|+{0}",
    "|!>{0}",
]

Cpme = [
    "ε+{0}",
    "|ά>ᾶ<ε|+{0}",
    "|!>{0}",
]


### ENDINGS


## PRIMARY ACTIVES


PRIMARY_ACTIVE = {
    "1S": g(["μι"], C0) + [
        f("ω"), f("|ά>ῶ<ω|"), f("|έ>ῶ<ω|"), f("|ό>ῶ<ω|"), f("|#>ῶ<ω|"),
    ],
    "2S": g(["ς"], C0 + [
        "ει+{0}", "|ά>ᾷ<ει|+{0}", "|έ>εῖ<ει|+{0}", "|ό>οῖ<ει|+{0}", "|#>εῖ<ει|+{0}",
        "|η>ῃ<ι|+{0}",
    ]) + [
        f("εἶ"),  # @@@
    ],
    "3S": g(["σι(ν)"], C0) + [
        f("ει"), f("|ά>ᾷ<ει|"), f("|έ>εῖ<ει|"), f("|ό>οῖ<ει|"), f("|#>εῖ<ει|"), f("|η>ῃ<ι|"),
        f("|!>τι(ν)"),
    ],
    "1P": g(["μεν"], C1o + ["|!>{0}"]),
    "2P": g(["τε"], C1e + ["|!>{0}"]),
    "3P": g(["σι(ν)"], Cp3P),
}


PERFECT_ACTIVE = {
    "1S": g([""], ["α+{0}"]),
    "2S": g(["ς"], [
        "α+{0}",
        "ε+{0}",  # @@@
    ]),
    "3S": [f("ε(ν)")],
    "1P": g(["μεν"], ["α+{0}"]),
    "2P": g(["τε"], ["α+{0}"]),
    "3P": g(["σι(ν)"], ["α+{0}"]) +
          g(["ν"], ["α+{0}"]),  # @@@
}

ACTIVE_SUBJUNCTIVE = {
    "1S": g([""], Casubjo),
    "2S": g(["ς"], Casubjei),
    "3S": g([""], Casubjei) + [
        f("|ε>εσῃ"),
        f("|ο!>οῖ"), f("|ω!>οῖ"), f("|ο!>ωῃ"), f("|ο!>ωσῃ")  # @@@
    ],
    "1P": g(["μεν"], Casubjo),
    "2P": g(["τε"], Casubje),
    "3P": g(["σι(ν)"], Casubjo),
}


## PRIMARY MIDDLES


PRIMARY_MIDDLE = {
    "1S": g(["μαι"], Cpmo),
    "2S": g(["σαι"], Cpme) + [
        f("ει"), f("|ά>ᾷ<ει|"), f("|έ>εῖ<ει|"), f("|ό>οῖ<ει|"),
        f("ῃ"), f("|α!>ῃ<ῃ|"), f("|έ>ῇ<ῃ|"), f("|η!>ῃ<ῃ|"),
    ],
    "3S": g(["ται"], C1e + ["|!>{0}"]),
    "1P": g(["μεθα"], C1o + ["|!>{0}"]),
    "2P": g(["σθε"], C1e + ["|!>{0}"]),
    "3P": g(["νται"], C1o + ["|!>{0}"]),
}

Cperfmid = [
    "+{0}",
    "+ω+{0}",  # for ἵημι
]

PERFECT_MIDDLE = {
    "1S": g(["μαι"], Cperfmid),
    "2S": g(["σαι"], Cperfmid),
    "3S": g(["ται"], Cperfmid),
    "1P": g(["μεθα"], Cperfmid),
    "2P": g(["σθε"], Cperfmid),
    "3P": g(["νται"], Cperfmid),
}


MIDDLE_SUBJUNCTIVE = {
    "1S": g(["μαι"], mosubj),
    "2S": [
        f("ῃ"),
        f("|ά>ᾷ"), f("|έ>ῇ"), f("|ό>οῖ"),
        f("|ό!>ῷ"), f("|έ!>ῇ"), f("|ά!>ῇ"),
        f("|ᾰ!>ῇ"),
    ],
    "3S": g(["ται"], mesubj),
    "1P": g(["μεθα"], mosubj),
    "2P": g(["σθε"], mesubj),
    "3P": g(["νται"], mosubj),
}


## SECONDARY ACTIVES


SECONDARY_ACTIVE = {
    "1S": g(["ν"], C1o + ["|!>+{0}", "|α!>η+{0}", "|ε!>ει+{0}", "|ε!>η+{0}", "|ο!>ου+{0}"]) + g([""], C2),
    "2S": g(["ς"], C1e + C2) + [
        f("|α!>η+ς"), f("|ε!>ει+ς"), f("|ο!>ου+ς"),
        f("|ειλ>εῖλες"),  # @@@
    ],
    "3S": g([""], C1e) + [
        f("ε(ν)"),
        f("|!>"), f("|η!>η"), f("|α!>η"), f("|ε!>ει"), f("|ο!>ου"), f("|!>ν"),
        f("|σ>σε(ν)"), f("|ψ>ψε(ν)"), f("|ξ>ξε(ν)"),
        f("|ειλ>εῖλε(ν)"),  # @@@
    ],
    "1P": g(["μεν"], C1o + C2),
    "2P": g(["τε"], C1e + C2),
    "3P": g(["ν"], C1o + C2) + [
        f("ο+σαν"), f("|ό>οῦ<ε|+σαν"),
        f("|!>σαν"),
        f("|ειλ>εῖλαν"),  # @@@
    ],
}


PRIMARY_ACTIVE_OPTATIVE = {
    "1S": g(["μι"], Cpao1) + g(["ν"], Cpao2),
    "2S": g(["ς"], Cpao1 + Cpao2),
    "3S": g([""], Cpao1 + Cpao2),
    "1P": g(["μεν"], Cpao1 + Cpao2),
    "2P": g(["τε"], Cpao1 + Cpao2),
    "3P": g(["εν"], Cpao1) + g(["σαν"], Cpao2) +
          g(["ε(ν)"], Cpao1),  # @@@
}


SECONDARY_ACTIVE_OPTATIVE = {
    "1S": [
        f("αι+μι"),
    ] + g(["η+ν"], Copt),
    "2S": [
        f("αι+ς"),
        f("εια+ς"),
    ] + g(["η+ς"], Copt),
    "3S": [
        f("αι"),
        f("οι"),
        f("ειε"),
    ] + g(["η"], Copt),
    "1P": g(["μεν"], Copt) + g(["η+μεν"], Copt),
    "2P": g(["τε"], Copt) + g(["η+τε"], Copt),
    "3P": [
        f("αι+ε(ν)"),  # @@@
        f("οι+ε(ν)"),
        f("εια+ν"),
    ] + g(["εν"], Copt) + g(["η+σαν"], Copt),
}


PLUPERFECT_ACTIVE = {
    "1S": [
        f("η"),
    ],
    "2S": [
        f("ης"),
    ],
    "3S": [
        f("ει"),
    ],
    "1P": g(["μεν"], ["ε+{0}"]),
    "2P": g(["τε"], [
        "ε+{0}",
        "ει+{0}",  # @@@
    ]),
    "3P": g(["σαν"], [
        "ε+{0}",
        "ει+{0}",  # @@@
    ]),
}


## SECONDARY MIDDLES


SECONDARY_MIDDLE = {
    "1S": g(["μην"], C1o + C2),
    "2S": [
        f("ου"), f("|ά>ῶ<ου|"), f("|έ>οῦ<ου|"), f("|ό>οῦ<ου|"),
        f("|ε!>ου<+σο|"), f("|ο!>ου<+σο|"),
        f("|!>σο"),
        f("|σ>σω"), f("|ξ>ξω"), f("|ψ>ψω"),
        f("|λ>λω"), f("|ρ>ρω"),
        f("|!>σθα"),  # @@@
    ],
    "3S": g(["το"], C1e + C2),
    "1P": g(["μεθα"], C1o + C2),
    "2P": g(["σθε"], C1e + C2),
    "3P": g(["ντο"], C1o + C2),
}


PRIMARY_MIDDLE_OPTATIVE = {
    "1S": g(["μην"], Cpopt),
    "2S": g(["ο"], Cpopt),
    "3S": g(["το"], Cpopt),
    "1P": g(["μεθα"], Cpopt),
    "2P": g(["σθε"], Cpopt),
    "3P": g(["ντο"], Cpopt),
}


SECONDARY_MIDDLE_OPTATIVE = {
    "1S": g(["μην"], Copt),
    "2S": g(["ο"], Copt),
    "3S": g(["το"], Copt),
    "1P": g(["μεθα"], Copt),
    "2P": g(["σθε"], Copt),
    "3P": g(["ντο"], Copt),
}


PLUPERFECT_MIDDLE = {
    "1S": g(["μην"], ["+{0}"]),
    "2S": g(["σο"], ["+{0}"]),
    "3S": g(["το"], ["+{0}"]),
    "1P": g(["μεθα"], ["+{0}"]),
    "2P": g(["σθε"], ["+{0}"]),
    "3P": g(["ντο"], ["+{0}"]),
}


## IMPERATIVES


PRIMARY_ACTIVE_IMPERATIVE = {
    "2S": [
        f("ε"),
        f("|α>ᾱ"), f("|ε>ει"), f("|ο>ου"),
        f("|ο!>ου"), f("|ε!>ει"), f("|α!>η"), f("|ῡ!>ῡ"),
        f("|ᾰ!>η"),
    ],
    "3S": g(["τω"], [
        "ε+{0}",
        "|α>~α+{0}", "|ε>~ει+{0}", "|ο>~ου+{0}",
        "|!>+{0}",
    ]),
    "2P": g(["τε"], [
        "ε+{0}",
        "|α>~α+{0}", "|ε>~ει+{0}", "|ο>~ου+{0}",
        "|!>+{0}",
    ]),
    "3P": g(["ντων"], [
        "ο+{0}",
        "|α>ω+{0}", "|ε>ου+{0}", "|ο>ου+{0}",
        "|!>+{0}",
    ]) + g(["τωσαν"], [
        "ε+{0}",
        "|α>α+{0}", "|ε>ει+{0}",
        "|!>+{0}",
    ]),
}


PRIMARY_MIDDLE_IMPERATIVE = {
    "2S": [
        f("ου"),
        f("|α>ῶ"), f("|ε>οῦ"), f("|ο>οῦ"),
        f("|!>+σο"), f("|η!>+ου"),
    ],
    "3S": g(["σθω"], Cpai),
    "2P": g(["σθε"], Cpai),
    "3P": g(["σθων"], Cpai) + g(["σθωσαν"], Cpai),
}


PERFECT_MIDDLE_IMPERATIVE = {
    "2S": g(["σο"], ["+{0}"]),
    "3S": g(["σθω"], ["+{0}"]),
    "2P": g(["σθε"], ["+{0}"]),
    "3P": g(["σθων"], ["+{0}"]),
}


SECONDARY_ACTIVE_IMPERATIVE = {
    "2S": g(["ς"], ["|σ>σα+{0}", "|!>+{0}"]) + [
        f("ον"),
        f("|!>+τι"),
        f("|!>+θι"),
        f("ε"),
        f("|α>ᾱ<ε|"),  # @@@
    ],
    "3S": g(["τω"], C1e + C2),
    "2P": g(["τε"], C1e + C2),
    "3P": g(["τωσαν"], C1e + C2) + g(["ντων"], [
        "α+{0}",
        "|α!>α+{0}",
        "|η!>ε+{0}",
        "|ε!>ε+{0}",
        "|ο!>ο+{0}",
        "|ω!>ο+{0}",
    ]),
}


SECONDARY_MIDDLE_IMPERATIVE = {
    "2S": [
        f("|ε!>ου"),
        f("|ο!>ου"),
        f("οῦ"),  # @@@
        f("|σ>σαι"),
        f("|ξ>ξαι"),
        f("|ψ>ψαι"),
    ],
    "3S": g(["σθω"], C1e + C2),
    "2P": g(["σθε"], C1e + C2),
    "3P": g(["σθωσαν"], C2) + g(["σθων"], [
        "α+{0}",
        "|ε!>ε+{0}",
        "|ο!>ο+{0}",
    ]),
}


## INFINITIVES


ACTIVE_INFINITIVE = [
    f("ειν"),
    f("~ειν"),
    f("|ε>~ειν"),

    f("|α>ᾶν"),  # @@@
    f("|ο>οῦν"),  # @@@
    f("|η>ῆν"),  # @@@
    f("|!>ναι"),
    f("|α!>άναι"),  # @@@
    f("|ῡ!>ύναι"),  # @@@
    f("|ο!>οῦναι"),  # @@@
    f("|ε!>εῖναι"),  # @@@
    f("|σ>σαι"),
    f("|ξ>ξαι"),
    f("|ψ>ψαι"),
    f("|κ>και"),
    f("|ρ>ραι"), f("|λ>λαι"),
    f("|ειν>εῖναι"),

    f("ε+ναι"),  # @@@ perfect
]


MIDDLE_INFINITIVE = g(
    ["σθαι"], [
        "ε+{0}",
        "έ+{0}",  # @@@
        "|ά>ᾶ+{0}", "|έ>εῖ+{0}", "|ό>οῦ+{0}",
        "|!>{0}", "|ει!>εῖ+{0}", "|η!>ῆ+{0}", "|ε!>έ+{0}",  # @@@
        "|σ>σα+{0}",
        "|ξ>ξα+{0}", "|ψ>ψα+{0}",
        "|ρ>ρα+{0}", "|λ>λα+{0}",

        "+{0}",  # perfect
        "η+{0}",  # perfect
    ]
) + [
    f("χ+θαι"),  # @@@
]
