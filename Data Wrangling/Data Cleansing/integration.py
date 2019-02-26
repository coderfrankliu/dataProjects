
# coding: utf-8

# # FIT5145 Task 2 Integrating two Datasets
# #### Student Name: Jiahao Liu
# #### Student ID: 27549593
# 
# Date: 2 May 2018
# 
# Version: 1.0
# 
# Environment: Python 3.6.3.final.0 and 4.5.0

# ## 1.  Import libraries 

# In[1]:


import pandas as pd
import re
import math


# ## 2. Load the data using Pandas library 

# In[2]:


# import the  file 
df1 = pd.read_csv('dataset1_solution.csv')
df2 = pd.read_csv('dataset2_integration.csv')


# In[3]:


# has a look how many rows and columns of the sheet, obviously we should reshape the data
df1 = df1.drop('Unnamed: 0',1)
print(df1.shape)


# In[4]:


df2.head()


# In[5]:


df2.location.value_counts()
df2.shape


# ## 3 . Adapt the Data

# ### 3.1 Id

# In[6]:


# check if the Ids are all unique
df2.Id.is_unique


# ### 3.2 Title

# In[7]:


#df.Title.value_counts


# ### 3.3 Location

# In[8]:


#df.Location.value_counts()


# ### 3.4 ContractType

# In[9]:


df2['Contract Type'].value_counts()


# In[10]:


df2['Contract Type'] = df2['Contract Type'].replace({'ft' : 'full_time', 'pt' : 'part_time', 'n/a' : 'non_specified'})
df2['Contract Type'].value_counts()


# ### 3.5 ContractTime

# In[11]:


df2['Contract Time'].value_counts()


# In[12]:


df2['Contract Time'] = df2['Contract Time'].replace({'perm.' : 'permanent', 'n/a' : 'non_specified', 'contr.':'contract'})
df2['Contract Time'].value_counts()


# In[13]:


pd.crosstab(df2['Contract Type'], df2['Contract Time'])


# ### 3.7 Category

# In[14]:


#check if the categories are consistent
df2.Category.value_counts()


# In[15]:


df2['Category'] = df2['Category'].replace({'Finance & Accounting Jobs' : 'Accouting & Finance Jobs'})
df2.Category.value_counts()


# ### 3.8 Salary per annum

# In[16]:


df2['Salary per month'].head()


# In[17]:


df2['Salary per month'] = df2['Salary per month'].apply(lambda x : x*12)


# ### 3.11 OpenDate and CloseDate

# In[18]:


df2.OpenDate=pd.to_datetime(df2.OpenDate)
df2.CloseDate=pd.to_datetime(df2.CloseDate)

df2.OpenDate = df2.OpenDate.apply(lambda x : x.strftime('%Y%m%dT%H%M%S'))
df2.CloseDate = df2.CloseDate.apply(lambda x : x.strftime('%Y%m%dT%H%M%S'))


# In[19]:


df1.columns


# In[20]:


df2.columns = df1.columns


# ### 4. Merge two dataset

# In[21]:


df = pd.concat([df1,df2], axis=0)


# In[22]:


df.head()


# In[23]:


df.Id.is_unique


# In[24]:


df.drop_duplicates(['Location', 'ContractType', 'ContractTime','Salary per annum','Company','Category'], keep='first', inplace = True)


# After concating two dataframes, there are lots of duplicated 'job advertisement':
# I would like to use "Company","Location","ContractType","ContractTime","Salary per annum","Category" to be the global key
# My reasons for didn't pick those column were:
# 
# 1. Id in this dataframe is unique so we can't use it.
# 2. Title is varied and not claen enough to be the criteria of duplication
# 3. Different company can post their advertisements on different websites
# 4. OpenDate and CloseDate were varied from different websites.
# 
# My reasons for picked up those columns were:
# 
# 1. A job have to be in the same location, even from different source or different time.
# 2. The contract type and time for one job should be consistent
# 3. The categories were greatly different from each other.
# 4. Salary should be the same for one job
# 5. Same job should be released by one company

# ### 6 Save the dataframe as CSV file

# In[25]:


df.to_csv('./dataset1_dataset2_solution.csv')


# ## 3. Summary
# This assessment measured the understanding of Excel file and how to extract data from it. The main outcomes achieved while applying these techniques were:
# 
# - 1.**Read data from excel**. By using the `pandas` package, we can parsing the data from excel to Dataframe, which makes the process more handy.
# 
# - 2.**Data frame manipulation**. By using the `pandas` package, adding, deleting, searching, editing data can be easily done in dataframe. Additional operations like filtering, slicing, makes the data management much easier.
# 
# - 3.**Exporting data to specific format**. By using built-in functions like `DataFrame.to_csv()` it was possible to export data frames into `.txt` files without additional formatting and transformations. 

# ## 4. References
# - sheinis (Aug 24 2016). *Read Excel File in Python* [Response to]. Retrieved from https://stackoverflow.com/questions/22169325/read-excel-file-in-python
# 
# - Mooncrater (Dec 29 2017). *Pandas: convert dtype 'object' to int* [Response to]. Retrieved from https://stackoverflow.com/questions/39173813/pandas-convert-dtype-object-to-int
# 
# https://stackoverflow.com/questions/17097643/search-for-does-not-contain-on-a-dataframe-in-pandas
# 
# https://stackoverflow.com/questions/15325182/how-to-filter-rows-in-pandas-by-regex
