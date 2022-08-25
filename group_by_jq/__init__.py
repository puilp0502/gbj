#!/usr/bin/env python3
# Author: Frank Yang <puilp0502@gmail.com>
# gbj.py: Group by newline-delimeted JSON data via jq expression
# Usage: gbj '.jq.expr.first' '.jq.expr.second'

from collections import defaultdict
import sys
import json

import jq
from tabulate import tabulate

def flatten_if_singular(output):
    if len(output) == 0:
        return ''
    elif len(output) == 1:
        return output[0]
    else:
        return output


def main():
    cols = sys.argv[1:]
    compiled_exprs = [jq.compile(expr) for expr in cols]
    aggs = defaultdict(lambda: 0)
    for raw_row in sys.stdin:
        if raw_row.strip() == "": continue
        key = tuple(str(flatten_if_singular(expr.input(text=raw_row).all())) for expr in compiled_exprs)
        aggs[key] += 1
    table = [[*key, value] for key, value in aggs.items()]
    print(tabulate(table, headers=cols + ["COUNT(*)"]))

if __name__ == "__main__":
    main()

