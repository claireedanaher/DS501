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





df = pd.read_csv('C:/WPI/DS501/CaseStudy/CaseStudy4/soundcloud.csv')
df.head()



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
    display_scores(vectorizor,tfid_result)
    


def display_scores(vectorizer, tfidf_result):
    # http://stackoverflow.com/questions/16078015/
    scores = zip(vectorizer.get_feature_names(),
                 np.asarray(tfidf_result.sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
   # end=len(sorted_scores)
    for item in sorted_scores[:20]:
        print ("{0:20} Score: {1}".format(item[0], item[1]))
            
    
    
    
    
    
          
          
################################################################################################
#NYC
################################################################################################         
ny_cities = ['New York','New York City','NYC','new york city','New York & Philadelphia','New York, NY','NEW YORK','New York/ L.A.','NY']
df_newyork = df.loc[df['city'].isin(ny_cities)]
df_newyork.shape
df_newyork.loc[df_newyork['city'].isin(ny_cities), 'city'] = 'New York City'
df_newyork.head()
df_newyork['city'].value_counts()

          
df_nyc =explode(df_newyork.assign(var1=df_newyork.genres_list.str.split(',')), 'var1')
df_nyc_csv = explode(df_nyc.assign(var2 = df_nyc.tags_list.str.split(',')),'var2')

df_city=df_nyc_csv*1
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

df_city['City']="New York City"
df_city['State']="NY"
df_city[1:5]
df_agg=df_city*1


city_genre=df_city['genre'].value_counts()
city_genre[1:5]


genres_pivot = df_city.pivot_table('tag',index='genre',aggfunc='count')



genres_pivot =  genres_pivot.sort_values('tag', ascending= False)
genres_pivot

top_genres = genres_pivot[0:1]
top_genres
top_genres =top_genres.index.tolist() # list of straight up movie_id of the worst movies
top_genres

genre=top_genres[:1]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)


genre=top_genres[1:2]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)

genre=top_genres[2:3]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)






################################################################################################
#Boston
################################################################################################         
boston_cities = ['Boston','Boston, Texas','Boston MA ,United states','Boston, Massachusetts - Austin, Texas','Boston, Massachusetts ','BOSTON','Boston, Massachusetts']
df_boston = df.loc[df['city'].isin(boston_cities)]
df_boston.shape
df_boston.loc[df_boston['city'].isin(boston_cities), 'city'] = 'Boston'
df_boston.head()
df_boston['city'].value_counts()


       
df_boston =explode(df_boston.assign(var1=df_boston.genres_list.str.split(',')), 'var1')
df_boston_csv = explode(df_boston.assign(var2 = df_boston.tags_list.str.split(',')),'var2')
df_boston[1:5]

df_city=df_boston_csv*1
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

df_city[1:5]
df_city['City']="Boston"
df_city['State']="MA"
df_city[1:5]


city_genre=df_city['genre'].value_counts()
city_genre[1:5]


genres_pivot = df_city.pivot_table('tag',index='genre',aggfunc='count')



genres_pivot =  genres_pivot.sort_values('tag', ascending= False)
genres_pivot

top_genres = genres_pivot[1:4]
top_genres
top_genres =top_genres.index.tolist() # list of straight up movie_id of the worst movies
top_genres

genre=top_genres[:1]
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)


genre=top_genres[1:2]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)

genre=top_genres[2:3]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)





################################################################################################


la_cities = ['Los Angeles, CA','Los Angeles','L.A','Los Angeles Area','Los Angeles, California','Los Angeles // Santa Barbara','los angeles','Los Angeles, California','LOS ANGELES','LosAngeles','Los Angeles, CA + Phoenix, AZ']
df_la = df.loc[df['city'].isin(la_cities)]
df_la.shape
df_la.loc[df_la['city'].isin(la_cities), 'city'] = 'Los Angeles'
df_la.head()
df_la['city'].value_counts()


       
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

df_city[1:5]
df_city['City']="Los Angeles"
df_city['State']="CA"
df_city[1:5]

df_city['genre'].value_counts()




city_genre=df_city['genre'].value_counts()
city_genre[1:5]


genres_pivot = df_city.pivot_table('tag',index='genre',aggfunc='count')



genres_pivot =  genres_pivot.sort_values('tag', ascending= False)
genres_pivot

top_genres = genres_pivot[1:4]
top_genres
top_genres =top_genres.index.tolist() # list of straight up movie_id of the worst movies
top_genres

genre=top_genres[:1]
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)


genre=top_genres[1:2]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)

genre=top_genres[2:3]
genre
tags_top_genre=df_city.query('genre in @genre')

doc = tags_top_genre['tag'].tolist()

val_max_feature=200
val_min_df=1
val_max_df=0.98
val_ngram_range=(1,3)

vector(doc,val_max_feature,val_min_df,val_max_df,val_ngram_range)




