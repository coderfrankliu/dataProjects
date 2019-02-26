
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
from motionchart.motionchart import MotionChart


# In[2]:


erp = pd.read_csv("ERP_by state and gender.csv")


# In[3]:


dferpraw = pd.DataFrame({
    'Date' : erp['Unnamed: 0'],
    'NSW' : erp['Estimated Resident Population ;  Persons ;  New South Wales ;'],
    'VIC' : erp['Estimated Resident Population ;  Persons ;  Victoria ;'],
    'QLD' : erp['Estimated Resident Population ;  Persons ;  Queensland ;'],
    'SA' : erp['Estimated Resident Population ;  Persons ;  South Australia ;'],
    'WA' : erp['Estimated Resident Population ;  Persons ;  Western Australia ;'],
    'TAS' : erp['Estimated Resident Population ;  Persons ;  Tasmania ;'],
    'NT' : erp['Estimated Resident Population ;  Persons ;  Northern Territory ;'],
    'ACT' : erp['Estimated Resident Population ;  Persons ;  Australian Capital Territory ;']  
})
print(dferpraw.head())
#The regions are now values of column 'Region'
dferp = pd.melt(dferpraw, id_vars=['Date'],value_vars=['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'],var_name='Region')

# rename the value column
dferp.rename(columns = {'value':'ERP'}, inplace = True)

dferp = dferp.pivot(index = 'Date', columns = 'Region', values = 'ERP')
dferp = dferp.reset_index()

dferp = dferp.groupby(pd.PeriodIndex(dferp.Date, freq='Q'), axis=0).mean()
dferp = dferp.reset_index()
dferp = pd.melt(dferp, id_vars=['Date'],value_vars=['ACT','NSW','NT','QLD','SA','TAS','VIC','WA'],var_name='Region')
dferp=dferp.rename(columns = {'value':'ERP'})
dferp.head()


# In[4]:


price = pd.read_csv("House Price Index.csv")


# In[5]:


dfpriceraw = pd.DataFrame({
    'Date' : price['Unnamed: 0'],
    'NSW' : price['Residential Property Price Index ;  Sydney ;'],
    'VIC' : price['Residential Property Price Index ;  Melbourne ;'],
    'QLD' : price['Residential Property Price Index ;  Brisbane ;'],
    'SA' : price['Residential Property Price Index ;  Adelaide ;'],
    'WA' : price['Residential Property Price Index ;  Perth ;'],
    'TAS' : price['Residential Property Price Index ;  Hobart ;'],
    'NT' : price['Residential Property Price Index ;  Darwin ;'],
    'ACT' : price['Residential Property Price Index ;  Canberra ;']  
})

#The regions are now values of column 'Region'
dfprice = pd.melt(dfpriceraw, id_vars=['Date'],value_vars=['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA'],var_name='Region')

dfprice.rename(columns = {'value':'House Price Index'}, inplace = True)

dfprice = dfprice.pivot(index = 'Date', columns = 'Region', values = 'House Price Index')
dfprice = dfprice.reset_index()

dfprice = dfprice.groupby(pd.PeriodIndex(dfprice.Date, freq='Q'), axis=0).mean()
dfprice = dfprice.reset_index()
dfprice = pd.melt(dfprice, id_vars=['Date'],value_vars=['ACT','NSW','NT','QLD','SA','TAS','VIC','WA'],var_name='Region')

dfprice=dfprice.rename(columns = {'value':'House Price Index'})
#have a look for the first five rows
dfprice.head()


# In[6]:


unemp = pd.read_excel("SA4 Time Series - October 2016.xls", sheetname='Time Series')


# In[7]:


dfunempraw = pd.DataFrame({
    'Region' : unemp['State/Territory'],
    'Date' : unemp['Date'],
    'Unemployment Rate' : unemp['Unemployment Rate (15+)'],
})

#dfunemp = dfunempraw.rename(columns = {'State/Territory':'Region'})
dfunemp = dfunempraw
dfunemp = dfunemp[(dfunemp['Date'] >= '2005/12/01') & (dfunemp['Date'] <= '2015/6/01')]
dfunemp = dfunemp.reset_index(drop = True)
dfunemp = dfunemp.pivot(index = 'Date', columns = 'Region' ,values = 'Unemployment Rate')
dfunemp = dfunemp.reset_index()

dfunemp = dfunemp.groupby(pd.PeriodIndex(dfunemp.Date, freq='Q'), axis=0).mean()
dfunemp = dfunemp.reset_index()

dfunemp = pd.melt(dfunemp, id_vars=['Date'],value_vars=['ACT','NSW','NT','QLD','SA','TAS','VIC','WA'],var_name='Region')
dfunemp=dfunemp.rename(columns = {'value':'Unemployment Rate'})

dfunemp.head()


# In[8]:


finaldf1 = pd.merge(dferp, dfprice, how = 'left', on = ['Date','Region'])
finaldf = pd.merge(finaldf1, dfunemp, how = 'left', on = ['Date', 'Region'])
finaldf['Date'] = finaldf['Date'].astype('str')
finaldf['year'], finaldf['quarter'] = finaldf['Date'].str.split('Q', 1).str
finaldf['quarter'] = finaldf['quarter'].replace(['1', '2', '3', '4'],['/03/01','/06/01','/09/01','/12/01'])
finaldf['Date'] = finaldf['year'] + finaldf['quarter']
finaldf = finaldf.drop(['year','quarter'],axis = 1)

finaldf.head()


# In[9]:


finaldf.to_csv('./formateddata.csv')


# The following html code block is just to make sure that you will see the entire motion chart nicely in the output cell.

# In[10]:


get_ipython().run_cell_magic('html', '', '<style>\n.output_wrapper, .output {\n    height:auto !important;\n    max-height:1000px;  /* your desired max-height here */\n}\n.output_scroll {\n    box-shadow:none !important;\n    webkit-box-shadow:none !important;\n}\n</style>')


# In[11]:


mChart = MotionChart(df = finaldf, key='Date', x='Unemployment Rate', y='House Price Index', xscale='linear', yscale='linear',
                     size='ERP', color='Region', category='Region')

mChart.to_notebook()


# In[12]:


# unemployment rate and houser price index, by date
plt.figure(figsize=(20,10))
plt.style.use('ggplot')
plt.plot(finaldf['Unemployment Rate'], label="Unemployment")
plt.plot(finaldf['House Price Index']/10, label="House Price Index/10")
plt.title('Relationship betweenn Unemployment Rate and House Price Index')
plt.legend(bbox_to_anchor=(1.05, 1), loc = 2, borderaxespad=0.)
plt.show()


# In[13]:


dfd = finaldf
dfd = dfd.set_index(keys= dfd['Date'].values)
dfd = dfd.drop('Date', 1)
dfd.index.set_names('Date',inplace = True)


# In[14]:


#house price index in different states changing by date
get_ipython().magic('matplotlib inline')
plt.figure(figsize=(20,10))
plt.plot(dfd[dfd.Region == 'NSW']['House Price Index'], label="NSW")
plt.plot(dfd[dfd.Region == 'VIC']['House Price Index'], label="VIC")
plt.plot(dfd[dfd.Region == 'QLD']['House Price Index'], label="QLD")
plt.plot(dfd[dfd.Region == 'SA']['House Price Index'], label="SA")
plt.plot(dfd[dfd.Region == 'WA']['House Price Index'], label="WA")
plt.plot(dfd[dfd.Region == 'TAS']['House Price Index'], label="TAS")
plt.plot(dfd[dfd.Region == 'NT']['House Price Index'], label="NT")
plt.plot(dfd[dfd.Region == 'ACT']['House Price Index'], label="ACT")
plt.title('House Price Rate by States')
plt.xlabel('Date')
plt.ylabel('House Price Rate')
plt.grid(True)  
plt.gcf().autofmt_xdate()
plt.legend(bbox_to_anchor=(1.0, 1), loc=2, borderaxespad=1.0)
plt.show()


# In[15]:


#unemployment rate in different states changing by date
plt.figure(figsize=(20,10))
plt.plot(dfd[dfd.Region == 'NSW']['Unemployment Rate'], label="NSW")
plt.plot(dfd[dfd.Region == 'VIC']['Unemployment Rate'], label="VIC")
plt.plot(dfd[dfd.Region == 'QLD']['Unemployment Rate'], label="QLD")
plt.plot(dfd[dfd.Region == 'SA']['Unemployment Rate'], label="SA")
plt.plot(dfd[dfd.Region == 'WA']['Unemployment Rate'], label="WA")
plt.plot(dfd[dfd.Region == 'TAS']['Unemployment Rate'], label="TAS")
plt.plot(dfd[dfd.Region == 'NT']['Unemployment Rate'], label="NT")
plt.plot(dfd[dfd.Region == 'ACT']['Unemployment Rate'], label="ACT")
plt.title('Unemployment Rate of each state by date')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate')
plt.grid(True)  
plt.gcf().autofmt_xdate()
plt.legend(bbox_to_anchor=(1.0, 1), loc=2, borderaxespad=1.0)
plt.show()


# In[16]:


plt.figure(figsize=(20,10))
plt.plot(dfd[dfd.Region == 'NSW']['House Price Index']/10, label="NSW", color = 'red')
plt.plot(dfd[dfd.Region == 'NSW']['Unemployment Rate'], label="NSW", linestyle = 'dashed', color = 'red')
plt.plot(dfd[dfd.Region == 'VIC']['House Price Index']/10, label="VIC", color = 'green')
plt.plot(dfd[dfd.Region == 'VIC']['Unemployment Rate'], label="VIC", linestyle = 'dashed', color = 'green')
plt.title('House Price Rate and Unemployment Rate of VIC and NSW')
plt.xlabel('Date')
plt.ylabel('House Price Rate')
plt.grid(True)  
plt.gcf().autofmt_xdate()
plt.legend(bbox_to_anchor=(1.0, 1), loc=2, borderaxespad=1.0)
plt.show()


# In[17]:


dfd1 = finaldf
dfd1['Unemployment people'] = dfd1['Unemployment Rate'] * dfd1['ERP']/100
dfd1 = dfd1.set_index(keys= dfd1['Date'].values)
dfd1 = dfd1.drop('Date', 1)
dfd1.index.set_names('Date',inplace = True)
dfd1.head()


# In[18]:


plt.figure(figsize=(20,10))
plt.plot(dfd1[dfd1.Region == 'NSW']['Unemployment people'], label="NSW")
plt.plot(dfd1[dfd1.Region == 'VIC']['Unemployment people'], label="VIC")
plt.plot(dfd1[dfd1.Region == 'QLD']['Unemployment people'], label="QLD")
plt.plot(dfd1[dfd1.Region == 'SA']['Unemployment people'], label="SA")
plt.plot(dfd1[dfd1.Region == 'WA']['Unemployment people'], label="WA")
plt.plot(dfd1[dfd1.Region == 'TAS']['Unemployment people'], label="TAS")
plt.plot(dfd1[dfd1.Region == 'NT']['Unemployment people'], label="NT")
plt.plot(dfd1[dfd1.Region == 'ACT']['Unemployment people'], label="ACT")
plt.title('Number of unemployment people')
plt.xlabel('Date')
plt.ylabel('Number of unemployment people')
plt.grid(True)  
plt.gcf().autofmt_xdate()
plt.legend(bbox_to_anchor=(1.0, 1), loc=2, borderaxespad=1.0)
plt.show()


# In[19]:


dfVac = pd.read_csv("VacancyRate.csv")
dfVac.head()


# In[20]:


climateChart = MotionChart(df = dfVac, key='Date', x='Vacancy Rate', y='House Price Index', xscale='linear', yscale='linear',
                     size='Population', color='State', category='State')

climateChart.to_notebook()


# # Reference
# 
# - sheinis (Aug 24 2016). *Read Excel File in Python* [Response to]. Retrieved from
# https://stackoverflow.com/questions/22169325/read-excel-file-in-python
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: Reshaping and Pivot Tables. Retrived from
# http://pandas.pydata.org/pandas-docs/stable/reshaping.html
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: Indexing and Selecting Data. Retrived from
# http://pandas.pydata.org/pandas-docs/stable/indexing.html#reset-the-index
# 
# - Edamame (Jun 23 2017). *pandas: merge (join) two data frames on multiple columns
# * [Response to]. Retrieved from https://stackoverflow.com/questions/41815079/pandas-merge-join-two-data-frames-on-multiple-columns
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.pivot. Retrived from
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.pivot.html
# 
# - hmelberg. Retrived from
# https://github.com/hmelberg/motionchart/blob/master/motionchart/motionchart.py
# 
# - The pandas Project. (2016a). pandas 0.22.0 documentation: pandas.DataFrame.to_csv. Retrieved from http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html#pandas.DataFrame.to_csv
# 
# - tatwright (Dec 1 2008). *How do you change the size of figures drawn with matplotlib?* Retrived from https://stackoverflow.com/questions/332289/how-do-you-change-the-size-of-figures-drawn-with-matplotlib
