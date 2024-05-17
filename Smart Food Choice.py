#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import warnings as w
w.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns 


# In[3]:


data = pd.read_csv("C:\\Users\\Admin\\Downloads\\India_Menu.csv")


# In[4]:


data.dtypes


# In[5]:


data.head()


# In[6]:


data.shape


# In[7]:


# Checking for the null values
data.isnull().sum()


# In[8]:


# Replacing the null value 
data['Sodium (mg)'].fillna(data['Sodium (mg)'].mean(),inplace = True)


# In[9]:


data.isnull().sum().sum()


# In[10]:


data.info()


# In[11]:


data 


# In[12]:


# group by menu item and calulate mean energy for each item 
menu_items_energy = data.groupby('Menu Items')['Energy (kCal)'].mean()


# In[13]:


print(menu_items_energy)


# In[14]:


# select the top 15 menu items 
top_cal_items = menu_items_energy.nlargest(15)


# In[15]:


# caluculating the total energy of other menu items 
other_energy = menu_items_energy.drop(top_cal_items.index).sum()
top_cal_items['Others'] = other_energy


# In[16]:


top_cal_items


# In[17]:


plt.figure(figsize=(10,10))
plt.pie(top_cal_items, labels=top_cal_items.index, autopct='%1.1f%%',startangle=140)
plt.title("Energy Distribution Across Top 15 Menu Items")


# In[18]:


# Descriptive Statistics 
data.describe


# In[19]:


data.tail()


# In[20]:


# univariate Ananlysis 
# Visualize the distribution of Energy Kcal
plt.figure(figsize=(8,6)) 
sns.histplot(data['Energy (kCal)'],bins = 20, kde = True)
plt.title("Distribution of Energy (Kcal)")
plt.show()


# In[21]:


# Bivariate Analysis 
# sactter plot for protein (g) vs fats (g)
plt.figure(figsize=(8,6))
sns.regplot(x=data["Protein (g)"], y=data["Total fat (g)"],color = "green")
plt.title("Protein Vs Total Fat")
plt.show()


# In[22]:


# Multivariate Analysis 
# Pairplot for selected numerical values
selected_data =['Energy (kCal)', 'Protein (g)', 'Total fat (g)', 'Total carbohydrate (g)']
sns.pairplot(data[selected_data])
plt.show()


# In[23]:


# Outlier Detection
# Box plot for outlier detection of Energy (Kcal) 
plt.figure(figsize=(8,6))
sns.boxplot(x=data['Energy (kCal)'])
plt.title("Detection of outlier for Energy (Kcal)")
plt.show()


# In[24]:


# visualize the transformed Distribution
log_energy = np.log1p(data["Energy (kCal)"])

plt.figure(figsize=(10,6))
sns.histplot(x=log_energy,kde= True)
plt.title("Log tranformed energy value in (Kcal)")
plt.show()


# In[25]:


from scipy.stats import ttest_ind
# hypothesis Testing 
Category_1 = data[data["Menu Items"]=='Burger']["Energy (kCal)"]
Category_2 = data[data["Menu Items"]=='Salads']['Energy (kCal)']

# Check if both have data points
if not Category_1.empty and not Category_2.empty:
    # Perform t-test
    t_stat, p_value_t = ttest_ind(Category_1,Category_2)
    print(f"T-Test: t_stat = {t_stat}, p_value = {p_value_t}")
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Menu Category', y='Energy (kCal)', data=data[data['Menu Category'].isin(['Burgers', 'Salads'])])
    plt.title('Boxplot of Energy Content for Burgers and Salads')
    plt.show()
else:
    print("One or both categories have no data points. Unable to perform tests.")


# In[26]:


# Correlation Analysis
numeric_col = data[data.select_dtypes(include=['float64','int64']).columns]
correlation_matrix = numeric_col.corr()
print(correlation_matrix)

plt.figure(figsize=(10,8))
sns.heatmap(correlation_matrix, annot= True , cmap='coolwarm', fmt='.2f')
plt.title("Correlation analysis using Heatmap")
plt.show()


# In[27]:


# average nutrition value
data['per serve size (g)'] = data['Per Serve Size'].str.extract('(\d+)').astype(float)
data['per serve size (g)']
data.drop(columns=['Per Serve Size'],inplace = True)


# In[28]:


# highest Energy (Kcal) item in the menu
high_Kcal = data[data['Energy (kCal)']== data['Energy (kCal)'].max()]['Menu Items'].values[0]
print("The menu item with higest Energy:",high_Kcal)


# In[29]:


# Distribution of total carbohydrates across the Menu Items
plt.figure(figsize=(10,8))
plt.hist(data["Total carbohydrate (g)"],bins=20,color= 'Purple',edgecolor='white')
plt.title("Distribution of Crabohydrates in (g)")
plt.xlabel("Total carbohydrate (g)")
plt.ylabel("Frequency")
plt.show()


# In[30]:


# what is the average protein content for menu category
avg_pro_by_cat= data.groupby("Menu Category")["Protein (g)"].mean()
print("The average protein content for menu category:",avg_pro_by_cat)


# In[31]:


# which category has the highest energy content ?
hig_energy_content = data.groupby('Menu Category')['Energy (kCal)'].mean().idxmax()
print("The Category with highest energy content is:",hig_energy_content)


# In[32]:


# Correlation between Total Fat and Protein
Corr=data['Protein (g)'].corr(data['Total fat (g)'])
print("Correlation between Total Fat and Protein:",Corr)


# In[33]:


# Distribution of calorie values across menu items 
print(data['Energy (kCal)'].describe())
plt.figure(figsize=(10,8))
plt.hist(data['Energy (kCal)'],bins=20,color="Pink",edgecolor='Black')
plt.title("Distribution of Calories")
plt.xlabel("Energy (kCal)")
plt.ylabel("Frequency")
plt.show()


# In[34]:


# Distribution of Protein Content
plt.figure(figsize=(10,8))
plt.hist(data['Protein (g)'],bins=20,color='green',edgecolor='white')
plt.title("Distribution of Protein (g)")
plt.xlabel("Protein (g)")
plt.ylabel("Frequency")
plt.show()


# In[35]:


# Distribution of Total Fat Content
plt.figure(figsize=(10,8))
plt.hist(data['Total fat (g)'],bins=20,color='red',edgecolor='white')
plt.title("Distribution of Total Fat (g)")
plt.xlabel("Total Fat (g)")
plt.ylabel("Frequency")
plt.show()


# In[36]:


data


# In[37]:


# comparing the nutritional content of different menu categories
plt.figure(figsize=(12,10))
sns.boxplot(x=data['Menu Category'],y=data['per serve size (g)'])
plt.title("Nutritional Content of different Menu Category")
plt.show()


# In[38]:


# sodium content vary across menu categories
plt.figure(figsize=(12,10))
sns.boxplot(x=data['Menu Category'],y=data['Sodium (mg)'])
plt.title("Distribution of Sodium over Menu Category")


# In[39]:


# the distribution of calories for different menu categories
plt.figure(figsize=(12,10))
sns.violinplot(x=data['Menu Category'],y=data['Energy (kCal)'])
plt.title("Nutritional Content of different Menu Category")
plt.show()


# In[64]:


# How do the distribution of menu items with low calorie content compare to those with high calorie content.
# What conclusions can we draw for health-conscious individuals
low_calorie_threshold=300
high_calorie_threshold=600

low_calorie_item = data[data['Energy (kCal)']<low_calorie_threshold].shape[0]
high_calorie_item = data[data['Energy (kCal)']>high_calorie_threshold].shape[0]
avg_calorie_item = data[(data['Energy (kCal)']>low_calorie_threshold) & (data['Energy (kCal)']<high_calorie_threshold)].shape[0]

labels=['Low Calorie','High Calorie','Avg calorie']
sizes=[low_calorie_item,high_calorie_item,avg_calorie_item]
colors=['green','red','yellow']

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=207,shadow=True)
plt.title('Distribution of Low and High Calorie Items')
plt.legend(loc='best')
plt.axis('equal')

if low_calorie_item > high_calorie_item:
    conclusion="There are more menu items with low calorie content, which is beneficial for health-conscious individuals."
elif high_calorie_item > low_calorie_item:
    conclusion="There are more menu items with high calorie content, indicating a need for more low-calorie options beneficial for health-conscious individuals."
else:
    conclusion="There is a balanced distribution of menu items with low and high calorie content."

plt.text(0.5, -1.2, conclusion, ha='center', va='center', fontsize=12,fontweight='bold', color='blue')
plt.show()



# In[93]:


# Which menu category offers the highest proportion of items with low total fat content (considering items with less than 10g of total fat as ‘low’)? 
# How can this information guide individuals towards healthier menu options.
Low_total_fat_threshold = 10
low_fat_Items = data[data['Total fat (g)']<Low_total_fat_threshold]
category_low_portion = low_fat_Items.groupby('Menu Category').size()/data.groupby('Menu Category').size()
Healthiest_Category= category_low_portion.idxmax()

plt.figure(figsize=(10,6))
plt.bar(category_low_portion.index,category_low_portion.values,color='lightgreen')
plt.title('Proportion of Low Total Fat Items by Menu Category')
plt.xlabel('Menu Category')
plt.ylabel('Proportion of Low fat Items')
plt.xticks(rotation=90)
plt.tight_layout()

conclusion = f"The '{Healthiest_Category}' category offers the highest proportion of items with low total fat content, making it a healthier choice for individuals concerned about fat intake."
plt.text(0.5, -0.6, conclusion, ha='center', va='center', fontsize=12,fontweight='bold', color='green')
plt.show()

