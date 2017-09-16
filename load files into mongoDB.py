# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 23:41:42 2017

@author: Jonny
"""

import twitter
import pymongo
import json
import os

def main():
   client = pymongo.MongoClient()
   db = client['twitter']
   collection = db['Case1']
   
   # INSERT YOUR LOCAL GITHUB DIRECTORY BELOW
   directory = os.fsencode("C:/Users/Jonny/Documents/")
                     
   
   for file in os.listdir(directory):
       filename = os.fsdecode(file)
       if filename.startswith("Results"):
           with open(file, 'r') as raw_data:
               collection.insert_one(file)
               
           
        
    
    
main()