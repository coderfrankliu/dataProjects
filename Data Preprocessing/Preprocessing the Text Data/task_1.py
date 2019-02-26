
# coding: utf-8

# # FIT5196 Assessment 3
# # Task 1 Reconstruct the Original Meeting Transcripts
# #### Student Name: Jiahao Liu
# #### Student ID: 27549593
# 
# Date: 01/Jun/2018
# 
# Version: 3.0
# 
# Environment: Python 3.6.3.final.0 and Anaconda 4.5.0 (64-bit)
# 
# Libraries used:
# * xml.etree.ElementTree (for parsing XML doc, included in Anaconda Python 3.6)
# * re 2.2.1 (for regular expression, included in Anaconda Python 3.6) 
# * os (for reading and writing files, included in Anaconda Python 3.6)
# 
# 
# ## Introduction
# The original meeting transcripts are stored in three different types of XML files, which are ending with ".words.xml", ".topic.xml" and ".segments.xml". The task here is to reconstruct the original meeting transcripts with the corresponding topical and paragraph boundaries from these files. What we going to do is generating a folder of txt files, meet the requirements that:
# 
# 1. A meeting transcript must be generated for each of the "*.topic.xml" file. For example, "**ES2002a**.txt" will be generated for "**ES2002a**.topic.xml".
# 2. All the generated meeting transcripts with the ".txt" file extension must be saved in the folder "txt_files".
# 3. The topical boundaries must be denoted with 10 asterisks.
# 4. All the tokens, including punctuations, must be separated by a white space. For example, "Alright , okay . Okay ."
# 5. The input files to your notebook "task_1.ipynb" must be the three types of XML files. The output must be the meeting transcripts saved in a set of txt files.

# In[ ]:


import xml.etree.ElementTree as ET
import os
import re


# In[ ]:


# get the current working directory
# 1. eaiser to coding 
# 2. improve the performance of reading adn writing
cd=os.getcwd()


# In[ ]:


#As we open a file, generate a dictionary
#set the index as the key, the word as the value
def buildWordDic(path):
    with open(path, 'r') as file:
        data = file.read()
    root = ET.fromstring(data)
    wordXml=dict()
    for elem in root.iter():
        if ("type" not in elem.attrib) and "starttime" in elem.attrib and elem.tag=="w":
            wordXml[int(elem.attrib["{http://nite.sourceforge.net/}id"].split("words")[1])]=elem.text
    file.close()
    return wordXml


# In[ ]:


def buildTopicTxt(path):
    with open(path, 'r') as file:
        data = file.read()
    root = ET.fromstring(data)
    txtString=[]
    wordDics=dict()
    file_head=path.split("/")[-1].replace(".topic.xml","")
    segmentDics=buildSegmentDics(file_head)
    for elem in root.findall("topic"):
        txtString.append("**********")
        for e in elem.iter():
            if e.tag=="{http://nite.sourceforge.net/}child":
                file_name,index=divideChild(e.attrib["href"])
                file_name_head=file_name.replace(".words.xml","") 
                #if we have opened the word file, we don't need to open again
                if file_name_head not in wordDics:
                    wordDics[file_name_head]=buildWordDic(cd + "/words/" + file_name)
                txtString.append(buildTopic(index,wordDics[file_name_head],segmentDics[file_name_head]))
            txtString=[text for text in txtString if text!=""]
            txtString=[text for text in txtString if text!=" "]
            # make sure there is no whitespaces 
            # make sure that the output is strictly follow the example
            while "" in txtString:
                txtString.remove("")
            while " " in txtString:
                txtString.remove(" ")
            while "  " in txtString:
                txtString.remove("  ")
            # make sure there are no multiple \n when we append txtString
            txtString=[txt.replace("\n \n","\n") for txt in txtString]
            while " \n \n" in txtString:
                txtString.remove(" \n \n")
            while " \n" in txtString:
                txtString.remove(" \n")
            StringToWrite = ("\n").join(txtString)
            file.close()             
            #To finnally make sure follow the example output
            #clean all of the String just in case 
            #also, there is a new line at the last line of 10 asterisks
    return (StringToWrite.replace("\n \n","\n").replace("\n\n","\n")+"**********").            replace("**********\n**********","**********")[11:] + "\n"


# In[ ]:


def buildTopic(index,wordDic,segmentDic):
    start=index[0]
    end=index[1]
    segments=[]
    segmentKeyList=list(segmentDic.keys())
    #some subtopic contain several segments
    if start in segmentKeyList:
        startInDict=segmentKeyList.index(start)
        for i in range(startInDict,list(segmentDic.keys())[-1]):
            if i in segmentDic:
                if segmentDic[i]<=end:
                    segments.append(i)
    topicList=[]
    for i in range(start,end+1):        
        if i in wordDic and isinstance("",str) and wordDic[i]!="":
            # if i is a str and not a null string
            topicList.append(wordDic[i])
        if i in segmentDic.values():
            topicList.append("\n")
    if len(topicList)==1:
        # strictly follow the output example. 
        # there is a whitespace in front of each line except the line with ten asterisks
        if topicList[0]!="":
            topicString=" "+topicList[0]
        else:
            topicString=topicList[0]
    else:
        # also find some lines maybe have too much whitespace
        while "" in topicList:
            topicList.remove("")
        while " " in topicList:
            topicList.remove(" ")
        while "  " in topicList:
            topicList.remove("  ")
        while " \n" in topicList:
            topicList.remove(" \n")
        topicList.insert(0,"")
        topicList=[topic.replace("\n \n","\n") for topic in topicList]
        topicList=[topic.replace("\n\n","\n") for topic in topicList]
        topicString=" ".join(topicList)
    return topicString


# In[ ]:


def buildSegmentDics(file_start):
    segmentDics=dict()
    for path,dir_list,file_list in os.walk(cd+"/segments"):
        for file_name in file_list:
            if file_name.startswith(file_start):
                segmentDics[file_name.replace(".segments.xml","")]=buildSegmentDic(cd+"/segments/"+file_name)
    return segmentDics


# In[ ]:


def buildSegmentDic(path):
    with open(path, 'r') as file:
        data = file.read()
    root = ET.fromstring(data)
    segmentDic=dict()
    for elem in root.iter():
        if elem.tag=="{http://nite.sourceforge.net/}child":
            # the key is the start of the list 
            # value is the end of the list
            item = divideChild(elem.attrib["href"])[1]
            if len(item)==1:
                segmentDic[item[0]]=item[0]
            else:
                segmentDic[item[0]]=item[1]
    file.close()
    return segmentDic


# In[ ]:


def divideChild(child):
    info=child.split("#id(")
    file_name=info[0]
    index=info[1].split("..id(")    
    index=[int(a.replace(")","").split("words")[-1]) for a in index]
    # in case of index error, easier to manipulate
    if len(index)==1:
        index=index*2
    return file_name,index


# In[ ]:


for path,dir_list,file_list in os.walk(cd + "/topics"):
    for file_name in file_list:
        file_name_write=file_name.replace("topic.xml","txt")
        read_path="/".join([cd + "/topics",file_name])
        stringToWrite=(buildTopicTxt(read_path))
        write_path="/".join([cd + "/txt_files",file_name_write])
        with open(write_path, 'w') as file:
            file.write(stringToWrite)
        file.close()


# ## Unit test

# In[ ]:


cd = os.getcwd()


# In[ ]:


wd = buildWordDic(cd + "/words/ES2002a.B.words.xml")


# In[ ]:


sd = buildSegmentDic(cd + "/segments/ES2002a.B.segments.xml")


# In[ ]:


sd.values()


# In[ ]:


s = buildTopicTxt(cd + "/topics/ES2010b.topic.xml")


# In[ ]:


s

