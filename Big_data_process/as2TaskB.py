
# coding: utf-8

# # FIT5148 Task B in Assessment 2
# #### Student Name: Jiahao Liu, Changze Chen
# #### Student ID: 27549593, 27717704
# 
# Date: 18 May 2018
# 
# Version: 3.0
# 
# Environment: Python 3.6.3.final.0 and 4.5.0

# ### 1. Based on the two data sets provided i.e. Fire data-Part 1 and Weather data-Part 1, design a suitable data model to support efficient querying of the two data sets in MongoDB. Justify your data model design

# # Data Model
# 
# **After reading [6 Rules of Thumb for MongoDB Schema Design](https://www.mongodb.com/blog/post/6-rules-of-thumb-for-mongodb-schema-design-part-1), and took the tasks we were going to do(TasksA2 - A8) into consideration, the modle we built was as follows:**
# 
# ```python
#   cliamte = {'Air Temperature (Celcius)': 21.0, #float
#              'Date': '2017-03-12', #datetime
#              'Fires': [{'_id': 'f2647'},
#                        {'_id': 'f2648'},
#                        {'_id': 'f2649'},
#                        {'_id': 'f2650'},
#                        {'_id': 'f2651'}], # a list of fire _id for reference
#              'MAX': '78.6*', 
#              'MIN': '60.3*', 
#              'Max Wind Speed': 11.1, 
#              'Precipitation': '0.00G', 
#              'Relative Humidity': 58.1,
#              'Station': '948701', 
#              'WindSpeed  (knots)': 5.3, 
#              '_id': 'c70'} # assigned a unique id for each climate document       
#             
#      fire = {'Confidence': 78.0, #float
#              'Date': '2017-12-27', #datetime
#              'Datetime': '2017-12-27 04:16:51', #datetime type, remove the 'T' 
#              'Latitude': -37.966, 
#              'Longtitude': 145.051, 
#              'Power': 26.7, 
#              'Surface Temperature (Celcius)': 68.0, 
#              'Surface Temperature (kelvin)': 341.8, 
#              '_id': 'f0',       # assigned a unique id for each fire document
#              'climate': 'c360'} # we are using two- way reference, so there also has a climate id in fire
# ```
# **JUSTIFICATION**
# 
# The data set we dealt with had a typical one to many relationship.
# The model we built was so-called **two-way referencing** It was a combined technology with both references from the 'one' side(climate), and from the 'many' side(fire).
# 
# -  Why don't we use embedding meodel?
# 
# Embedding model is hard to deal with task like find all information when the surface temperature was between 65 and 100.(TaskA3), It was **hard to access the embedded detials** as stand- alone entities.
# 
# -  Why don't we use one way reference?(one to many)
# 
# One way reference, generally means that in 'one' side, it has an 'id' attribute to refer to the 'many' side. But in this case, since we were **not only need to get information from fire in a climate** find(TaskA4), we also need to get information from climate in a fire find(TaskA5), Since the mongodb will automatically assign an index to '_id' attrivute, in order to have quicker and more efficient search function, we built up two way reference.

# In[ ]:


import pymongo 
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import multiprocessing as mp
from datetime import datetime


# ### 2. Create a new database in MongoDB. The new database will be based on the document model you have designed in Task B1

# In[ ]:


#Connect on the default host and port
client = MongoClient()

#Our new database called task2_db
db = client.task2_db


# ### 3. Write a python program that will read the data from Fire data-Part1 and Climate data-Part1 and load them to the new database created in Task B2

# In[ ]:


fileclimate = open("./ClimateData-Part1.csv", "r", encoding="utf-8")
filefire = open("./FireData-Part1.csv", "r", encoding="utf-8")

climateString = fileclimate.read()
fireString = filefire.read()

fileclimate.close()
filefire.close()

# split the long string to list of short string, each short string contains one record
c = climateString.split("\n")
f = fireString.split("\n")

# remove the space
c = [s.strip() for s in c]
f = [s.strip() for s in f]

# notice that there has a "" at the end of the list
while "" in c:
    c.remove("")
    
while "" in f:
    f.remove("")

# the first line is header which is useless for data
c = c[1:] 
f = f[1:]

climateData = []
for i in range(0,len(c)):
    climateData.append([elem.strip() for elem in c[i].split(',')])

fireData = []
for i in range(0,len(f)):
    fireData.append([elem.strip() for elem in f[i].split(',')])


# In[ ]:


# insert unique id for climate and fire
# Pattern:  climate starts from c0, fire starts from f0.
number = 0
for climate in climateData:
    climate.insert(0, 'c' + str(number))
    number +=1
    
number = 0
for fire in fireData:
    fire.insert(0, 'f' + str(number))
    number +=1


# In[ ]:


def create_fire(myCol):
       
    for fire in fireData:            
        for climate in climateData:            
            if climate[2] == fire[-2]: # if the date is the same
                climateofthatday = climate[0] # assign the climate id to fire id
        
        _date = datetime.strptime(fire[7], '%Y-%m-%d').strftime('%Y-%m-%d')
        _datetime = datetime.strptime(fire[4], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        #convert the string of 'Date' and 'Datetime' to datetime type 
        
        f = {
        '_id' : fire[0],
        'Latitude': float(fire[1]),
        'Longtitude': float(fire[2]),
        'Surface Temperature (kelvin)': float(fire[3]),
        'Datetime': _datetime,
        'Power': float(fire[5]),
        'Confidence': float(fire[6]),
        'Date': _date,
        'Surface Temperature (Celcius)': float(fire[8]),
        'climate': climateofthatday
        }
        myCol.insert_one(f)
        
db.fire.drop() # in case duplicated import data
fireCol = db.fire
create_fire(fireCol)

# You can use this code to check the data input to the database
#results = fireCol.find()
#for d in results:
#    pprint(d)


# In[ ]:


def create_climate(myCol):
    fires = []      
    for climate in climateData:            
        for fire in fireData:            
            if climate[2] == fire[-2]: # if the dates are matched
                fires.append({'_id' : fire[0] })  
                # assign fire id into the climate as a list of dictionary
                
        _date = datetime.strptime(climate[2], '%Y-%m-%d').strftime('%Y-%m-%d') 
        #convert string of 'Date' to datetime
        
        c = {
        '_id' : climate[0],
        'Station': climate[1],
        'Date': climate[2],
        'Air Temperature (Celcius)': float(climate[3]),
        'Relative Humidity': float(climate[4]),
        'WindSpeed  (knots)': float(climate[5]),
        'Max Wind Speed': float(climate[6]),
        'MAX': climate[7],
        'MIN': climate[8],
        'Precipitation': climate[9],
        'Fires': fires
        }
        myCol.insert_one(c)
        fires = []
        
db.climate.drop()
climateCol = db.climate
create_climate(climateCol)

# You can use this code to check the data input to the database
#results = climateCol.find()
#for d in results:
#    pprint(d)


# ### 4. Write a queries to answer the Tasks A2-A8 on teh new database. You need to write the queries as a python program using pymongo library in Jupyter Notebook. Choose one of it implement in parallel

# In[ ]:


# method to pprint the cursor
def _print(cursor):
    for document in cursor:
        pprint(document)


# ### A2

# In[ ]:


results = climateCol.find({'Date': '2017-12-15'},                          {'_id':0, 'Fires':0})#we don't need to display '_id' or 'Fires'
_print(results)


# ### A3

# In[ ]:


#Normal find
results = fireCol.find({'$and':[{'Surface Temperature (Celcius)': {'$lte': 100}},                                {'Surface Temperature (Celcius)': {'$gte': 65}}                               ]
                       },
                      {'Latitude':1, 'Longtitude':1, 'Confidence':1, '_id':0})
_print(results)


# ### A4

# In[ ]:


results = climateCol.aggregate([
{'$lookup':{
        'from': 'fire',
        'localField': '_id',
        'foreignField' : 'climate', # using '_id' to index will much quicker than 'Date', as mongodb will automatically allocate index for '_id'
        'as': 'fireDate'
         }
},
{'$unwind':"$fireDate"},
{'$match':{"Date":{"$in":["2017-12-15","2017-12-16"]}}},
{'$project':{"_id":0, "fireDate.Surface Temperature (Celcius)":1, "Air Temperature(Celcius)":1, "Relative Humidity":1, "Max Wind Speed":1}}
])

_print(results)


# ### A5

# In[ ]:


results = fireCol.aggregate([
{'$lookup':{
        'from': "climate",
        'localField': "climate",
        'foreignField' : "_id",# using '_id' to index will much quicker than 'Date', as mongodb will automatically allocate index for '_id'
        'as': "climateData"
         }
},
{'$unwind':"$climateData"},
{'$match':{'$and':[{"Confidence": {"$lte": 100}},{"Confidence": {"$gte": 65}}]}},
{'$project':{"_id":0, "Datetime":1,"climateData.Air Temperature (Celcius)":1, "Surface Temperature (Celcius)":1, "Confidence":1}}
])
_print(results)


# ### A6 

# In[ ]:


results = fireCol.find({},{'climate':0}).sort('Surface Temperature (Celcius)', pymongo.ASCENDING).limit(10)
_print(results)


# ### A7 ( With a parallel implementation)

# In[ ]:


# normal implement
results = fireCol.aggregate(
[
  {'$group':{'_id':"$Date", 'count':{'$sum':1}}},
  {'$sort': {'_id': 1}}
])
_print(results)


# In[ ]:


# parallel
def rr_partition(data, n): 
    #data: the list converted from the collection cursor
    #n: the number of parts to be partitioned
    result = []
    for i in range(n):
        result.append([]) # append n empty sublists

    n_bin = len(data)/n
    
    for index, element in enumerate(data): 
        index_bin = (int) (index % n)
        result[index_bin].append(element)
        
    return result # It will return a list, which contains n sublists.


def local_groupby(dataset):
    dict = {}
    for index, record in enumerate(dataset):
        key = record['Date']
        if len(record['Fires'])>0:
            dict[key] = len(record['Fires'])
    return dict


def parallel_groupby(dataset, n): # dataset: the list of all documents from the collection; n : partition to n parts
    result = {}
    
    dataset = rr_partition(dataset, n)
    n_processor = len(dataset)

    pool = mp.Pool(processes = n_processor)

    local_result = [] # the result of each sublist
    for s in dataset:
        local_result.append(pool.apply(local_groupby, [s]))
    pool.close()

    for r in local_result:
        for key, val in r.items():
            if key not in result:
                result[key] = 0
            result[key] += val    
    
    return result

results = climateCol.find()
climateList = list(results)
parallel_groupby(climateList,3)


# ### A8

# In[ ]:


results = fireCol.aggregate(
[
  {'$group':{'_id':"$Date", 'average':{'$avg':'$Surface Temperature (Celcius)'}}},
  {'$sort': {'_id': 1}}
])
_print(results)

