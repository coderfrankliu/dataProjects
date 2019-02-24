
# coding: utf-8

# # FIT5145 Task 3 in Assessment 2
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
import math
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import linear_model

get_ipython().magic('matplotlib inline')


# ## 2. Load the data and check missing values 

# In[2]:


# import the  file 
df = pd.read_csv("dataset3_with_missing.csv")


# In[3]:


df.info()


# In[4]:


df.isnull().sum()


# ## 3 . Investigate with missing values

# ### 3.1 sqft_living, sqft_above, sqft_basement

# After scanning the data, we can see that ** sqft_living = sqft_above + sqft_basement**

# In[5]:


df['sqft_living'] = df['sqft_living'].fillna(df['sqft_above']+df['sqft_basement'])
df[df['sqft_living'].isnull()]


# In[6]:


df['sqft_above'] = df['sqft_above'].fillna(df['sqft_living']-df['sqft_basement'])
df[df['sqft_above'].isnull()]


# In[7]:


df['sqft_basement'] = df['sqft_basement'].fillna(df['sqft_living']-df['sqft_above'])
df[df['sqft_basement'].isnull()]


# ### 3.1 bathrooms

# **Step1:** 
# Build a linear regression by the data without null.
# Split it into train_x,y and testx,y. After verifying the accuracy of the model, using this model to impute missing value.

# As the date and id definitely will not influence the bathrooms remove them.

# In[8]:


dropna_df = df.copy()


# In[9]:


#As date is object, id is for unify different house so drop them 
cols = dropna_df.columns.tolist()
cols = cols[2:4] + cols[5:] + cols[4:5]
dropna_df = dropna_df[cols]


# In[10]:


dropna_df.isnull().sum()


# In[11]:


# impute_df 
impute_df = dropna_df.copy()


# In[12]:


# Data without null value
dropna_df = dropna_df.dropna(subset=['bathrooms'],axis=0)


# In[13]:


X_train, X_test, y_train, y_test = train_test_split(dropna_df.iloc[:,:-1],dropna_df.iloc[:,-1:], random_state = 1)


# In[14]:


map(pd.np.shape,[X_train, X_test, y_train, y_test])


# In this case, I would use all data except null to train a model:
# so X_train is ...
# 

# In[15]:


import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
X_Train=X_train.values
X_Train=np.asarray(X_Train)

# Finding normalised array of X_Train
X_std=StandardScaler().fit_transform(X_Train)
from sklearn.decomposition import PCA
pca = PCA().fit(X_std)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlim(0,16,1)
plt.grid()
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')


# In[16]:


import seaborn as sns
result = pd.concat([X_train, y_train], axis = 1)# GETTING Correllation matrix
corr_mat=result.corr(method='pearson')
plt.figure(figsize=(20,10))
sns.heatmap(corr_mat,vmax=1,square=True,annot=True,cmap='cubehelix')


# As we can see, 7 componets can explain over 80% variance, Top 7 componets related to bathrooms are: 'sqft_living', 'sqft_above', 'grade', 'floors','price','bedrooms','yr_built'

# seven component:

# In[17]:


lm_impute1 = LinearRegression()
lm_impute1.fit(X_train,y_train)
print ('r-squared for this model = ',lm_impute1.score(X_test,y_test))
y_pred = lm_impute1.predict(X_test)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# So this the regression based on these conpenents R-squared is 0.72, which is not bad. 
# when we evaluate a missing-data method, to maximise the use of available information is important,however, in order to pervent from overfitting, we should also drop the coeffcients which are not greatly influence the result

# In[18]:


X_train = X_train.drop(['sqft_lot','waterfront','view','condition','sqft_basement','yr_renovated','zipcode','lat','long'],1)
X_test = X_test.drop(['sqft_lot','waterfront','view','condition','sqft_basement','yr_renovated','zipcode','lat','long'],1)


# In[19]:


lm_impute = LinearRegression()
lm_impute.fit(X_train[[x for x in X_train]],y_train)
print ('r-squared for this model = ',lm_impute.score(X_test,y_test))
y_pred = lm_impute.predict(X_test)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# Although its r-squared is lower than before, but we dropped as much coefficient as we can.

# In[20]:


X_train = X_train.drop(['yr_built'],1)
X_test = X_test.drop(['yr_built'],1)
lm_impute3 = LinearRegression()
lm_impute3.fit(X_train,y_train)
print ('r-squared for this model = ',lm_impute3.score(X_test,y_test))
y_pred = lm_impute3.predict(X_test)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# As we can, when I drop 'yr_built', which is the 7th relative coefficient opponents, the r-squared has greatly decreased, so I stop dropping.

# In[21]:


impute_df[impute_df['bathrooms'].isnull()].head()


# Replace the null values to predict value

# In[22]:


predict = lm_impute.predict(impute_df.drop(['sqft_lot','waterfront','view','condition','sqft_basement',                                   'yr_renovated','zipcode','lat','long','bathrooms'],axis=1)) 


# In[23]:


l = []
for i in predict:
    s = round(i[0]*4)/4
    l.append(s)

se =pd.Series(l)
impute_df['predict'] = se.values


# In[24]:


impute_df.loc[impute_df['bathrooms'].isnull(),'bathrooms'] = impute_df['predict']


# In[25]:


impute_df = impute_df.drop('predict',1)


# Reformat the dataframe

# In[26]:


impute_df['id'] = df['id']
impute_df['date'] = df['date']
#reshape the data 
cols = impute_df.columns.tolist()
cols = cols[-2:-1]+ cols[-1:0]+ cols[0:2] + cols[-3:-2] + cols[2:16]
impute_df = impute_df[cols]


# In[27]:


impute_df.isnull().sum()


# ## 5.  Save the dataframe as CSV file

# In[28]:


impute_df.to_csv('./dataset3_solution.csv')


# ## 4. References
# - sheinis (Aug 24 2016). *Read Excel File in Python* [Response to]. Retrieved from https://stackoverflow.com/questions/22169325/read-excel-file-in-python
# 
# https://stackoverflow.com/questions/41238769/warning-messages-when-using-python
# 
# https://stackoverflow.com/questions/30357276/pandas-fillna-with-another-column
# 
# https://stackoverflow.com/questions/28305008/algorithm-to-find-similar-strings-in-a-list-of-many-strings
# 
# https://www.kaggle.com/ankitjha/comparing-regression-models/code
# 
