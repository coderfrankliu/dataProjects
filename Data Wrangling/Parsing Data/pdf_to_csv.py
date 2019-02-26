
# coding: utf-8

# # FIT5196 Task 2 in Assessment 1
# #### Student Name: Jiahao Liu
# #### Student ID: 27549593
# 
# Date: 1/Apr/2018
# 
# Version: 2.0
# 
# Environment: Python 3.6.3.final.0 and 4.5.0
# 
# Libraries used: 
# * pandas (for dataframe, included in Anaconda Python 3.6) 
# * re (for regular expression, included in Anaconda Python 3.6) 
# * numpy (for numpy array, included in Anaconda Python 3.6) 
# 
# # Introduction
# Extract Data from a PDF File. The PDF file, "health.pdf", contains the children's health data over 202 countries in the world. The table spreads over four pages. The task is to extract the table and save them in a CSV file as
# where the first column contains the country names, and the following 22 columns contain various health information. In order to finish this task,
# 
# - you must correctly parse and extract the table;
# - existing Python packages (like: pdfminer or pdftables) can be used, however, APIs (like pdftables_api), which requires API keys to push the PDF file to the server in order to get the file parsed, must not be used;
# - it is **not required** to extract the column labels. Except for the first column, which should be named as "Country Name", the other columns should be indexed with integers as shown in the figure;
# - if the number followed by a character "x" in the pdf file,  "x" must be dropped in your script;
# - your script must be written in a Jupyter notebook named as "**pdf.ipynb**";
# - and the extracted table should be saved in a CSV file named as "**health.csv**";
# - the input file must only be "**health.pdf**".

# ## 1.  Import libraries 

# In[ ]:


get_ipython().system('pip install tabula-py # install the tabula-py as the first time run tablua-py')


# In[ ]:


from tabula import read_pdf
import pandas as pd
import re


# ## 2. Parse PDF File

# ### Step 1 Import pdf data into DataFrame

# In[ ]:


'''
As there are four pages in the  pdf file, we seperate it into two parts
1. The first three pages, d1, which are full of table
2. The fourth page, d2, which is partly table
'''
df1 = read_pdf("health.pdf",pages = '1-3', multiple_tables = False)
print(df1.shape)


# In[ ]:


# area, the area of the page of the pdf, which can be found at the gernal info of the file
df2 = read_pdf("health.pdf",pages = '4', area = (88.26,30.2,300.4,552.54))
print(df2.shape)


# In[ ]:


# concatenate two dataframes
df = pd.concat([df1,df2]) 
print(df.shape)


# ### Step 2 Drop useless columns and rows

# In[ ]:


'''
As we can see there are 230 rows and 14 columns in this dataframe
First, we will drop all rows where 'Unnamed: 0'(Country Name)are Nan
'''
df = df.dropna(subset = ['Unnamed: 0'])
print(df.shape)
df.head()


# In[ ]:


#For the country name should be unique, thus, find out all rows that not unique and drop them
df['Unnamed: 0'].value_counts()


# In[ ]:


#Also, we find that there are two countries spilt into two rows, for their names are too long

# Obviously, drop 'Countries' and 'and areas' rows
df = df[(df['Unnamed: 0'] != 'Countries') & (df['Unnamed: 0'] != 'and areas')]

# drop the half name of country
df = df[(df['Unnamed: 0'] != 'Democratic People\'s Republic of') & (df['Unnamed: 0'] != 'The former Yugoslav Republic of')]

# concatenate two country names
df.loc[df['Unnamed: 0'] =='Korea','Unnamed: 0']= 'Democratic People\'s Republic of Korea'
df.loc[df['Unnamed: 0'] =='Macedonia','Unnamed: 0']= 'The former Yugoslav Republic of Macedonia'

df.shape


# As we can see that the number of rows and columns meet the requirement

# ### Step 3 Split column which contains multiple data

# In[ ]:


# reset the index of the dataframe
df = df.reset_index(drop = True)

df.head()


# In[ ]:


#split column'Unnamed: 1' by space, split two times, into column'1','2','3'
d1 = pd.DataFrame(df['Unnamed: 1'].str.split(' ', 2).tolist(),columns = ['1','2','3'])

#split column'Unnamed: 2' by space, split two times, into column'4','5','6'
d2 = pd.DataFrame(df['Unnamed: 2'].str.split(' ', 2).tolist(),columns = ['4','5','6'])

#split column'Immunization coverage (%)' by space, split 4 times, into column'7','8','9',''10,'11'
d3 = pd.DataFrame(df['Immunization coverage (%)'].str.split(' ', 4).tolist(),columns = ['7','8','9','10','11'])

#split column 'Pneumonia Diarrhoea' by space, split one time, into column'12','13'
d4 = pd.DataFrame(df['Pneumonia Diarrhoea'].str.split(' ', 1).tolist(),columns = ['12','13'])

#concatenate all columns in order 
df = pd.concat([df['Unnamed: 0'],d1,d2,df['Unnamed: 3'],df['Unnamed: 4'],df['Unnamed: 5'],d3,df['Unnamed: 7'],df['Unnamed: 8'],df['Unnamed: 9'],d4,df['Unnamed: 11'],df['Malaria'],df['Unnamed: 13']], axis = 1)

df.head()


# ### Step 4 Set Country Index and Columns Names

# In[ ]:


# Set the country names as row indices
df = df.set_index(df['Unnamed: 0'].values)

# Delete "Unnamed: 0" column, it is now redundant.
df = df.drop('Unnamed: 0', 1)

# Reindex columns
df.columns = list(range(len(df.columns))) 

# Set the 
df.index.set_names('Country Name',inplace = True)

# have a look for the first five rows
df.head()


# In[ ]:


#using regular expression to replace all non-number to ''
df.replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
df.head()


# ### Step 5 Save the dataframe as CSV file

# In[ ]:


df.to_csv('./health.csv')


# ## 3. Summary
# This assessment measured the understanding of PDF file and how to extract data from it. The main outcomes achieved while applying these techniques were:
# 
# - 1.**Read data from PDF**. There are several packages and methods to read data from pdf, such 
# 
# - 2.**Data frame manipulation**. By using the `pandas` package, adding, deleting, searching, editing data can be easily done in dataframe. Additional operations like filtering, slicing, makes the data management much easier.
# 
# - 3.**Exporting data to specific format**. By using built-in functions like `DataFrame.to_csv()` it was possible to export data frames into `.txt` files without additional formatting and transformations. 

# ## 4. References
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.to_csv. Retrieved from http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.dropna. Retrieved from https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html
# 
# - The re Project. (2016a). regular expression documentation: Retrieved from https://docs.python.org/3.6/library/re.html
