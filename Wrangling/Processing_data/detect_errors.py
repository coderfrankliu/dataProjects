
# coding: utf-8

# # FIT5196 Task 1 Detecting Errors
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
import datetime
import difflib


# ## 2. Load the data using Pandas library 

# In[2]:


# import the  file 
df = pd.read_csv("dataset1_with_error.csv")


# In[3]:


# has a look how many rows and columns of the sheet
print(df.shape)


# In[4]:


df.info()


# ## 3 . Audit the data

# ### 3.1 Id

# In[5]:


# check if the Ids are all unique
df.Id.is_unique


# ### 3.2 Location

# In[6]:


# get the list of all locations, will be used to filter the location from title to replace UK afterward
location = df.Location.unique()


# In[7]:


#Have a look for the smilar city name to check is there has any typo
#for i in location:
#    if len(difflib.get_close_matches(i, location)) >=2:
#        print (difflib.get_close_matches(i, location))    


# There are several sets are suspicious:
# 
# **typo:**
# 
# - ['Nottinham', 'Nottingham', 'Nottinghamshire'] 
# - ['Oxfords', 'Oxford', 'Oxfordshire'] 
# - ['Surrey', 'Surey', 'Sudbury']
# 
# **inconsistency:**
# 
# - ['Manchester Science Park', 'Manchester']
# - ['The City', 'City']
# - ['Southampton International Airport']
# - ['Glasgow East Investment Park']
# 

# Repeatted this step I found that **Nottinham, Oxfords and Surey** were typo, at the meantime, ** Manchester Science Park and City ** were inconsistency(because it is too specific)

# In[8]:


df.Company = df.Company.replace({'Nottinham':'Nottingham',                                 'Oxfords':'Oxford',                                 'Surey':'Surrey',                                  'Manchester Science Park':'Manchester',                                 'City' : 'The City',                                 'Southampton International Airport' : 'Soouthampton',                                 'Glasgow East Investment Park' : 'Glasgow East'                               
                                })


# Since the UK is too broad, we can extract some information of location from title as well

# In[9]:


#If the location is UK there is some information of the location in the title, replace UK with
# the information from title
for i in range(0,len(df)):
    if df.iloc[i]['Location'] == 'UK':
        for a in df.iloc[i]['Title'].split():
            if a in location:
                df.iloc[[i],[2]] = a


# ## Title

# There are multiple errors in the title:
# - contains location
# - contains the salary
# - contains uncommon symbols (* etc)
# 
# In order to find error pattern, I checked title by category

# In[10]:


# the messiest category is Hospitality & Catering Jobs
df[df.Category == 'Hospitality & Catering Jobs'].head()


# As we can see, for hospitality and catering jobs, there were some patterns for their titles:
# 1. lack of vairety, we can easily list the potential jobs and replace it
# 2. sometimes contains salary or the information of the restaurant.

# In[11]:


# remove all *****k from title
df['Title'] = df['Title'].replace('*k','')
df['Title'] = df['Title'].replace('*','')


# In[12]:


def extract_hospitality_title(title):
    positionList =['Chef','Manager','']
    for position in positionList:
        if position in title:
            return position
    return title


# ### 3.4 ContractType

# In[13]:


df.ContractType.value_counts()


# In[14]:


df.ContractType = df.ContractType.replace({'not available':'non-specified','full_time':'full-time','part_time': 'part-time'})
df.ContractType.value_counts()


# ### 3.5 ContractTime

# In[15]:


df.ContractTime.value_counts()


# In[16]:


df.ContractTime = df.ContractTime.replace({'not available':'non-specified'})
df.ContractTime.value_counts()


# I thought the contract time should have some relationship with contract type, (e.g if the contract tpye is unavailable, the time should be unavailable as well)
# But it also happened in dataset2, as the dataset 2 has no error,so I just igonored it.

# In[17]:


pd.crosstab(df['ContractType'], df['ContractTime'])


# ### 3.6 Company

# In[18]:


df.Company.dropna().unique()


# In[19]:


company = df.Company.dropna().unique()


# Have a check on if there any possible type on company name

# In[20]:


# this is used to search the most likely pair of matches in company name, very time consuming.
#As there are too much Company name to check, I just check the most looked like pair.
#for i in company:
#    if len(difflib.get_close_matches(i, company)) == 2:
#         print (difflib.get_close_matches(i, company))   


# In order to keep the data's consistency, after scanning the set of similar company name, there are some pattern of errors:(just example)
# 
# -  missing some suffix
# 
# ['Anonymous', 'Anonymous Recruiter'],['VanRath IT', 'VanRath'] 
# ['Sizzling Pubs', 'Sizzling Pub Co.']
# - missing whitespace 
# 
# ['Madigan Gill', 'Madigangill'] 
# - Case insensitive 
# 
# ['Just Chefs', 'Just chefs'] 
# - composite error
# 
# ['Brookstreet UK', 'Brook Street']
# - Symbol missing 
# 
# ['Jamie s Italian', "Jamie's Italian"]
# - Typo 
# 
# ['Epsilon', 'Expion']

# For those which lack in suffix, like 'Ltd', 'Limited', I just replace it by whitespace, because it will not influence the understanding of the company name

# In[21]:


# replace all suffix
df['Company'] = df['Company'].str.replace('Co.|Ltd|Limited|UK|PLC|&|.','')
df['Company'] = df['Company'].str.replace('\'','')


# In[22]:


#fix others:
df.Company = df.Company.replace({'VanRath IT':'VanRath',                                  'Anonymous':'Anonymous Recruiter',                                  'Madigan Gill':'Madigangill',                                  'Just Chefs': 'Just chefs',                                  'Lewis Paige': 'Lewis Paige Recruitment',                                  'Detail2Leisure': 'Detail 2 Leisure',                                  'Nuffield Health   StaffNurse.com': 'Nuffield Health',                                 'Resource Solutions Group   Royal London':'Resourcing Solutions',                                'Brookstreet UK': 'Brook Street',                                 'M S Bank': 'M  S Bank',                                 'Epsilon': 'Expion',                                'NHS Lanarkshire   Medical Staffing': 'NHS Lanarkshire',                                 'One Two Trade':'OneTwoTrade',                                 'The M ller Centre':'The Miller Group',                                 'Mortimer Spinks Ltd T/A Harvey Nash': 'Mortimer Spinks'})


# ### 3.7 Category

# In[23]:


#check if the categories are consistent
df.Category.value_counts()


# ### 3.8 Salary per annum

# In[24]:


df['Salary per annum'] = df['Salary per annum'].astype('str') 
#reformat the XXk to xx000 
df['Salary per annum'] = df['Salary per annum'].replace('K','000',regex = True)


# In[25]:


df[df['Salary per annum'].str.contains('-')]


# In[26]:


#reformat the range salary to the average of the range
def salary_reformat(self):
    if '-' in self:
        salary = self.split('-')
        self = (float(salary[0].strip()) + float(salary[1].strip()))/2
    return self


# In[27]:


df['Salary per annum'] = df['Salary per annum'].apply(salary_reformat)


# ### 3.9 SourceName

# As we can see it, some sourceNames are invalid, so use regular expression to find them and correct them

# In[28]:


df.SourceName.unique()


# There are three suspicious sourcenames: 'monashstudent','jobcareer' and 'admin@caterer.com'. As we can make a regular expression to find out, is there any other errors like them.

# In[29]:


df['SourceName'] = df['SourceName'].astype('str') 
df[df.SourceName.str.contains('.com|.co|.org|.net')==False]


# In[30]:


df[df.Company =='Brightwater Group']


# In[31]:


df[df.Company =='The A24 Group']


# In[32]:


df[df.SourceName.str.contains('@')]


# In[33]:


df[df.Company =='Blu Digital']


# Assume that one company should post their advertisement on one website. So change monashstudent to staffnurse.com, change jobcareer to nijobs.com, change admin@caterer.com to totaljobs.com

# In[34]:


df.SourceName = df.SourceName.replace({'monashstudent':'staffnurse.com',                                        'jobcareer':'nijobs.com',                                       'admin@caterer.com':'totaljobs.com'})


# ### 3.10  OpenDate

# As I have found couple of errors for the Data: 1) some of the date were not in format yyyymmddTHHMMSS but yyyyddmmTHHMMSS. 2)some of the close date is earlier than the open date.

# I assume that the date format should be yyyymmddTHHMMSS

# 1) using Regular expression to find which date are invalid.(As we just have 2012,2013,2014 three years, so just 2012 is leap year)

# In[35]:


DateisValid = '(2012(((0[13578]|(10|12))(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|[1-2][0-9]))|((0[469]|11)(0[1-9]|[1-2][0-9]|30)))|201(3|4)(((0[13578]|(10|12))(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|1[0-9]|2[0-8]))|((0[469]|11)(0[1-9]|[1-2][0-9]|30))))T(([0-1][0-9])|(2[0-3]))00'

df[df.OpenDate.str.match(DateisValid) == False]


# After scanning for these dates, I assumed that I can just swap the day and month

# In[36]:


def date_reformat(date):
    year = date[0:4] 
    month = date[4:6]
    day = date[6:8]
    time = date[8:]
    if int(month) > 12:
        return year + day + month + time
    return year + month +day +time

df.OpenDate = df.OpenDate.apply(date_reformat)


# ### 3.11 CloseDate

# For closedate, we should check:
# 1. if the dates are valid
# 2. if the close date is later than open date

# In[37]:


#display all the dates are invalid
df[df.CloseDate.str.match('(2012(((0[13578]|(10|12))(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|[1-2][0-9]))|((0[469]|11)(0[1-9]|[1-2][0-9]|30)))|201(3|4)(((0[13578]|(10|12))(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|1[0-9]|2[0-8]))|((0[469]|11)(0[1-9]|[1-2][0-9]|30))))T(([0-1][0-9])|(2[0-3]))00')==False]


# In[38]:


df.OpenDate=pd.to_datetime(df.OpenDate)
df.CloseDate=pd.to_datetime(df.CloseDate)

#if the close date is ealier than open date, swap them
idx = (df.OpenDate > df.CloseDate)
df.loc[idx,['OpenDate','CloseDate']] = df.loc[idx,['CloseDate', 'OpenDate']].values


# In[39]:


df.OpenDate=pd.to_datetime(df.OpenDate)
df.CloseDate=pd.to_datetime(df.CloseDate)

df.OpenDate = df.OpenDate.apply(lambda x : x.strftime('%Y%m%dT%H%M%S'))
df.CloseDate = df.CloseDate.apply(lambda x : x.strftime('%Y%m%dT%H%M%S'))


# ### Step 5 Save the dataframe as CSV file

# In[40]:


df.to_csv('./dataset1_solution.csv')


# ## 4. References
# 
# 
# https://stackoverflow.com/questions/17097643/search-for-does-not-contain-on-a-dataframe-in-pandas
# 
# https://stackoverflow.com/questions/15325182/how-to-filter-rows-in-pandas-by-regex
