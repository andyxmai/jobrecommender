import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

df_data_floats = pd.read_csv('data.csv')
df_data_transpose = df_data_floats.transpose()

print 'computing feature_norm_transpose'
feature_norm_transpose = df_data_transpose.copy()
for column in df_data_transpose:
  idx = int(column)
  if df_data_transpose[column]['Sample Name'] == 'Males':
    sum_df = df_data_transpose[idx+1] + df_data_transpose[idx]
    feature_norm_transpose[idx][3:] = df_data_transpose[idx][3:].divide(sum_df[3:])
    feature_norm_transpose[idx+1][3:] = df_data_transpose[idx+1][3:].divide(sum_df[3:])
  
  if df_data_transpose[column]['Sample Name'] == 'Highest Degree Associates':
    sum_df = df_data_transpose[idx] + df_data_transpose[idx+1] + df_data_transpose[idx+2] + df_data_transpose[idx+3]
    feature_norm_transpose[idx][3:] = df_data_transpose[idx][3:].divide(sum_df[3:])
    feature_norm_transpose[idx+1][3:] = df_data_transpose[idx+1][3:].divide(sum_df[3:])
    feature_norm_transpose[idx+2][3:] = df_data_transpose[idx+2][3:].divide(sum_df[3:])
    feature_norm_transpose[idx+3][3:] = df_data_transpose[idx+3][3:].divide(sum_df[3:])
  
  if df_data_transpose[column]['Sample Name'] == 'Gen Y (1982-2000)':
    sum_df = df_data_transpose[idx] + df_data_transpose[idx+1] + df_data_transpose[idx+2]
    feature_norm_transpose[idx][3:] = df_data_transpose[idx][3:].divide(sum_df[3:])
    feature_norm_transpose[idx+1][3:] = df_data_transpose[idx+1][3:].divide(sum_df[3:])
    feature_norm_transpose[idx+2][3:] = df_data_transpose[idx+2][3:].divide(sum_df[3:])

feature_norm = feature_norm_transpose.transpose()
feature_norm = feature_norm.fillna(0.000001)

print 'computing computed_df'
computed_df = pd.DataFrame()
for column in feature_norm_transpose:
  idx = int(column)
  occ_name = feature_norm_transpose[column]['Detailed SOC Occupation']
  if feature_norm_transpose[column]['Sample Name'] == 'Males':
    gender_name = feature_norm_transpose[column]['Sample Name']
    gender_probs = feature_norm_transpose[column][3:]
    for i in range(4):
      degree_idx = idx + 2 + i
      degree_name = feature_norm_transpose[degree_idx]['Sample Name']
      degree_probs = feature_norm_transpose[degree_idx][3:]
      for j in range(3):
        age_idx = idx + 6 + j
        age_name = feature_norm_transpose[age_idx]['Sample Name']
        age_probs = feature_norm_transpose[age_idx][3:]
        
        name = "{}+{}+{}+{}".format(gender_name, degree_name, age_name, occ_name)
        
        bucket_probs = gender_probs * degree_probs * age_probs
        bucket_df = pd.DataFrame({name: bucket_probs})
        if idx == 1:
          computed_df = bucket_df
        else:
          computed_df[name] = bucket_probs
  
  if feature_norm_transpose[column]['Sample Name'] == 'Females':
    gender_name = feature_norm_transpose[column]['Sample Name']
    gender_probs = feature_norm_transpose[column][3:]
    for i in range(4):
      degree_idx = idx + 1 + i
      degree_name = feature_norm_transpose[degree_idx]['Sample Name']
      degree_probs = feature_norm_transpose[degree_idx][3:]
      for j in range(3):
        age_idx = idx + 5 + j
        age_name = feature_norm_transpose[age_idx]['Sample Name']
        age_probs = feature_norm_transpose[age_idx][3:]
        
        name = "{}+{}+{}+{}".format(gender_name, degree_name, age_name, occ_name)
        
        bucket_probs = gender_probs * degree_probs * age_probs
        bucket_df = pd.DataFrame({name: bucket_probs})
        if idx == 1:
          computed_df = bucket_df
        else:
          computed_df[name] = bucket_probs

computed_df = computed_df.fillna(0)

print 'computing best_job'
best_job = {}
for i in range(len(computed_df)):
  if i % 100 == 0:
      print 'At row {}...'.format(i)
  major = computed_df.index[i]
  for j in range(len(computed_df.columns)):
    if j % 1000 == 0:
      print 'At row {} col {}...'.format(i, j)
      
    if computed_df.iloc[i,j] == 0:
      continue
    
    tokens = computed_df.columns[j].split("+")
    occ = tokens[-1]
    feature_name = "+".join(tokens[:-1])
    feature_name += "+" + major
    if feature_name not in best_job:
      best_job[feature_name] = [occ, computed_df.iloc[i,j]]
    elif best_job[feature_name][1] < computed_df.iloc[i,j]:
      best_job[feature_name] = [occ, computed_df.iloc[i,j]]

import json
with open('best_job.json', 'w') as fp:
  json.dump(best_job, fp)