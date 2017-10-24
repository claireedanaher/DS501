###CASE STUDY 2####
import sys
import pandas as pd
import json
import pymongo
import numpy as np
from pymongo import MongoClient




###################################################################################################################################
# CONNECT TO MONGODB ATLAS
###################################################################################################################################

#Connects with the mongodb client
client = pymongo.MongoClient("mongodb://admin:ds501@casestudy2-shard-00-00-z2tsj.mongodb.net:27017,casestudy2-shard-00-01-z2tsj.mongodb.net:27017,casestudy2-shard-00-02-z2tsj.mongodb.net:27017/test?ssl=true&replicaSet=CaseStudy2-shard-0&authSource=admin")

#Connects to collection in mondgo db
#Likely would make sense to rename this but I didn't have time
db=client['data_agg_1M']

#Connects to the table in mongodb
dbmovielens=db['data_agg_1M']
#Connects to the table in mongodb with the tag info
#dbTagData=db['tag_data']



###################################################################################################################################
# PULLS ALL DATA FROM MONGO DB AND CREATES A DATA FRAME CALLED movielensDF
###################################################################################################################################


allfields=['user_id','movie_id','rating','timestamp','title', 'genre', 'gender',  'age',  'occupation', 'zipcode' ]


cursor = dbmovielens.find({})
movielensDF = pd.DataFrame(list(cursor), columns = allfields)
movielensDF[:5]
movielensDF.dtypes()

movielensDF[:100]
###################################################################################################################################
# CALCULATES HIGH AVERAGE MOVIES
###################################################################################################################################
movie_avgrating=movielensDF.pivot_table('rating',index='title',aggfunc='mean')
highavg_movie=movie_avgrating[movie_avgrating['rating']>=4.5]
high_avgcnt=len(highavg)
print('The total number of movies with an average rating of at least 4.5 is '+str(high_avgcnt))

###################################################################################################################################
# CREATES GENDER SPECIFIC DFs
###################################################################################################################################
fem_reviews=movielensDF
#REMOVE= CRITERIA FOR REMOVAL
remove=['M']
#REMOVES RECORDS FROM DATA FRAME BASED ON CRITIA
fem_reviews=fem_reviews.query('gender not in @remove')

fem_movies=fem_reviews.pivot_table('rating',index='title',aggfunc='mean')
highavg=fem_movies[fem_movies['rating']>=4.5]
high_avgcnt=len(highavg)
print('The total number of movies with an average rating of at least 4.5 among women is '+str(high_avgcnt))



male_reviews=movielensDF
remove=['F']
male_reviews=male_reviews.query('gender not in @remove')

male_reviews=male_reviews.pivot_table('rating',index='title',aggfunc='mean')
highavg=male_reviews[male_reviews['rating']>=4.5]
high_avgcnt=len(highavg)
print('The total number of movies with an average rating of at least 4.5 among men is '+str(high_avgcnt))







