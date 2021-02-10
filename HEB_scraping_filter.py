#!/usr/bin/env python
# coding: utf-8

# In[1]:


###########################################


# In[2]:


############ Import libraries


# In[3]:


from bs4 import BeautifulSoup as bs 
import pandas as pd
import re
from selenium import webdriver 
import time


# In[5]:


#####################################################
################ utility function
def return_string(string, start_after_word,stop_before_word):
    """return part of string between 2 words     (string, start_after_word,stop_befor_word)"""
    try:
        if start_after_word=="":
            start_address=0
        else:
            start_address=re.search(start_after_word,string).span()[1]
        #print(start_address)
        if stop_before_word=="":
            stop_address=len(string)
        else:
            stop_address=re.search(stop_before_word,string).span()[0]
        #print(stop_address)
        my_string=string[start_address:stop_address]
    except Exception as e:
        # handle error
        error=f"STRING _exception_: {type(e).__name__},</br> _arguments_: {e.args}"
        #print(error)
        my_string=None
    return my_string


# In[7]:


####################################################
###############filter function 
def heb_filter(soup_find):
    """ function takes result of HEB scraping - soup.find_all and
    transforms it to dataframe """
    my_result=soup_find
    scrap_df=pd.DataFrame()
    try:
#       my_result=soup.body.find_all('a',id=re.compile('product-'))
       
        i=0
        for record in my_result:
            name=record.find('span',class_=re.compile('responsive')).text.strip()
            size=return_string(name,"Milk","")
            json=eval(record.find('script',type="application/ld+json").string)
            id=json['id']
            brand=json['brand']
            category=json['category']
            price=json['price']
            search_string=record['aria-label'].strip()
            features=return_string(search_string,"Features:","")
         #  rating=return_string(search_string,"Rated","stars")
            uomSalePrice=record.find('span',class_=re.compile('uomSalePrice')).text.strip()
            image=record.find('img',attrs={"data-src":re.compile('prd-small')})['data-src']
            if record.find('img',src=re.compile('coupon'))==None:
                coupon=0
            else:
                coupon=1
            #debug prints
            #print(i) 
            #print (f'{name} \n{size}\n{json}\n{id}\n{brand}\n{category}\n{price}\n{features}\n{coupon}\n{uomSalePrice}\n{image}')
            #print('___________________')
            i+=1
            scrap_df = scrap_df.append({'id':id,
                                'name': name,
                                'brand':brand,
                                'size':size,
                                'category':category,
                                'price':price,
                                'features':features,
                                'coupon':coupon,
                                'uomSalePrice':uomSalePrice,
                                'image':image,
                               }, ignore_index=True)
        null_df=scrap_df[scrap_df.isna().any(axis=1)]
    except Exception as e:
        # handle error
        print (f'{name} \n{size}\n{json}\n{id}\n{brand}\n{category}\n{price}\n{features}\n{coupon}\n{uomSalePrice}\n{image}')
        error=f"_exception_: {type(e).__name__},</br> _arguments_: {e.args}"
        print(error)
        
    return scrap_df
    
    
    


# In[ ]:




