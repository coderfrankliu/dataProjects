
# coding: utf-8

# In[ ]:


import socket
from time import sleep
import sys

from pyspark import SparkContext # spark
from pyspark.streaming import StreamingContext # spark streaming

import pymongo
from pymongo import MongoClient


# In[ ]:


# Create a local StreamingContext with as many working processors as possible and a batch interval of 10 seconds            
batch_interval = 5

# local[*]: run Spark locally with as many working processors as logical cores on your machine.
sc = SparkContext(master="local[2]", appName = "Climate&Fires") 

# a batch interval of 5 seconds   
ssc = StreamingContext(sc, batch_interval)


# In[ ]:


# We add this line to avoid an error : "Cannot run multiple SparkContexts at once". If there is an existing spark context, we will reuse it instead of creating a new context.
sc = SparkContext.getOrCreate()

# If there is no existing spark context, we now create a new context
if (sc is None):
    sc = SparkContext(appName="Climate&Fires")
ssc = StreamingContext(sc, batch_interval)


# In[ ]:


cn = 0
fn = 0
#each record contains 1 time, 1 climate data, 5 fires.
def addRecord(records):
    
    #used to make incement id
    global cn
    global fn
    
    # split the record, to date and other data
    date_other = record.split('cdata,')
    date = date_other[0]
    
    #split climate data and fires' data
    climate_fires = date_other[1]
    climate_fires = climate_fires.split('fdata,')
    
    #get the climate data
    clist = climate_fires[0]
    clist = clist.split(',')
    Station = clist[0]
    Air_Temperature_Celcius = clist[1]
    Relative_humidity = clist[2]
    WindSpeed = clist[3]
    Max_Wind = clist[4]
    Max = clist[5]
    Min = clist[6]
    Precipitation = clist[7]
    cid = 'c' + str(cn)
    cn = cn+1
    
    #get five fire data
    flist = climate_fires[1:]
    f0 = flist[0].split(',')
    Lat0 = f0[0]
    Long0 = f0[1]
    SurfaceK0 = f0[2]
    Power0 = f0[3]
    Confidence0 = f0[4]
    SurfaceC0 = f0[5]
    fid0 = 'f' + str(fn)
    fn = fn+1
    
    f1 = flist[0].split(',')
    Lat1 = f1[0]
    Long1 = f1[1]
    SurfaceK1 = f1[2]
    Power1 = f1[3]
    Confidence1 = f1[4]
    SurfaceC1 = f1[5]
    fid1 = 'f' + str(fn)
    fn = fn+1
    
    f2 = flist[0].split(',')
    Lat2 = f2[0]
    Long2 = f2[1]
    SurfaceK2 = f2[2]
    Power2 = f2[3]
    Confidence2 = f2[4]
    SurfaceC2 = f2[5]
    fid2 = 'f' + str(fn)
    fn = fn+1
    
    f3 = flist[0].split(',')
    Lat3 = f3[0]
    Long3 = f3[1]
    SurfaceK3 = f3[2]
    Power3 = f3[3]
    Confidence3 = f3[4]
    SurfaceC3 = f3[5]
    fid3 = 'f' + str(fn)
    fn = fn+1
    
    f4 = flist[0].split(',')
    Lat4 = f4[0]
    Long4 = f4[1]
    SurfaceK4 = f4[2]
    Power4 = f4[3]
    Confidence4 = f4[4]
    SurfaceC4 = f4[5]
    fid4 = 'f' + str(fn)
    fn = fn+1

    # build mongodb model followed by what we did in TaskB
    client =MongoClient()
    db = client.fit5148
    db = db.climate
    db.insert_one({'_id': cid, 'Station': Station, 'Date': date,              'Air Temperature(Celcius)': Air_Temperature_Celcius,              'Relative Humidity':Relative_humidity, 'WindSpeed  (knots)':WindSpeed,              'MAX':Max, 'MIN':Min, 'Max Wind Speed':Max_Wind,              'Precipitation':Precipitation,              'Fires':[{'_id':fid0},{'_id':fid1},{'_id':fid2},{'_id':fid3},{'_id':fid4}]})
    
    db = client.fit5148
    db = db.fires
    db.insert_one({'_id':fid0,'Confidence':Confidence0,'Date': date,              'Datetime': date,'Latitude':Lat0,              'Longtitude':Long0,'Power':Power0,              'Surface Temperature (Celcius)':SurfaceC0,              'Surface Temperature (kelvin)':SurfaceK0,'climate': cid})
    
    db.insert_one({'_id':fid1,'Confidence':Confidence1,'Date': date,              'Datetime': date,'Latitude':Lat1,              'Longtitude':Long1,'Power':Power1,              'Surface Temperature (Celcius)':SurfaceC1,              'Surface Temperature (kelvin)':SurfaceK1,'climate': cid})
    
    db.insert_one({'_id':fid2,'Confidence':Confidence2,'Date': date,              'Datetime': date,'Latitude':Lat2,              'Longtitude':Long2,'Power':Power2,              'Surface Temperature (Celcius)':SurfaceC2,              'Surface Temperature (kelvin)':SurfaceK2,'climate': cid})
    
    db.insert_one({'_id':fid3,'Confidence':Confidence3},{'Date': date,              'Datetime': date,'Latitude':Lat3,              'Longtitude':Long3,'Power':Power3,              'Surface Temperature (Celcius)':SurfaceC3,              'Surface Temperature (kelvin)':SurfaceK3,'climate': cid})
    
    db.insert_one({'_id':fid4,'Confidence':Confidence4,'Date': date,              'Datetime': date,'Latitude':Lat4,              'Longtitude':Long4,'Power':Power4,              'Surface Temperature (Celcius)':SurfaceC4,              'Surface Temperature (kelvin)':SurfaceK4,'climate': cid})
    client.close()


# In[ ]:


# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)

# Split each record by the interval made before
line = lines.flatMap(lambda line: line.split("`"))

line.foreachRDD(lambda rdd: rdd.foreach(addRecord))

line.pprint()
ssc.start()             # Start the computation
ssc.awaitTermination()

