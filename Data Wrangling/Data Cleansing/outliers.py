
# coding: utf-8

# # FIT5196 Task 4 in Assessment 2
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
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import scipy.stats as stats
from scipy.stats import norm
get_ipython().magic('matplotlib inline')


# ## 2. Load the data using Pandas library 

# In[2]:


# import the  file 
df = pd.read_csv("dataset4_with_outliers.csv")


# In[3]:


df


# # 3 Investigate Outliers

# ### 3.1 Longitude and latitude

# As we know zipcode indicates the longtitude and altitude should be close, therefore, if the longtitude or altitude is far away from others are outliers

# In[4]:


bp = df.boxplot(column='long',by = 'zipcode')


# In[5]:


sns.lmplot( x="lat", y="long", data=df, fit_reg=False, hue='zipcode', legend=False, palette="Set1")


# Obviously, the longitude which upper than -121.6 are outliers

# In[6]:


df.loc[(df['long'] > -121.6)]


# By analysing longitude and altitude, I found 9 outliers

# In[7]:


df = df[df['long'] <= 121.6] 


# ## 3.2 living_sqrt and lot_sqrt

# As we know that the price per livingsqft is basically vary from the suburb, which means that the house's price per livingsqrt in the same zipcode should not vary too much.

# In[8]:


df['price_per_livingsqft'] = df['price']/df['sqft_living']
bp = df.boxplot(column='price_per_livingsqft',by = 'zipcode')


# There are 5 points very suspicious, which are over 800 per sqft

# In[9]:


df[df['price_per_livingsqft']>800]


# By analysing price and sqft_living, I found 5 outliers

# In[10]:


df = df[df['price_per_livingsqft'] <= 800]


# As we know, generally, in the same suburb, the function of the house is similar, in remote region the living_aqft/lot_sqft generally 

# In[11]:


df['lot_vs_living'] = df['sqft_lot']/df['sqft_living']


# In[12]:


bp = df.boxplot(column='lot_vs_living',by = 'zipcode')


# The proportion of the living and lot are too weird compared to other house in the same suburb.

# In[13]:


df[df['lot_vs_living'] > 1500]


# In[14]:


df = df[df['lot_vs_living'] < 1500]


# ## 3.2 bedrooms and bathrooms

# As we can see there are several houses with lots of bedrooms,
# we also know that the numbers of bedrooms of a house is also related to the number of bathrooms: 
# e.g. if a house has 20 bedrooms but 2 bathrooms, it should be the outlier. Also, if a house has 3 bedrooms but 6 bathrooms, it should be outlier as well.
# So I introduce a column(bedrooms/bathrooms) to detect the outlier between them.(extemely high or low either suspicious)

# In[15]:


df['bedrooms_bathrooms'] = df['bedrooms']/df['bathrooms']


# In[16]:


bp = df.boxplot(column='bedrooms_bathrooms')


# The number of 'bedrooms_bathrooms' indicates the number of bathroom per bedroom, by common sense and searching information in house selling website, this number would be maximum 5, so 'bedrooms_bathsrooms' larger than 5 are outlier

# In[17]:


df[df['bedrooms_bathrooms'] > 5]


# There are 12 outliers for the relationship between bedrooms and bathrooms

# In[18]:


df = df[df['bedrooms_bathrooms'] <= 5]


# ## 3.3 Bedrooms

# In[19]:


df['sqft_bedrooms'] = df['sqft_above']/df['bedrooms']


# In[20]:


bp = df.boxplot(column='sqft_bedrooms',by = 'grade')


# There is a point in grade 8 great different from other, I treat it as outlier.

# In[21]:


df[df['sqft_bedrooms'] > 2500]


# In[22]:


df = df[df['sqft_bedrooms'] <2500]


# ## 3.4 Floors

# In order to find out if there has disproportionate number of floor, I introduced bedrooms/floors

# In[23]:


df['bedrooms_floor'] = df['bedrooms']/df['floors']


# In[24]:


sample = df['bedrooms_floor']
#mean, parameters[0] and std, parameters[1]
parameters = norm.fit(sample)

x = np.linspace(min(sample),max(sample),100)

# Generate the pdf (fitted distribution)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
# Generate the pdf (normal distribution non fitted)
normal_pdf = norm.pdf(x)

plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[25]:


mean = parameters[0]
sd = parameters[1]
#can't use 3-sigma rule here, however, I would choose that extremely small one
lower = mean - 2*sd
df.loc[df['bedrooms_floor'] <= lower]


# Since A 3-floors house only has one bedroom is so wierd, I treat these two records as outliers

# In[26]:


df[df.bedrooms_floor<0.5]


# In[27]:


df = df[df.bedrooms_floor>=0.5]


# ## 3.5 Price

# There are lots of outliers in the price, so I would figure out the outliers of price by using ** 3-sigma rule** to identify the outliers

# In[28]:


bp = df.boxplot(column='price_per_livingsqft',by = 'grade')


# There are several points in grade 4 suspiciously higher than others and one point in grade 12 lower than others:

# In[29]:


df.loc[((df['price_per_livingsqft'] >500) & (df['grade'] ==4)) | ((df['price_per_livingsqft'] < 200 )& (df['grade'] ==12))]


# These rows did't have relevent price acccording to their grades, so I treated them as outliers

# In[30]:


df = df.drop([1591,5197,7323])


# Then have a closer look on the price on different grades

# In[31]:


sample = df[df.grade ==5]['price']
#mean, parameters[0] and std, parameters[1]
parameters = norm.fit(sample)
x = np.linspace(min(sample),max(sample),100)
# Generate the pdf (fitted distribution)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
# Generate the pdf (normal distribution non fitted)
normal_pdf = norm.pdf(x)
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,20,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[32]:


mean = sample.mean()
sd = sample.std()
upper = mean + 3*sd
lower = mean - 3*sd
print(upper)
print(lower)
df.loc[df['grade']== 5][(df['price'] <= lower) | (df['price'] >= upper)]


# In[33]:


df = df.drop([5135,5360,6173,8106])


# In[34]:


sample = df[df.grade ==6]['price']
parameters = norm.fit(sample)
x = np.linspace(min(sample),max(sample),100)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
normal_pdf = norm.pdf(x)
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,20,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[35]:


mean = sample.mean()
sd = sample.std()
upper = mean + 3*sd
lower = mean - 3*sd
df.loc[df['grade']== 6][(df['price'] <= lower) | (df['price'] >= upper)]


# In[36]:


df = df.drop([69,2651,5768,8002])


# In[37]:


sample = df[df.grade ==7]['price']
parameters = norm.fit(sample)
x = np.linspace(min(sample),max(sample),100)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
normal_pdf = norm.pdf(x)
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,20,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[38]:


mean = sample.mean()
sd = sample.std()
upper = mean + 3*sd
lower = mean - 3*sd
_drop = df.loc[df['grade']== 7][(df['price'] <= lower) | (df['price'] >= upper)].index


# In[39]:


df = df.drop(_drop)


# In[40]:


sample = df[df.grade ==8]['price']
parameters = norm.fit(sample)
x = np.linspace(min(sample),max(sample),100)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
normal_pdf = norm.pdf(x)
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,200,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[41]:


mean = sample.mean()
sd = sample.std()
upper = mean + 3*sd
lower = mean - 3*sd
_drop = df[df['grade'] == 8][(df['price'] <= lower) | (df['price'] >= upper)].index


# In[42]:


df = df.drop(_drop)


# In[43]:


sample = df[df.grade ==9]['price']
parameters = norm.fit(sample)
x = np.linspace(min(sample),max(sample),100)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
normal_pdf = norm.pdf(x)
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,20,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[44]:


mean = sample.mean()
sd = sample.std()
upper = mean + 3*sd
lower = mean - 3*sd
df.loc[df['grade']== 9][(df['price'] <= lower) | (df['price'] >= upper)]


# In[45]:


df = df.drop([1584,2172,2891,5097,9463])


# In[46]:


sample = df[df.grade ==10]['price']
parameters = norm.fit(sample)
x = np.linspace(min(sample),max(sample),100)
fitted_pdf = norm.pdf(x ,loc = parameters[0],scale = parameters[1])
normal_pdf = norm.pdf(x)
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=1)
plt.hist(sample,normed=1,color="cyan")
plt.title("Normal distribution fitting")
plt.legend()
plt.show()


# In[47]:


mean = sample.mean()
sd = sample.std()
upper = mean + 3*sd
lower = mean - 3*sd
df.loc[df['grade']== 10][(df['price'] <= lower) | (df['price'] >= upper)]


# In[48]:


df = df.drop([5524])


# In[49]:


df.head()


# In[50]:


df = df.reset_index(drop = True)
columns = ['bedrooms_floor', 'sqft_bedrooms', 'bedrooms_bathrooms','lot_vs_living','price_per_livingsqft']
df.drop(columns, inplace=True, axis=1)


# In[51]:


df.to_csv('./dataset4_solution.csv')


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
