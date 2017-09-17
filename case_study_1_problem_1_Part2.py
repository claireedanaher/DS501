# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 10:34:23 2017

@author: Claire Danaher
"""
import os
import json

def concatFiles(path):
    #path = 'C:/WPI/DS501/CaseStudy/CaseStudy1/rawtweets'
    os.chdir(path)
    files = os.listdir(path)
    parsed_data=[]
    all_tweets=[]
    for infile in files:
        with open(infile) as raw_data:
            row=[]
            row.append(infile)
            row.append(json.load(raw_data))
            
        parsed_data += row
        
    return(parsed_data)

def remove_duplicates(parsed_data):
    texts = []
    repeated_indices = []
    for index in range(len(parsed_data)):
        text = parsed_data[index]['text']
        if text in texts:
            repeated_indices.append(index)
        else:
            texts.append(text)
    
    # deletes repeated tweets
    for index in sorted(repeated_indices, reverse = True): 
        del parsed_data[index]
    return(parsed_data)

def parse_date(string):
    print(string)
    colon=string.find(':')
    start=colon-2
    end=colon
    time=string[start:end]
    month=string[4:7]
    day=string[8:10]
    date=month+day+'HR'+time
    return(date)
    
    

def parse_tweettime(parsed_data):
    senti_data=[]
    for tweet in parsed_data:
        row=[]
        s=tweet['created_at']
        dayhour=parse_date(s)
        row.append(dayhour)
        row.append(tweet['text'])
        senti_data.append(row)
    return(senti_data)

#####################################################################
#EXPORT JSON FILE
#invar=variable containing data to be converted to json
#filename=file name for the json data to be save to
##################  START   ############################################
def json_export(invar,filename):
    data= json.dumps(invar, indent=1)
    file = open(filename,'w')
    file.write(data)
    file.close()
###################  END  ##################################################    

def main():
    path="C:/WPI/DS501/CaseStudy/CaseStudy1/rawtweets"
    raw_data=concatFiles(path)
    print('Number of Raw Tweets: '+str(len(raw_data)))
    json_export(raw_data,'allresults.txt')
    
    
    
    #parsed_data=remove_duplicates(raw_data)
   # print('Number of Unique Tweets: '+str(len(parsed_data)))
    

    
    
main()   