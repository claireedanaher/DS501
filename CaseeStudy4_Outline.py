###CASE STUDY 2####
import sys
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import numpy as np


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics


#final_df.to_csv("ckjhafkjha.csv",index=False)


df = pd.read_csv('C:/WPI/DS501/CaseStudy/CaseStudy4/soundcloud.csv')
df.head()

chicago = ['Chicago','Chicago IL and Anaheim Ca','CHICAGO IL, The Almighty WestSide','Chicago Illinois','Chicago, Illinois','Chicago/Albuquerque/Stuttgart','Chicagoland']
miami = ['Fort Lauderdale / Miami Beach area in Florida','miami','MIAMI','Miami Beach','Miami Beach - Florida','Miami Beach / Los Angeles /','Miami,Fl']
houston = ['Houston','Houston, Texas','Houston ','HOUSTON TEXAS','Houston Tx','houston,texas,united states','Houston`','PORT ARTHUR/HOUSTON/LOS ANGELES/DALLAS/HAMPTON VA.']
denver= ['Denver','Denver, CO','Denver','Denver, Colorado']
nashville= ['Nashville','Nashville','NASHVILLE, TENNESSEE','Nashville, TN']
DC=['Washington DC','Washington, D.C.','Washington D.C.','Washington, DC','Washington D. C.','Washington, D.C','washington,d.c']
boston = ['Boston','Boston, Texas','Boston MA ,United states','Boston, Massachusetts - Austin, Texas','Boston, Massachusetts ','BOSTON','Boston, Massachusetts']
la= ['Los Angeles, CA','Los Angeles','L.A','Los Angeles Area','Los Angeles, California','Los Angeles // Santa Barbara','los angeles','Los Angeles, California','LOS ANGELES','LosAngeles','Los Angeles, CA + Phoenix, AZ']
nyc = ['New York','New York City','NYC','new york city','New York & Philadelphia','New York, NY','NEW YORK','New York/ L.A.','NY']



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
    
    
#####################################################################
#Extract info from raw file
##################  START   ############################################    

def explode(df, lst_cols, fill_value=''):
    # make sure `lst_cols` is a list
    if lst_cols and not isinstance(lst_cols, list):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)

    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()

    if (lens > 0).all():
        # ALL lists in cells aren't empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .loc[:, df.columns]
    else:
        # at least one list in cells is empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .append(df.loc[lens==0, idx_cols]).fillna(fill_value) \
          .loc[:, df.columns]
          
###################  END  ##################################################
          
    
    
def vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range):
    vectorizor=TfidfVectorizer(doc,max_features=val_max_feature,
                           min_df=val_min_df,max_df=val_max_df,
                           stop_words='english',
                           ngram_range=val_ngram_range)

    tfid_result=vectorizor.fit_transform(doc)
    top_tags=display_scores(vectorizor,tfid_result)
    
    return(top_tags)


def display_scores(vectorizer, tfidf_result):
    # http://stackoverflow.com/questions/16078015/
    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(tfidf_result.sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
   # end=len(sorted_scores)
    out_list = []
    for item in sorted_scores[:10]:
        out_list.append(item[0])
    return(out_list)
            
################################################################################################
#City1
################################################################################################


la_cities = ['Los Angeles, CA','Los Angeles','L.A','Los Angeles Area','Los Angeles, California','Los Angeles // Santa Barbara','los angeles','Los Angeles, California','LOS ANGELES','LosAngeles','Los Angeles, CA + Phoenix, AZ']
df_la = df.loc[df['city'].isin(la_cities)]
df_la.loc[df_la['city'].isin(la_cities), 'city'] = 'Los Angeles'
df_la.head()
df_la['city'].value_counts()

final_df.to_csv("export",index=False)
       
df_la =explode(df_la.assign(var1=df_la.genres_list.str.split(',')), 'var1')
df_la_csv = explode(df_la.assign(var2 = df_la.tags_list.str.split(',')),'var2')
df_la[1:5]







df_city=df_la_csv*1
del df_city['genres_list']
del df_city['tags_list']
del df_city['city']
df_city=df_city.rename(columns={'var1':'genre','var2':'tag'})
df_city["genre"] = df_city["genre"].str.replace("[", "")
df_city["genre"] = df_city["genre"].str.replace("]", "")
df_city["genre"] = df_city["genre"].str.replace("'", "")
df_city["tag"] = df_city["tag"].str.replace("[", "")
df_city["tag"] = df_city["tag"].str.replace("]", "")
df_city["tag"] = df_city["tag"].str.replace("'", "")
df_city["tag"] = df_city["tag"].str.replace('"', "")
df_city["genre"]=df_city["genre"].str.lower()
df_city["tag"]=df_city["tag"].str.lower()

df_city[1:5]

#uniques = df_city['genre'].unique()
#print(uniques)


genres_pivot = df_city.pivot_table('tag',index='genre',aggfunc='count')
genres_pivot =  genres_pivot.sort_values('tag', ascending= False)

  
top_genres = genres_pivot[0:5]
print(top_genres)

genre_cnt=top_genres.ix[0,0]
genre_cnt
top_genres_list =top_genres.index.tolist() # list of straight up movie_id of the worst movies

genre=top_genres_list[0]



#######################################################################################
#CREATE TOP TAGS
tags_top_genre=df_city.query('genre in @top_genres_list')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

top_tags=vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)
top_tags
#######################################################################################

city_to_add = pd.Series()
city_to_add['code'] = 'NY'
city_to_add['state'] = 'New York'
city_to_add['category'] = 'state'
city_to_add['ranking_value'] = genre_cnt
city_to_add['City'] = "New York City"
city_to_add['Top Genre'] = genre
city_to_add['Tags'] = top_tags 



#code-state=two letters, state=state writte, city=city, category=genre, ranking_value 
COLUMN_TITLES = ['code','state', 'category', 'ranking_value','City','Top Genre', 'Tags']
final_df=pd.DataFrame(columns = COLUMN_TITLES)
final_df=final_df.append(city_to_add, ignore_index = True)

final_df
