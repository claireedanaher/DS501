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

#The variable cursor is used to identify what you would like to search for
cursor=dbmovielens.find({'title':"Erin Brockovich (2000)"})

#Creates a dict for the dataframe
fields=['user_id','movie_id','rating','timestamp','title', 'genre', 'gender',  'age',  'occupation', 'zipcode' ]

#creates a dataframe containing all of the records associated with the term queried for via the cursor 
movielens=pd.DataFrame(list(cursor),columns=fields)

#Prints the results
print(movielens)

client.close()

###################################################################################################################################


###################################################################################################################################
# CONNECT TO MONGODB ATLAS
###################################################################################################################################

#Connects with the mongodb client
client = pymongo.MongoClient("mongodb://admin:ds501@casestudy2-shard-00-00-z2tsj.mongodb.net:27017,casestudy2-shard-00-01-z2tsj.mongodb.net:27017,casestudy2-shard-00-02-z2tsj.mongodb.net:27017/test?ssl=true&replicaSet=CaseStudy2-shard-0&authSource=admin")

#Connects to collection in mondgo db
#Likely would make sense to rename this but I didn't have time
db=client['data_agg_1M']

#Connects to the table in mongodb with the tag info
dbmovielens=db['tag_data']

#The variable cursor is used to identify what you would like to search for
cursor=dbmovielens.find({'tag':'Mark Waters'})

#Creates a dict for the dataframe
fields=['user_id','movie_id','tag','timestamp','title', 'genre' ]

#creates a dataframe containing all of the records associated with the term queried for via the cursor 
movielens=pd.DataFrame(list(cursor),columns=fields)

#Prints the results
print(movielens)

client.close()

###################################################################################################################################



