# Job Recommender

## Goal
To recommend careers to students based on their age, degree, gender, and major. This repository contains the exploratory data analysis iPython file and python scripts to run the recommender system.

## Dataset
The `data.csv` file contains a list of professions and the corresponding features of each person in that profession. The features include the person's gender, age, highest-degree achieved, and major.

## Algorithm
The core algorithm can be split into two parts: 
1. find the best profession for a prospective student
2. find the 9 most relevant professions for the best profession from #1

The recommender system uses collaborative filtering. The two parts are unified at the end to produce the final product.

### Finding the best profession
To find the best profession for a student, I transformed the dataset by looking at previous similar students and see what professions they went into. A matrix of probabilities is computed for each profession and each possible feature combination of the student. The top profession is the profession with the highest probability for a student with the features given.

### Finding similar professions
Item-based collaborative filtering was used to find similar professions. I created a matrix filled with the cosine similarities between every pair of profession. The pair with the highest cosine score are the most similar. I then parsed out the matrix and stored the nine most similar professions for each profession. 

Once a top profession is calculated, I simply get the nine most relevant professions from that cosine similarity matrix. 

## Website
https://ancient-beyond-95266.herokuapp.com/

All the code for the website is in the `career-recommendation-app` folder.
