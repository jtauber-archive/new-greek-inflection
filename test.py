#!/usr/bin/env python3

import os.path

from lexicon import LEXICON
from verbs import calculate_form, calculate_part


TEST_DIR = "tests"

TEST_FILES = [
    "test01.txt",
    "test02.txt",
    "test03.txt",
    "test04.txt",
    "test05.txt",
    "test06.txt",
    "test07.txt",
    "test08.txt",
    "test09.txt",
    "test10.txt",
]


passed = 0
fails = []


for test_name in TEST_FILES:
    with open(os.path.join(TEST_DIR, test_name)) as f:
        for line in f:
            record = line.strip().split("#")[0]
            if not record:
                continue
            lemma, parse, form = record.split()

            try:
                lexeme = LEXICON[lemma]
            except KeyError:
                print("{}:\n    P: unknown".format(lemma))

            prediction = calculate_form(lexeme, parse)

            predictions = []

            if isinstance(prediction, list):
                prediction_list = prediction
            else:
                prediction_list = [prediction]
            for prediction in prediction_list:
                if prediction.endswith("(ν)"):
                    predictions.append(prediction[:-3])
                    predictions.append(prediction[:-3] + "ν")
                predictions.append(prediction)

            if form in predictions:
                passed += 1
            else:
                suggested_num, suggested_part = calculate_part(lexeme, form, parse)
                fails.append("{} != {} (try {} for part {})".format(record, "/".join(predictions), "/".join(suggested_part), suggested_num))
                if len(fails) == 1:
                    print(fails[0])


print("{} passed".format(passed))
if fails:
    print("{} failed".format(len(fails)))
    print(fails[0])
