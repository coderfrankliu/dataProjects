
# coding: utf-8

# # FIT5196 Task 1 in Assessment 1
# #### Student Name: Jiahao Liu
# #### Student ID: 27549593
# 
# Date: 8 Apr 2018
# 
# Version: 2.0
# 
# Environment: Python 3.6.3.final.0 and 4.5.0

# ## 1.  Import libraries 

# In[1]:


import pandas as pd
#import re
#import numpy as np


# ## 2. Parse Excel File

# ### Step 1 Import Excel data into DataFrame

# In[2]:


# import the excel file 
excel_data = pd.ExcelFile('basic_indicators.xlsx') 
excel_data


# In[3]:


# in case that the excel file has mutiple sheets, so have a look to it
excel_data.sheet_names 


# In[4]:


# parse the excel sheet to dataframe
df = excel_data.parse('Basic Indicators') 

# has a look how many rows and columns of the sheet, obviously we should reshape the data
df.shape 


# ### Step 2 Drop useless columns and rows
# 
# - First, we will start with removing columns and rows which are all NaN.
# - Then, we will remove the header, which are incorrectly parsed as data, at the same time remove the rows that don't represent nation
# - Third, we will remove the additional columns, which are useless.
# - Finally, reindex the dataframe.

# In[5]:


# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

# have a look for the first 5 rows
df.head() 


# In[6]:


#have a look at the excel file, find that the last country should be Zimbabwe
df.loc[df['TABLE 1. BASIC INDICATORS'] == 'Zimbabwe'] 


# In[7]:


# have a look at the last row of the dataframe 
# Also can use df.tail(1).index() to get it
df.tail(1)


#  As we check the excel file find that the last country is 'Zimbabwe' and the index of it is 205, and the last row index is 244, so we will drop rows between them

# In[8]:


# drop all the rows after 'Zimbabwe'
df.drop(df.index[205:244],inplace =True) 

# drop the first three rows, which are header
df.drop(df.index[0:3],inplace =True) 

# drop three useless columns
df.drop(['Unnamed: 15','Unnamed: 17','Unnamed: 23'], axis = 1, inplace = True) 

#have a look for the first five rows
df.head()


# In[9]:


'''
check the shape of the dataframe and it satisfy the requirement of 
the task(additional one is the columns of country name)
'''
df.shape 


# ### Step 3 Set Country Index and Columns Names

# In[10]:



# Set the country names as row indices
df = df.set_index(keys= df['TABLE 1. BASIC INDICATORS'].values)

# Delete "TABLE 1. BASIC INDICATORS" column, it is now redundant.
df = df.drop('TABLE 1. BASIC INDICATORS', 1)

# Set the name of the index
df.index.set_names('Country Name',inplace = True)

# Reindex columns
df.columns = list(range(len(df.columns))) 

#have a look for the first five rows
df.head()


# ### Step 4 Tidy up all columns

# In[11]:


# change the datatype from object to number, those which can't be transfer to number will be assgined as NaNs
df = df.apply(pd.to_numeric, errors = 'coerce')

# make all numbers to integers
df = df.applymap('{:.0f}'.format)

# replace all nan with ''
df = df.replace('nan', '', regex = True)

# have a look for the first five rows
df.head()


# ### Step 5 Save the dataframe as CSV file

# In[12]:


df.to_csv('./basic_indicators.csv')


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
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.to_csv. Retrieved from http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.dropna. Retrieved from https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html
# 
# - Mooncrater (Dec 29 2017). *Pandas: convert dtype 'object' to int* [Response to]. Retrieved from https://stackoverflow.com/questions/39173813/pandas-convert-dtype-object-to-int
