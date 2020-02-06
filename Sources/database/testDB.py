import numpy as np
from pymongo import MongoClient
from pprint import pprint
import random
import Potential_field as pf
import matplotlib.pyplot as plt
from bson.objectid import ObjectId
import seaborn as sns

client = MongoClient("localhost:27017")
db = client.admin

serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)

#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db=client.map
# #Step 2: Create sample data
# names = ['Kitchen','Animal','State', 'Tastey', 'Big','City','Fish', 'Pizza','Goat', 'Salty','Sandwich','Lazy', 'Fun']
# company_type = ['LLC','Inc','Company','Corporation']
# company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
# for x in range(1, 501):
#     business = {
#         'name' : names[random.randint(0, (len(names)-1))] + ' ' + names[random.randint(0, (len(names)-1))]  + ' ' + company_type[random.randint(0, (len(company_type)-1))],
#         'rating' : random.randint(1, 5),
#         'cuisine' : company_cuisine[random.randint(0, (len(company_cuisine)-1))]
#     }
#     #Step 3: Insert business object directly into MongoDB via isnert_one
#     result=db.reviews.insert_one(business)
#     #Step 4: Print to the console the ObjectID of the new document
#     print('Created {0} of 500 as {1}'.format(x,result.inserted_id))
# #Step 5: Tell us that you are done
# print('finished creating 500 business reviews')

# fivestarcount = db.reviews.find({'rating': 5}).count()
# print(fivestarcount)


# # Now let's use the aggregation framework to sum the occurrence of each rating across the entire data set
# print('\nThe sum of each rating occurance across all data grouped by rating ')
# stargroup=db.reviews.aggregate(
# # The Aggregation Pipeline is defined as an array of different operations
# [
# # The first stage in this pipe is to group data
# { '$group':
#     { '_id': "$rating",
#      "count" :
#                  { '$sum' :1 }
#     }
# },
# # The second stage in this pipe is to sort the data
# {"$sort":  { "_id":1}
# }
# # Close the array with the ] tag
# ] )
# # Print the result
# for group in stargroup:
#     print(group)

## GET AND SHOW MAP
# pfMap = db.pf.find_one({"mapNumber": 0})
#
# pmap = pfMap[u'pmap']
# xw = pfMap[u'xw']
# yw = pfMap[u'yw']
#
# np.interp(pmap, (min(map(min, pmap)), max(map(max, pmap))), (0, 1))
#
# #pmap = np.array(pmap)
# #pmap = np.array(pmap) - max(map(max, pmap))
# #pmap[pmap > -0.5] = 0.5
#
# pf.draw_heatmap(pmap, xw, yw)
#
# plt.show()

## UPDATE FIELD
#db.pf.update_one({"_id": ObjectId("5e27573f13a4340b3ae180c1")}, {"$set": {"mapNumber": 0}})

## 2D heatmap
# pfMap = db.pf.find_one({"mapNumber": 0})
#
# pmap = pfMap[u'pmap']
# xw = pfMap[u'xw']
# yw = pfMap[u'yw']
#
# pmap = np.array(pmap)
#
# plt.imshow(pmap, cmap='hot', interpolation='nearest')
# plt.show()

## TEST GETOBJECT
objectID = 0
db = client.map


pfMap = db.objects.find_one({"id": objectID})

print ""