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




#####################################################################
#EXPORT JSON FILE
#invar=variable containing data to be converted to json
#filename=file name for the json data to be save to
##################  START   ############################################
def json_export(invar,filename):
    data=invar.reset_index().to_json(orient='records')
    file = open(filename,'w')
    file.write(data)
    file.close()
    return(data)
###################  END  ##################################################





def main():
    outfile='C:/WPI/DS501/CaseStudy/CaseStudy2/Data/1M/data_agg_1M.json'
    obj_json=json_export(data_agg_1M,outfile)
    
main()


###################################################################################################################################
# CONNECT TO MONGODB ATLAS
###################################################################################################################################


client = pymongo.MongoClient("mongodb://admin:ds501@ds502casestudy2-shard-00-00-z2tsj.mongodb.net:27017,ds502casestudy2-shard-00-01-z2tsj.mongodb.net:27017,ds502casestudy2-shard-00-02-z2tsj.mongodb.net:27017/test?ssl=true&replicaSet=DS502CaseStudy2-shard-0&authSource=admin")



###################################################################################################################################



