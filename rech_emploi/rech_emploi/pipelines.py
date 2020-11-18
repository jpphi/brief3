# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from pymongo import MongoClient
import logging

from rech_emploi.items import RechEmploiItem
#from Bot_Scrap_Offre.items import BotScrapOffreItem

class RechEmploiPipeline:

    collection_name = 'offres_emploi2'

    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
    	## pull the information for settings.py
    	return cls(
    	    mongo_db = crawler.settings.get('MONGO_DATABASE')
            )   

    def open_spider(self, spider):
        ## intitializing spider opening db connection
        self.client = MongoClient()
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()


#    def process_item(self, item, spider):
#        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#        return item



    def process_item(self, item, spider):
        ## how to handle each post
        self.db[self.collection_name].find_one_and_update(
            {"guid": item["guid"]},
            {"$set": dict(item)},           
            upsert=True
        )
        logging.debug ("Post added to MongoDB")
        return item
    


"""
print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")


client = MongoClient("localhost", 27017)
db = client["test"]
CollectionMaongodb1 = db["offre_emploi2"]
with open("toto.json") as f:
    file_data = json.load(f)

for ident in file_data:
    guid = ident ["guid"] [0]
    rest= CollectionMaongodb1.find({"guid":guid})
    #print (rest.count())
    if rest.count() ==0:
        CollectionMaongodb1.insert_one(ident)
        print("doceument inserted", ident ["title"])

#CollectionMaongodb1.insert_many(file_data)
#client.close()



client = MongoClient("localhost", 27017)
db = client["data-mangodb"]
CollectionMaongodb1 = db["CollectionMaongodb1"]

"""