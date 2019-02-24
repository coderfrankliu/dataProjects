
# coding: utf-8

# # FIT5196 Assessment 3
# # Task 2 Generate Sparse Representations 
# #### Student Name: Jiahao Liu
# #### Student ID: 27549593
# 
# Date: 03/Jun/2018
# 
# Version: 3.0
# 
# Environment: Python 3.6.3.final.0 and Anaconda 4.5.0 (64-bit)
# 
# Libraries used:
# * nltk 3.2.2 (Natural Language Toolkit, included in Anaconda Python 3.6)
# * re 2.2.1 (for regular expression, included in Anaconda Python 3.6) 
# * os (for reading and writing files, included in Anaconda Python 3.6)
# * nltk.tokenize (for tokenization, included in Anaconda Python 3.6)
# * FreqDist （For counting the frequency, included in Anaconda Python 3.6)
# * CountVectorizer(Convert a collection of text documents to a matrix of token counts)
# 
# 
# ## Introduction
# The aim of this task is to build sparse representations for the meeting transcripts generated in task 1, which includes word tokenization, vocabulary generation, and the generation of sparse representations.
# 
# 1. The word tokenization must use the following regular expression, "\w+(?:[-']\w+)?", and all the words must be converted into the lower case.
# 2. The words, whose document frequencies are greater than 132, must be removed.
# 3. The stop words list (i.e, stopwords_en.txt) provided in the zip file must be used.
# 4. The output of this task must contain the following files: **vocab.txt, topic_seg.txt, ./sparse_files/*.txt**

# In[1]:


import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist
import os
import re
from sklearn.feature_extraction.text import CountVectorizer


# In[2]:


# get the current working directory
# 1. eaiser to coding 
# 2. improve the performance of reading adn writing
cd=os.getcwd()


# In[3]:


# get the tokenizer and stop words 
tokenizer = RegexpTokenizer("\w+(?:[-']\w+)?") 
with open(cd + "/stopwords_en.txt", 'r') as file:
    stopwords = file.read().split("\n")
file.close()


# In[4]:


# Code to generated the sparse count vectors
def word_concat(dsd):
    """
    concatenate all the words stored in the values of a given dictionary. Each value is a list
    of tokenized sentences.
    """
    all_words = []
    for value in dsd.values():
        all_words += value
    print("tokens:", len(all_words))
    print ("types:", len(set(all_words)))
    return all_words


# In[5]:


def buildTopic_seg(data):
    topic_seg=[]
    paragraphs=data.split("\n")
    for p in paragraphs:
        if p!="**********":
            topic_seg.append(0)
        else:
            topic_seg[-1]=1
    topic_seg = topic_seg[:-1]
    return topic_seg


# In[6]:


def writeSparse_file(data,file_name):
    with open(cd + "/sparse_files/" + file_name, 'w') as file:
        paragraphs=data.split("\n")
        for p in paragraphs:
            words=tokenizer.tokenize(p.lower())
            words=[word for word in words if ((word not in stopwords) and (word not in frequence_word) and (len(word)>=3)and word!="**********")]
            # when the paragraph is not empty
            if len(words)!=0:
                freq_dist1=FreqDist(words)
                tokenizer.tokenize(data.lower())
                toWrite=""
                for item in freq_dist1.items():
                    # the data format in freq_dist1 is {word: frequency}
                    # the data format in word_dist is {word: index}
                    toWrite+=(str(word_dict[item[0]])+":"+str(item[1])+",")
                toWrite=toWrite[:-1]+"\n"
                file.write(toWrite)
        file.close()


# In[7]:


unigram_tokens_dic={}
topic_segs={}
for path,dir_list,file_list in os.walk(cd+"/txt_files"):
    for file_name in file_list:
        if file_name.endswith("txt"):
            read_path="/".join([cd+"/txt_files",file_name])
            with open(read_path, 'r') as file:
                data = file.read()
            unigram_tokens = tokenizer.tokenize(data.lower())
            # dictionary of list which key == filename, value == list of words
            unigram_tokens_dic[file_name]=unigram_tokens
            topic_seg=buildTopic_seg(data)
            # if we directly string a list, there will be '[' ']' at the beginning and end need to be sliced
            # also slice .txt 
            topic_segs[file_name[:-4]]=str(topic_seg)[1:-1]
            file.close()


# In[8]:


with open(cd+"/topic_segs.txt", 'w') as file:
    for item in topic_segs.items():
        file.write(item[0]+":"+item[1]+"\n")
    file.close()


# In[9]:


freq_dist = FreqDist(word_concat(unigram_tokens_dic))
frequence_word=[]
for item in freq_dist.items():
    if item[1]>132:
        frequence_word.append(item[0]) 


# In[10]:


#get rid of all words in the list stopwords and frequently appeared words
words = [word for word in freq_dist.keys() if ((word not in stopwords) and (word not in frequence_word))]
#Forum said we need to filter out the words which lens less than 3
words = [word for word in words if (len(word) >= 3)]
# default sort is based on alphabat
words.sort()
word_dict=dict()
with open(cd + "/vocab.txt", 'w') as file:
    for word in words:
            word_dict[word]=words.index(word)
            file.write(word+":"+str(words.index(word))+"\n")
file.close()


# In[ ]:


len(words)


# In[ ]:


for path,dir_list,file_list in os.walk(cd +"/txt_files"):
    for file_name in file_list:
        if file_name.endswith("txt"):
            read_path="/".join([cd+"/txt_files",file_name])
            with open(read_path, 'r') as file:
                data = file.read()
            writeSparse_file(data,file_name)

