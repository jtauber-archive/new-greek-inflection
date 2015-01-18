#!/usr/bin/env python

from pysblgnt import morphgnt_rows


for book_num in range(1, 28):
    for row in morphgnt_rows(book_num):
        if row["ccat-pos"] == "V-":
            tvm = row["ccat-parse"][1:4]
            if tvm[:2] == "PP":
                tvm = "PM" + tvm[2]
            elif tvm[:2] == "IP":
                tvm = "IM" + tvm[2]
            elif tvm[:2] == "XP":
                tvm = "XM" + tvm[2]
            elif tvm[:2] == "YP":
                tvm = "YM" + tvm[2]
            if tvm[0] in ["X", "Y"] and tvm[2] not in ["P"]:
                if tvm[2] == "N":
                    print(row["lemma"], tvm, row["norm"])
                else:
                    pn = row["ccat-parse"][0] + row["ccat-parse"][5]
                    print(row["lemma"], tvm + "." + pn, row["norm"])
