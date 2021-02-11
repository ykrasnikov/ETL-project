#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
from sqlalchemy import create_engine


# ### Store CSV into DataFrame

# In[93]:


from secrets import username, password


# Read in and put into a database the Kroger products

# In[94]:


csv_file = "../kroger/kroger_milk_prices.csv"
kroger_data_df = pd.read_csv(csv_file)
#kroger_data_df.head()


# Read in and put into a database HEB Products

# In[95]:


path = "../data/heb_clean.csv"
heb_data_df = pd.read_csv(path)
heb_milk = heb_data_df.drop(columns=['coupon', 'name' , 'price', 'uomSalePrice', 'simple_type'])
milk_type_file = "../data/heb_milk_vs_types.csv"
milk_type_df = pd.read_csv(milk_type_file)
heb_milk = heb_milk.merge(milk_type_df, on = 'id')
heb_milk = heb_milk.rename(columns= {'id':'product_id' , 'brand' : 'Brand'})
heb_milk['Store_Number'] = 1111111
today = pd.datetime.now().date()
heb_data_df['Date'] = today
#heb_data_df.head()
heb_milk = heb_milk.drop(columns = ['type_x','types'])
heb_milk = heb_milk.rename(columns = {'type_y' : 'type'})
#heb_milk


# Create dataframe to match Milk database table. Merge HEB and Kroger milk dataframes.

# In[96]:


milk_df = kroger_data_df
milk_df = milk_df.drop(columns=['Unnamed: 0', 'description' , 'price.regular', 'price.promo', 'Date'])
features = 'none'
milk_df['features'] = features
kroger_milk_type_file = "../data/kroger_milk_vs_types.csv"
kroger_milk_type_df = pd.read_csv(kroger_milk_type_file)
kroger_milk_type_df = kroger_milk_type_df.rename(columns = {'id' : 'productId'})
milk_df = milk_df.merge(kroger_milk_type_df, on = 'productId')
milk_df = milk_df.drop(columns=['types'])
milk_df = milk_df.rename(columns={"productId": "product_id", "brand": "Brand" , "categories" : "category" , 'Store_Id' : 'Store_Number'})
complete_milk = pd.concat([milk_df, heb_milk])
#complete_milk


# Create and populate Store dataframe for Store database table. Will be automated once more stores are added in future itterations of project.

# In[97]:


store_df = pd.DataFrame()
store_id = 3400312 , 1111111
store_df["Store_Number"] = store_id
zipcode = 77007 , 77007
store_df['Store_Zipcode'] = zipcode
name = "Kroger" , "HEB"
store_df['Store_Name'] = name
#store_df.head()


# In[ ]:





# Read in and create dataframe for milk types. Formatted for database table.
# 
# 

# In[98]:


milk_type_file = "../data/milk_types.csv"
milk_type_df = pd.read_csv(milk_type_file)
milk_type_df['Full_Name'] = 'Almond-Milk' , 'Chocolate-Milk', 'Reduced-Fat-Milk', 'Lactose-Free-Milk', 'Oat-Milk', 'Organic-Milk', 'Other', 'Powder-Milk', 'Protein-Product' , 'Whole'
milk_type_df = milk_type_df.rename(columns={'count_id' : 'count'})
#milk_type_df


# In[ ]:





# ### Connect to local database

# In[99]:


rds_connection_string = f"{username}:{password}@localhost:5432/milk_db"
engine = create_engine(f'postgresql://{rds_connection_string}')


# ### Check for tables

# In[100]:


engine.table_names()


# Use drop duplicates to only add updated data to a dataframe that is then loaded into the database

# In[101]:


temp_store = pd.read_sql_query('select * from "Store"', con=engine)
temp_store = temp_store.drop(columns = 'id')
#temp_store


# In[102]:


db_store = pd.concat([temp_store, store_df]).drop_duplicates(keep=False)
db_store = db_store.reset_index(drop=True)   
#db_store.head()


# ### Use pandas to load csv converted DataFrame into database

# In[103]:


db_store.to_sql(name='Store', con=engine, if_exists='append', index=False)


# ### Confirm data has been added by querying the customer_name table
# * NOTE: can also check using pgAdmin

# In[104]:


pd.read_sql_query('select * from "Store"', con=engine).head()


# Same process as above for store table is followed for milk type.

# In[105]:


temp_type = pd.read_sql_query('select * from "Milk_Type"', con=engine)
temp_type = temp_type.drop(columns = 'id')
db_type = pd.concat([temp_type, milk_type_df]).drop_duplicates(keep=False)
db_type = db_type.reset_index(drop=True)   
#db_type


# In[106]:


db_type.to_sql(name='Milk_Type', con=engine, if_exists='append', index=False)


# ### Confirm data has been added by querying the customer_location table

# In[107]:


pd.read_sql_query('select * from "Milk_Type"', con=engine)


# Retrieves and merges Store data with milk data to set the Store ID then next cell deletes data not required in Milk Table

# In[108]:


stores2_df = pd.read_sql_query('select * from "Store"', con=engine).head()
complete_milk = complete_milk.merge(stores2_df, on = 'Store_Number')
#complete_milk.head()


# In[109]:


complete_milk = complete_milk.drop(columns = ['Store_Name' , 'Store_Zipcode', 'Store_Number'])
#complete_milk.head()


# In[110]:


complete_milk = complete_milk.rename(columns ={'id' : 'Store_ID'})
#complete_milk.head()


# In[111]:


type2_df =pd.read_sql_query('select * from "Milk_Type"', con=engine)
type2_df = type2_df.drop(columns = ['Full_Name' , 'count'])
complete_milk = complete_milk.merge(type2_df, on = 'type')
complete_milk = complete_milk.drop(columns = {'type' })
complete_milk = complete_milk.rename(columns = {'id' : 'Type_ID'})
#complete_milk


# Same process as above is followed to insert Milk data from dataframe into Milk table of database

# In[112]:


temp_milk = pd.read_sql_query('select * from "Milk"', con=engine)
temp_milk = temp_milk.drop(columns = 'id')
#temp_milk


# In[113]:


db_milk = pd.concat([temp_milk, complete_milk]).drop_duplicates(keep=False)
db_milk = db_milk.reset_index(drop=True)   
#db_milk.head()


# In[114]:


db_milk.to_sql(name='Milk', con=engine, if_exists='append', index=False)


# In[115]:


pd.read_sql_query('select * from "Milk"', con=engine)


# Milk data is pulled from database Milk table and merged with price history. Uneeded price history columns are dropped and renamed to coordinate with Price History Table. This sets the product ID in price history.

# In[ ]:





# In[116]:


price_history_df = kroger_data_df[['Date', 'price.regular', 'price.promo', 'productId']].copy()
heb_price = heb_data_df[['price' , 'coupon', 'id', 'Date']]
heb_price =heb_price.rename(columns={'Date':'date', 'coupon':'saleprice', 'id':'product_id'})
price_history_df =price_history_df.rename(columns={'Date':'date', 'price.regular':'price', 'price.promo':'saleprice', 'productId': 'product_id'})
price_history_df = pd.concat([price_history_df, heb_price])
price_history_df['date'] = pd.to_datetime(price_history_df['date'])
#price_history_df


# In[117]:


milk2_df = pd.read_sql_query('select * from "Milk"', con=engine)
milk2_df = milk2_df.drop(columns = ['Brand' , 'size', 'image', 'Store_ID', 'Type_ID', 'category', 'features', 'name'])
merged_price = price_history_df.merge(milk2_df, on = 'product_id')
#merged_price


# In[118]:


merged_price = merged_price.drop(columns = ['product_id'])
merged_price = merged_price.rename(columns = {'id' : 'product_id'})
#merged_price


# Price History Dataframe is then added to Price History Table. Duplicates are not checked for in this instance because duplicates will trigger an error and stop the update process. 

# In[119]:


temp_history = pd.read_sql_query('select * from "Price_History"', con=engine)
db_history = pd.concat([temp_history, merged_price]).drop_duplicates(keep=False)
db_history = db_history.reset_index(drop=True)   
#db_history


# In[120]:


db_history.to_sql(name='Price_History', con=engine, if_exists='append', index=False)


# In[121]:


pd.read_sql_query('select * from "Price_History"', con=engine)


# In[ ]:





# In[ ]:




