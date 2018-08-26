import glob
import os
import re
import pandas as pd
import unicodedata
from collections import OrderedDict

REG = re.compile(r"^(?P<root>[A-Z_]*\$?[A-Z_]+): *(?P<opt>[A-Z0-9_\/]+)? +"
                 r"(?P<value>[A-Za-z\[\]+()\-0-9 \/.′;&,:~<%>'?^\$_{}=#]+)+\s*$")

def prog3(folder_path):
    dfs = []

    for filename in glob.glob(os.path.join(folder_path, '*.txt')):

        nest = False
        records =OrderedDict()

        with open(filename, 'r', encoding="utf8") as opened_txt:
            for line in opened_txt:
                line = unicodedata.normalize('NFD', line).encode(
                    'ascii', 'ignore').decode('utf-8')
                match = REG.match(line).groupdict() if REG.match(line) else \
                    False
                if match:
                    nest = False
                    column = "_".join(
                        filter(None, (match.get("root"), match.get("opt"))))
                    records[column] = match.get("value") \
                        if column not in records else ",".join(
                        filter(None, (records[column], match.get("value"))))

                else:
                    nest = (
                        [next(reversed(records)) + "_" + value for value in
                         records[next(reversed(records))].split()],
                        re.compile(r"^\s*" + r"(\d+\.?\d*)\s*" *
                                   len (records.pop(next(reversed(records))).split())
                                   + r"$")) if not nest else nest
                    match = nest[1].match(line).groups() if \
                        nest[1].match(line) else None
                    for idx, nestcol in enumerate(nest[0]):
                        records[nestcol] = [] if nestcol not in records \
                            else records[nestcol]
                        records[nestcol] = records[nestcol] + \
                            [match[idx]] if match else records[nestcol]

            dfs.append((pd.DataFrame(records)))

    return pd.concat(dfs, sort=False)
if __name__ == "__main__":
    df3 = prog3("./datafullPS")
    df3.to_csv("recup_PS.csv")
