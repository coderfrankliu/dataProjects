
# coding: utf-8

# In[1]:


import pandas as pd
import re


# In[2]:


excel_data = pd.ExcelFile('3303_13 causes of death by year of occurrence (australia).xls') 
excel_data.sheet_names 


# In[3]:


df = excel_data.parse('Table 13.1') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))


# In[4]:


dfAU = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfAU = dfAU.add_suffix(' Australia')
dfAU['Causes of death'] = df[0]


# In[5]:


dfAU.head()


# In[6]:


df = excel_data.parse('Table 13.2') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()
    
dfNSW = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfNSW = dfNSW.add_suffix(' NSW')
dfNSW['Causes of death'] = df[0]
# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))


# In[7]:


df = excel_data.parse('Table 13.3') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfVIC = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfVIC = dfVIC.add_suffix(' VIC')
dfVIC['Causes of death'] = df[0]


# In[8]:


df = excel_data.parse('Table 13.4') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfQLD = pd.DataFrame({    
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfQLD = dfQLD.add_suffix(' QLD')
dfQLD['Causes of death'] = df[0]


# In[9]:


df = excel_data.parse('Table 13.5') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfSA = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfSA = dfSA.add_suffix(' SA')
dfSA['Causes of death'] = df[0]


# In[10]:


df = excel_data.parse('Table 13.6') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfWA = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfWA = dfWA.add_suffix(' WA')
dfWA['Causes of death'] = df[0]


# In[11]:


df = excel_data.parse('Table 13.7') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfTAS = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfTAS = dfTAS.add_suffix(' TAS')
dfTAS['Causes of death'] = df[0]


# In[12]:


df = excel_data.parse('Table 13.8') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfNT = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfNT = dfNT.add_suffix(' NT')
dfNT['Causes of death'] = df[0]


# In[13]:


df = excel_data.parse('Table 13.9') 

# drop the columns which are all NaNs
df = df.dropna(axis=1, how = 'all') 

# drop the rows which are all NaNs
df = df.dropna(axis=0, how = 'all') 

df.columns = list(range(len(df.columns))) 

df = df.dropna(subset = [0])

df = df[df[0].str.match('.+\([A-Z][0-9][0-9]\)')]

df = df.reset_index(drop = True)
df.head()

# check if the number of people is correct (male + female = total)
for i in range(1,32,3):
    print(df[i+2].equals(df[i]+df[i+1]))
    
dfACT = pd.DataFrame({
    '2006 male' : df[1],
    '2006 female' : df[2],
    '2007 male' : df[4],
    '2007 female' : df[5],
    '2008 male' : df[7],
    '2008 female' : df[8],
    '2009 male' : df[10],
    '2009 female' : df[11],
    '2010 male' : df[13],
    '2010 female' : df[14],
    '2011 male' : df[16],
    '2011 female' : df[17],
    '2012 male' : df[19],
    '2012 female' : df[20],
    '2013 male' : df[22],
    '2013 female' : df[23],
    '2014 male' : df[25],
    '2014 female' : df[26],
    '2015 male' : df[28],
    '2015 female' : df[29],
    '2016 male' : df[31],
    '2016 female' : df[32]
})
dfACT = dfACT.add_suffix(' ACT')
dfACT['Causes of death'] = df[0]


# In[14]:


dfAll = pd.concat([dfNSW, dfVIC, dfQLD, dfSA, dfWA, dfTAS, dfNT, dfACT], axis = 1)


# In[15]:


dfAll = dfAll.drop('Causes of death', 1)
dfAll['Causes of death'] = df[0]


# In[16]:


print(dfAll.shape)
dfAll.head()


# In[17]:


dfAll.to_csv('./AustraliaDeath.csv')


# In[18]:


excel_data = pd.ExcelFile('310104.xls') 
df = excel_data.parse('Data1') 
df.head()


# In[19]:


df = df.groupby(pd.PeriodIndex(df.Date, freq='A'), axis=0).mean()


# In[20]:


df = df.rename(columns = {'Estimated Resident Population ;  Male ;  New South Wales ;' : 'male NSW',
                          'Estimated Resident Population ;  Male ;  Victoria ;' : 'male VIC',
                          'Estimated Resident Population ;  Male ;  Queensland ;' : 'male QLD',
                          'Estimated Resident Population ;  Male ;  South Australia ;' : 'male SA',
                          'Estimated Resident Population ;  Male ;  Western Australia ;' : 'male WA',
                          'Estimated Resident Population ;  Male ;  Tasmania ;' : 'male TAS',
                          'Estimated Resident Population ;  Male ;  Northern Territory ;' : 'male NT',
                          'Estimated Resident Population ;  Male ;  Australian Capital Territory ;' : 'male ACT',
                          'Estimated Resident Population ;  Female ;  New South Wales ;' : 'female NSW',
                          'Estimated Resident Population ;  Female ;  Victoria ;' : 'female VIC',
                          'Estimated Resident Population ;  Female ;  Queensland ;' : 'female QLD',
                          'Estimated Resident Population ;  Female ;  South Australia ;' : 'female SA',
                          'Estimated Resident Population ;  Female ;  Western Australia ;' : 'female WA',
                          'Estimated Resident Population ;  Female ;  Tasmania ;' : 'female TAS',
                          'Estimated Resident Population ;  Female ;  Northern Territory ;' : 'female NT',
                          'Estimated Resident Population ;  Female ;  Australian Capital Territory ;' : 'female ACT'   
                         })
df
df = df.applymap('{:.0f}'.format)


# In[23]:


df = df.filter(regex = ('[A-Z]{2,3}$'))
df.shape


# In[22]:


df.to_csv('./population.csv')


# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.to_csv. Retrieved from http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.dropna. Retrieved from https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html
# 
# - The re Project. (2016a). regular expression documentation: Retrieved from https://docs.python.org/3.6/library/re.html
