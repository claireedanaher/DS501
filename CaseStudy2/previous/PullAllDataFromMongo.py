###CASE STUDY 2####
import sys
import pandas as pd
import json
import pymongo
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



###################################################################################################################################
# PULLS ALL DATA FROM MONGO DB AND CREATES A DATA FRAME CALLED movielensDF
###################################################################################################################################


allfields=['user_id','movie_id','rating','timestamp','title', 'genre', 'gender',  'age',  'occupation', 'zipcode' ]


cursor = dbmovielens.find({})
movielensDF = pd.DataFrame(list(cursor), columns = allfields)
movielensDF[:5]




