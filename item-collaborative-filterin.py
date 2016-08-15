import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

df_data = pd.read_csv('data.csv')

for column in df_data:
  if column not in ['SOC Code', 'Detailed SOC Occupation', 'Sample Name']:
    df_data[column] = df_data[column].fillna(0)
    df_data[column] = df_data[column].astype(int)

df_occ = df_data.drop(['SOC Code', 'Sample Name'], axis=1)
# group by detailed occupation
df_occ = df_occ.groupby(df_occ['Detailed SOC Occupation']).apply(np.sum)

numeric_columns = df_occ._get_numeric_data()
normalized_numeric_df = numeric_columns.copy()
normalized_numeric_df = numeric_columns.div(numeric_columns.sum(axis=1), axis=0)
normalized_numeric_df = normalized_numeric_df.fillna(0)


# Item-based collaborative filtering
data_ibs = pd.DataFrame(index=normalized_numeric_transponse_df.columns,columns=normalized_numeric_transponse_df.columns)
 
for i in range(0,len(data_ibs.columns)) :
    for j in range(0,len(data_ibs.columns)) :
      # Use cosine similarities
      data_ibs.ix[i,j] = 1-cosine(normalized_numeric_transponse_df.ix[:,i],normalized_numeric_transponse_df.ix[:,j])
 
# Create a placeholder items for closes neighbours to an item
data_neighbors = pd.DataFrame(index=data_ibs.columns,columns=[range(1,11)])
 
# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(0,len(data_ibs.columns)):
    data_neighbors.ix[i,:10] = data_ibs.ix[0:,i].sort_values(ascending=False)[:10].index