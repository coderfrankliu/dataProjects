// Task1 Import the dataset in terminal
// mongoimport --db fit5148_db --collection climate --type csv --headerline --ignoreBlanks --file /Users/frank/Documents/ClimateData-Part1.csv
// mongoimport --db fit5148_db --collection fire --type csv --headerline --ignoreBlanks --file /Users/frank/Documents/FireData-Part1.csv

use fit5148_db

// Task2
db.climate.find({"Date": "2017-12-15"})

// Task3
db.fire.find({$and:[{"Surface Temperature (Celcius)": {"$lte": 100}},
                    {"Surface Temperature (Celcius)": {"$gte": 65}}
                   ]
             },{"_id":0, "Latitude":1, "Longitude":1, "Confidence":1})

// Task4
db.climate.aggregate([
{$lookup:{
        from: "fire",
        localField: "Date",
        foreignField : "Date",
        as: "fireDate"
         }
},
{$unwind:"$fireDate"},
{$match:{"Date":{"$in":["2017-12-15","2017-12-16"]}}},
{$project:{"_id":0, "fireDate.Surface Temperature (Celcius)":1, "Air Temperature(Celcius)":1, "Relative Humidity":1, "Max Wind Speed":1}}
])

// Task5
db.climate.aggregate([
{$lookup:{
        from: "fire",
        localField: "Date",
        foreignField : "Date",
        as: "fireDate"
         }
},
{$unwind:"$fireDate"},
{$match:{$and:[{"fireDate.Confidence": {"$lte": 100}},{"fireDate.Confidence": {"$gte": 65}}]}},
{$project:{"_id":0, "fireDate.Datetime":1,"Air Temperature(Celcius)":1, "fireDate.Surface Temperature (Celcius)":1, "fireDate.Confidence":1}}
])


// Task6 top10 records of highest surface temperature
db.fire.find().sort({'Surface Temperature (Celcius)': -1}).limit(10)

// Task7 number of fire for each day
db.fire.aggregate(
[
  {$group:{_id:"$Date", fires:{$sum:1}}}
 
]
)

// Task8 average surface temperature fro each day
db.fire.aggregate(
[
  {$group:{_id:"$Date", average:{$avg:"$Surface Temperature (Celcius)"}}},
  {$sort: {average: -1}}
]
)
