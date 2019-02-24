
# coding: utf-8

# # FIT5196 Task 3 in Assessment 1
# #### Student Name: Jiahao Liu
# #### Student ID: 27549593
# 
# Date: 5/April/2018
# 
# Version: 1.0
# 
# Environment: Python 3.6.3.final.0 and 4.5.0
# 
# Libraries used: 
# * re (for regular expression, included in Anaconda Python 3.6) 
# * json (for json file, included in Anaconda Python 3.6) 
#  
# # Introduction
# Convert Data Stored in an XML File to a JSON File. This task focuses on converting the Austrailian Sport Thesaurus stored in an XML file ("**australian-sport-thesaurus-student.xml**") into a JSON file. The following figure shows what the JSON file should look like.
# In order to finish this task, 
# - you must correctly extract the thesaurus in the XML file and store it in the JSON file;
# - while extracting the thesaurus from the XML file, existing Python Packages that are written to parse XML files (e.g.,  Beautiful-soup, lxml and ElementTree) must not be used. You must write your own Python script to extract the thesaurus. **Hint**: Regular Expressions can be used.
# - Python packages, like json, can be used to save the extracted thesaurus;
# - your script must be written in a Jupyter notebook named as "**xml_json.ipynb**";
# - the JSON data should be saved in a file named as "**sport.dat**";
# - the input file must only be "**australian-sport-thesaurus-student.xml**".

# ## 1.  Import libraries 

# In[3]:


import re
import json


# ## 2. Parse XML File to a JSON File

# ### Step 1  Read the xml file

# In[4]:


#open the xml file
file = open("australian-sport-thesaurus-student.xml", "r", encoding="utf-8")

#read the xml as a string
fileString=file.read()

#close after reading
file.close()


# ### Step 2 Tidy up the data as a list of string

# In[5]:


#split the string to a list of short strings, split when it comes to a new line
k = fileString.split("\n")
k


# In[6]:


#clean the space of each string 
k = [s.strip() for s in k]
k


# In[7]:


#in case that there has blank line(there has '' in the list of string), which should be removed
while "" in k:
    k.remove("")


# In[8]:


'''
If there is a string that does't start with a <, means that it 
should be concatenate with its previous line, which has tag
'''
for i in range(len(k)):
    # -2 is because we will +1 afterward
    if i <= len(k) - 2:
        if k[i+1].startswith("<") == False:
            k[i] = k[i] + k[i+1]
            k[i+1] = ""

while "" in k:
    k.remove("")


# In[9]:


# The first line is useless data, remove it
k = k[1:]


# In[10]:


# this function can transfer list of string to json style
def lstToJson(l):
    #The total String is start with"{" and ends with"}"
    jsonString="{"
    #used to check process
    stack=[]
    '''
    There are three patterns
    1. just the open tag, like <Title>
    2. has open tag, data and close tag, like <Title>Rugby League terms and techniques</Title>
    3. just the close tag </Title>
    '''
    pattern1 = re.compile(r'<.*?>')
    pattern2 = re.compile(r'<.*?>(.*)</.*?>')
    pattern3 = re.compile(r'(.*)</.*?>')
    
    currentPosition=0
    for i in l:
        if pattern2.match(i):
            
            #extract the open tag
            matchObj=pattern1.match(i)
            if matchObj:
                
                #used to check the process
                lab=re.sub(r'<.*?>',"",i)
                
                #transfer the xml tag to a json tag
                lebal=matchObj.group().replace("<","").replace(">","")
                
                #append json tag tojsonString, there has some untidy data like "", tab, '-', should be replaced
                toAppend="\"" +lebal+"\":"+"\""+lab.replace("\"","\'").replace("\t","").replace("\u2022","")+"\""
                jsonString += toAppend
                
                if currentPosition<=len(l)-2:
                    #If the position is not the end of a term, append ","
                    if l[currentPosition+1] not in ["</Terms>","</Term>","</RelatedTerms>"]:
                        jsonString += ","
                    else:
                        #if it comes to end, append final close tag "}"
                        jsonString += "}"
                        
        elif pattern3.match(i):
            stack = stack[0:len(stack)-1]
            matchObj = pattern3.match(i)
            
            #if it is the end of a relatedterms, append with "]}"
            if matchObj.group() == "</RelatedTerms>":
                jsonString+="]}"
                if currentPosition<=len(l)-2:
                    if l[currentPosition+1] not in ["</Terms>","</Term>"]:
                        jsonString+=","
            if matchObj.group()=="</Terms>":
                jsonString+="]}"
                return jsonString
            if currentPosition<=len(l)-2:
                if l[currentPosition+1] not in ["</Terms>","</Term>","</RelatedTerms>"]:
                    jsonString+=","
                    
        elif pattern1.match(i):
            matchObj=pattern1.match(i)
            
            #get the data from the tag
            lebal=matchObj.group().replace("<","").replace(">","")
            stack.append(lebal)
            if lebal=="Terms" or lebal=="RelatedTerms":
                if lebal=="Terms":
                    lebal="thesaurus"
                    # append "lebal":[
                jsonString=jsonString+"\""+lebal+"\""+":["
            elif lebal=="Term":
                jsonString+="{"
            else:
                jsonString+=lebal+":"
        currentPosition+=1
    return jsonString


# ### Step 3 Tranfer the list of string into a long JSON style string

# In[11]:


# s is the long string of json file
s=lstToJson(k)


# ### Step 4 Save the String as dat file

# In[12]:


file = open("sport.dat","w", encoding="utf-16") 
file.write(s)
file.close()


# In[13]:


# check the result
g=json.loads(s)
g


# In[14]:


type(g)


# ## 3. Summary
# This assessment measured the understanding of XML and JSON file and how to transfer a file from XML to JSON. The main outcomes achieved while applying these techniques were:
# 
# - 1.**Read data from xml**. We read the xml data as a long string and split it into multiple short string and operate on them.
# 
# - 2.**transfer data**. As we read in all the data, applying regular expression to operate on different pattern of data

# ## 4. References
# - The re Project. (2016a). regular expression documentation: Retrieved from https://docs.python.org/3.6/library/re.html
# 
# - aaa90210 (Apr 26 2017). *Python re.sub(): how to substitute all 'u' or 'U's with 'you' * [Response to]. Retrieved from https://stackoverflow.com/questions/13748674/python-re-sub-how-to-substitute-all-u-or-us-with-you
