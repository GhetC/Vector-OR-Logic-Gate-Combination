import numpy as np
import pandas as pd
from google.colab import files
from google.colab import drive


print ("Enter Path (without Quotation marks):")
path=input()
df=pd.read_excel(path)

species_names = list(df.columns)
df=df.to_numpy()

cols=len(df[0,1:])
rows=len(df[:,0])

def pair_compare(row1,row2):       
  comb_lst=([])
  for i in range(cols):
    if row1[i]==1 or row2[i]==1:
     comb_lst=np.append(comb_lst, int(1))
    else:
      comb_lst=np.append(comb_lst, int(0))
  comb_lst=comb_lst.reshape((cols,1))
  return comb_lst.astype(int), int(sum(comb_lst))



def Pairs_full_table(dataframe):
  names_lst=([])
  sums_lst=([])
  pairs_matrix=np.full((cols,1),2,dtype=int)
  for j in range(0, rows-1):
    for i in range(j+1,rows):
      overlap=False
      row1_ints=[]
      row2_ints=[]
      pair_name=None

      if type(dataframe[j,0])==str or type(dataframe[i,0])==str:
        row1_ints=list(map(int, dataframe[j,0].split(",")))
        row2_ints=list(map(int, dataframe[i,0].split(",")))

      for x in row1_ints:
        if x in row2_ints:
          overlap=True
          break

      if overlap==True:
        continue
      
      if row1_ints==[] or row2_ints==[]:
        pair_name=str(dataframe[j,0])+","+str(dataframe[i,0])
      
      if row1_ints!=[] or row2_ints!=[]:
        comb_rows=row1_ints+row2_ints
        comb_rows.sort()
        pair_name=",".join(map(str, comb_rows))
      
      if pair_name in names_lst:
        continue
      
      else:
        names_lst=np.append(names_lst, pair_name)

        P=pair_compare(dataframe[j,1:],dataframe[i,1:])
        Tuple=[pair_name, P[1]]
        sums_lst.append(Tuple)
        if np.all(pairs_matrix==2):
          pairs_matrix=P[0]
        else:
          pairs_matrix=np.concatenate((pairs_matrix,P[0]), axis=1)

  return sums_lst, pairs_matrix.T


Pairs=Pairs_full_table(df)

index_names=[a[0] for a in Pairs[0]]
Total_species=[a[1] for a in Pairs[0]]
df1=pd.DataFrame(Pairs[1])
df1.index = index_names
df1.columns =species_names[1:]
df1=df1.assign(Total=Total_species)
df1
print ("Enter Path (without Quotation marks):")
out_path=input()
with pd.ExcelWriter(out_path) as writer:
    df1.to_excel(writer, "Pairs")
