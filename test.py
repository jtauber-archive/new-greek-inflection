#!/usr/bin/env python3


from lexicon import LEXICON
from verbs import calculate_form, calculate_part


passed = 0
fails = []

# for test_name in ["test0.txt"]:
for test_name in ["test.txt", "test2.txt", "test3.txt", "test4.txt", "test5.txt", "test6.txt", "test7.txt", "test8.txt", "test9.txt", "test10.txt"]:
    with open("tests/{}".format(test_name)) as f:
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
