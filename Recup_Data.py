# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:21:56 2018

@author: daido
"""
import pandas as pd
from collections import OrderedDict
dfvars = []
newvarflag = False

records = OrderedDict()
#test pour un fichier txt
with open(r"C:\Users\daido\Downloads\PM000104.txt") as opened_txt:
    for line in opened_txt:
        # Conversion de la ligne (string) en une liste de string pour recuperer l'information
        line = line.rstrip("\r\n").split(": ") if ":" in line else line.rstrip("\r\n").split()
        # Stocke nom colonne et valeurs si la ligne possede une variable
        column, record = line if len(line) == 2 else (None, line)
        if column and column.isupper():
            # Si nouvelle variable, on ajoute une nouvelle entree et ses valeurs dans les deux listes imbriquees
            # Si la ligne correspond a une variable existante, on ajoute uniquement les nouvelles valeurs
            records[column] = record if column not in records else ",".join([records[column], record])
        else:
            # Sinon la ligne ne contient pas de variable, il s'agit soit de la fin du fichier ou de sous variables associees a la variable precedente
            # On recupere le nom de la colonne precedente dans le dictionnaire records
            column = next(reversed(records))
            if not isinstance(records[column], list):
                column = tuple("_".join([column, subcolumn]) for subcolumn in records.pop(column).split())
                records[column] = [[] for i in range(0, len(column))]
            [records[column][i].append(subrecord) for i, subrecord in enumerate(record) if len(record) == len(column)]

print("Columns:")
print(records.keys())
print("Values:")
print(records.values())
print(records)


df = pd.DataFrame(records)
df.to_csv('mycsv.csv', index=False)
df = pd.read_csv('mycsv.csv')
df.head(30)