import pandas as pd

df1=pd.read_csv('recup_PM.csv')
df2=pd.read_csv('recup_PT.csv')
df3=pd.read_csv('recup_PS.csv')



df1['PK$PEAK_int.']=df1['PK$PEAK_int.'].apply(float)
df1['CH$EXACT_MASS']=df1['CH$EXACT_MASS'].astype(object)
df1['AC$ANALYTICAL_CONDITION_COLLISION_ENERGY']=df1['AC$ANALYTICAL_CONDITION_COLLISION_ENERGY'].astype(object)
df1['MS$FOCUSED_ION_PRECURSOR_M/Z']=df1['MS$FOCUSED_ION_PRECURSOR_M/Z'].astype(object)

df2['CH$SMILES']=df2['CH$SMILES'].astype(object)
df2['CH$EXACT_MASS']=df2['CH$EXACT_MASS'].astype(object)
df2['AC$ANALYTICAL_CONDITION_COLLISION_ENERGY']=df2['AC$ANALYTICAL_CONDITION_COLLISION_ENERGY'].astype(object)
df2['MS$FOCUSED_ION_PRECURSOR_M/Z']=df2['MS$FOCUSED_ION_PRECURSOR_M/Z'].astype(object)

df3['CH$SMILES']=df3['CH$SMILES'].astype(object)
df3['CH$INCHI']=df3['CH$INCHI'].astype(object)
df3['PK$PEAK_m/z']=df3['PK$PEAK_m/z'].astype(float)
df3['AC$ANALYTICAL_CONDITION_COLLISION_ENERGY']=df3['AC$ANALYTICAL_CONDITION_COLLISION_ENERGY'].astype(object)
df3['PK$PEAK_int.']=df3['PK$PEAK_int.'].astype(float)


#df1.info()
#df2.info()
#df3.info()

df = pd.concat([df1, df2, df3])
df.to_csv("fulldata.csv")
#df.info()