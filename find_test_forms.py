#!/usr/bin/env python

from pysblgnt import morphgnt_rows

from utils import remove

for book_num in range(1, 28):
    for row in morphgnt_rows(book_num):
        if row["ccat-pos"] == "V-":
            tvm = row["ccat-parse"][1:4]
            if tvm == "PPI":
                tvm = "PMI"
            elif tvm == "IPI":
                tvm = "IMI"
            if tvm in ["PAI", "PMI", "IAI", "IMI", "FAI", "FMI", "FPI"]:
                pn = row["ccat-parse"][0] + row["ccat-parse"][5]
                if remove(row["lemma"]).endswith("μαι") and not remove(row["lemma"]).endswith("ομαι"):
                    print(row["lemma"], tvm + "." + pn, row["norm"])
