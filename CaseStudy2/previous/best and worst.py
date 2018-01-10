# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 16:25:06 2017

@author: Jonny
"""

import pandas as pd
import pymongo


#Connects with the mongodb client
client = pymongo.MongoClient("mongodb://admin:ds501@casestudy2-shard-00-00-z2tsj.mongodb.net:27017,casestudy2-shard-00-01-z2tsj.mongodb.net:27017,casestudy2-shard-00-02-z2tsj.mongodb.net:27017/test?ssl=true&replicaSet=CaseStudy2-shard-0&authSource=admin")

#Connects to collection in mondgo db
#Likely would make sense to rename this but I didn't have time
db=client['data_agg_1M']

#Connects to the table in mongodb
dbmovielens=db['data_agg_1M']


allfields=['movie_id','rating']

cursor = dbmovielens.find({})
movielensDF = pd.DataFrame(list(cursor), columns = allfields)

movie_rate_freq = movielensDF['movie_id'].value_counts()

seen_IDs = movie_rate_freq.index.tolist()
seen_IDs = seen_IDs[:int(len(seen_IDs)/2)]


seen_movies = movielensDF.query('movie_id not in @seen_IDs')
seen_movies_pivot = seen_movies.pivot_table('rating',index='movie_id',aggfunc='mean')

seen_movies_pivot =  seen_movies_pivot.sort_values('rating', ascending= False)

bottom_percentile = 5 # can change this to whatever percentile you want
top_percentile = 5 # can change this to whatever percentile you want
num_movies = len(seen_IDs)

bottom_position = int((bottom_percentile/100)*(num_movies + 1))
top_position = int((top_percentile/100)*(num_movies + 1))

worst_movies = seen_movies_pivot[-bottom_position:] # dataFrame that has the worst movies and their average rating
worst_movies_list = worst_movies.index.tolist() # list of straight up movie_id of the worst movies
best_movies = seen_movies_pivot[:top_position] # dataFrame that has the best movies and their average rating
best_movies_list = best_movies.index.tolist() # list of straight up movie_id of the best movies


client.close()

