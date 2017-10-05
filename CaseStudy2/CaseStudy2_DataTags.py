###CASE STUDY 2####
import sys
import pandas as pd
import json
import pymongo
from pymongo import MongoClient


###################################################################################################################################
# IMPORT 1M Data
###################################################################################################################################
ratings=pd.read_table("C:/WPI/DS501/CaseStudy/CaseStudy2/Data/1M/ratings.dat", sep='::', names=['user_id', 'movie_id', 'rating','timestamp'])
ratings
users=pd.read_table('C:/WPI/DS501/CaseStudy/CaseStudy2/Data/1M/users.dat',  sep='::', names=['user_id', 'gender', 'age', 'occupation', 'zipcode'])
users
movies=pd.read_table('C:/WPI/DS501/CaseStudy/CaseStudy2/Data/1M/movies.dat',  sep='::', names=['movie_id', 'title', 'genre'])
users
# AGGREGATE INTO ONE FLAT FILE NAMES data_agg_1M
data_agg_1M=pd.merge(ratings, movies, on='movie_id')
data_agg_1M=pd.merge(data_agg_1M, users ,on='user_id')
###################################################################################################################################




###################################################################################################################################
# IMPORT TAG AND MOVIE TITLE INFO FROM 20M data
###################################################################################################################################

movies_tags=pd.read_csv("C:/WPI/DS501/CaseStudy/CaseStudy2/Data/20M/movies.csv", names=['movie_id', 'title', 'genre'])
movies_tags=movies_tags.drop(0)
movies_tags

tags=pd.read_csv("C:/WPI/DS501/CaseStudy/CaseStudy2/Data/20M/tags.csv", names=['user_id', 'movie_id', 'tag', 'timestamp'])
tags=tags.drop(0)
tags
# AGGREGATE INTO ONE FLAT FILE NAMES tagg_agg
tag_agg=pd.merge(tags,movies_tags,on='movie_id')

###################################################################################################################################



###################################################################################################################################
#CONSISTENCY CHECK
#PURPOSE: Determine differences in movie titles with 1M and 20M data sets
###################################################################################################################################

#RETURNS TRUE/FALSE with counts of matching titles from 1M to 20M
movies['title'].isin(movies_tags['title']).value_counts()
#True     3361
#False     522

#RETURNS TRUE/FALSE with counts of matching titles from 20M to 10M
movies_tags['title'].isin(movies['title']).value_counts()
#False    23914
#True      3364

###################################################################################################################################
#OUTCOME1: NUMBERS PROVE TO BE CONSISTANT WITH MERGE
#OUTCOME2:  522 out of 3883 movies are in 1M but not 20M accounting for approx 13% of the movies
###################################################################################################################################

movielens=pd.merge(data_agg_1M,tag_agg,how='left', on='title')
movielens.drop('user_id_y', axis=1)
movielens.drop('movie_id_y', axis=1)
movielens.drop('timestamp_y', axis=1)               
movielens.drop('genre_y', axis=1)    



