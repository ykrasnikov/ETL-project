# ETL-project

# SmartMilk


<img src="images/data-lake.gif"  align="right" width="70%"/>

<img src="https://www.kroger.com/product/images/large/front/0019181735007" align="center" width="24%"/>


<br> </br>

_______________________
<br> </br>

## 1.1 Scrape Kroger milk API 

[Kroger_location scrape code](kroger/kroger_locations.ipynb)

[Kroger_milk scrape code](kroger/kroger_milk_get_price.ipynb)

__________________________
## 1.2 Scrape HEB webpages

[HEB scrape code](NEW _scraping_HEB.ipynb)

_________________________
## 2. Stage area filters

[HEB filter](staging_area/filters_HEB.ipynb)

[Kroger filter](staging_area/filters_kroger.ipynb)

[Cleaned CSVs](data/)

____________________________

## 3. Database

[ERD diagram](database/ERD.ipynb)

[Database schema](database/schema.sql)

[DATA insertion](database/data_etl.ipynb)

[DATA check query](database/Check_database_insertion.ipynb)

_________________________________
For our group ETL project we’d like to look at the price of milk at different stores in different zip codes.


From Kroger and HEB websites we’’ll be building a relational database using the following fields:
zip code
price
size (based on name in HEB website)
name
(type based on name)
(brand based on name)


We’ll be building a structured database in SQL.

Kroger has its own API that we can use to build a database for their products but HEB does not so we’ll be using scraping to build a database of their products.

Data cleanup will include string manipulation to determine type and brand (and for HEB the amount) of each product.

Charles will be using the Kroger API to build the Kroger database.
Alex will be scraping the HEB website and set up the GitHub.
Jacob will handle string manipulation to clean up the HEB results.
Justin will take care of building the database and the ERD.

For HEB the first file is NEW_scraping_HEB.ipynb. Next is the kroger_locations.ipynb file, and then kroger_get_milk_prices.ipynb. These generate the csv files used in the filter notebooks in the staging_area directory. After that csv's are saved in the data folder and used to build the database.
Next the ERD diagram in the database folder. The next file for creating the schema of the database and populating the database is data_etl.ipynb.