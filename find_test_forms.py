#!/usr/bin/env python

from pysblgnt import morphgnt_rows

# from utils import remove

for book_num in range(1, 28):
    for row in morphgnt_rows(book_num):
        if row["ccat-pos"] == "V-":
            tvm = row["ccat-parse"][1:4]
            if tvm[:2] == "PP":
                tvm = "PM" + tvm[2]
            elif tvm[:2] == "IP":
                tvm = "IM" + tvm[2]
            if tvm[0] in ["P", "I", "F"] and tvm[2] in ["D", "S", "O", "N"]:
                pn = row["ccat-parse"][0] + row["ccat-parse"][5]
                if tvm[2] == "N":
                    print(row["lemma"], tvm, row["norm"])
                else:
                    print(row["lemma"], tvm + "." + pn, row["norm"])
