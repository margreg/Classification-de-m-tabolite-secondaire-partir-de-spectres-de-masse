import glob
import os
import re
import pandas as pd
import unicodedata
from collections import OrderedDict

# EXPRESSION REGULIERE (Regular Expression)
# CF https://regex101.com/ pour les prochaines (le sauveur)
REG = re.compile(r"^(?P<root>[A-Z_]*\$?[A-Z_]+): *(?P<opt>[A-Z0-9_\/]+)? +"
                 r"(?P<value>[A-Za-z\[\]+()\-0-9 \/.;&,:~<%>'?^\$_{}=#]+)?\s*$")

def prog1(folder_path):
    dfs = []

    for filename in glob.glob(os.path.join(folder_path, '*.txt')):

        nest = False
        records =OrderedDict()
        # L'utilisation de with permet de cloturer automatiquement le fichier.
        with open(filename, 'r', encoding="utf8") as opened_txt:
            for line in opened_txt:
                #supprime les characteres qui sont pas en utf8
                line = unicodedata.normalize('NFD', line).encode(
                    'ascii', 'ignore').decode('utf-8')
                # On utilise le regex pour stocker les différentes valeurs dans
                #  un dictionnaire temporaire grace a la methode groupdict
                match = REG.match(line).groupdict() if REG.match(line) else \
                    False
                # Si match, la nouvelle variable est stocké en verifiant qu'elle
                # n'existe pas dans le dictionnaire
                if match:
                    nest = False
                    # Pour le nom de la clé, on concatene root avec opt.
                    # Comme opt peut etre égal à None,
                    # on filtre la liste avant d'appliquer la methode join
                    column = "_".join(
                        filter(None, (match.get("root"), match.get("opt"))))
                    # Sauvegarde dans le dict ordonné "records" en verifiant
                    # que la cle n'existe pas deja, sinon on ajoute la valeur
                    # a l'existante
                    records[column] = match.get("value") \
                        if column not in records else " ".join(
                        filter(None, (records[column], match.get("value"))))

                else:
                    # Sinon il s'agit des valeurs de la dernière variable
                    # Si la ligne ne contient pas de variable, il s'agit soit
                    #  de la fin du fichier ou de sous variables associees a la
                    # variable precedente.
                    # On a dans ce cas besoin d'une nouvelle regex.
                    # Pour eviter d'afficher les variables en double on supprime
                    # les anciennes valeurs avec la methode pop
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
    df1 = prog1("./datafullPM")
    df1.to_csv("recup_PM.csv")