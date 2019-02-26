
# coding: utf-8

# In[ ]:


import socket
from time import sleep
import sys
import datetime


# In[ ]:


fileclimate = open("./ClimateData-Part2.csv", "r", encoding="utf-8")
filefire = open("./FireData-Part2.csv", "r", encoding="utf-8")

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


# we stored one climate followed by 5 firedata in a list, and treated them as a line
j = 0
combined = []
for i in range(len(climateData)):
    climateData[i].extend(fireData[j])
    climateData[i].extend(fireData[j+1])
    climateData[i].extend(fireData[j+2])
    climateData[i].extend(fireData[j+3])
    climateData[i].extend(fireData[j+4])
    climateData[i].extend('`') # to identify data interval
    combined.append(climateData[i])
    j+5


# In[ ]:


stream=[]
for record in combined:
     stream.append(','.join(record))


# In[ ]:


stream[0]


# In[ ]:


datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# In[ ]:


host = 'localhost'
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
while True:
    print('\nListening for a client at', host, port)   
    conn, addr = s.accept()
    print('\nConnected by', addr)
    try:
        print('\nReading file...\n')
        for record in stream:
            out = record.encode('utf-8')
            interval = ('\n').encode('utf-8')
            print('Sending line',record)
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            time = time.encode('utf-8')
            conn.send(time)
            conn.send(out)  
            conn.send(interval)
            sleep(1)
        print('End Of Stream.')
        break
    except socket.error:
        print ('Error Occured.\n\nClient disconnected.\n')
conn.close()

