# ETL-project
SmartMilk Database Design

For this project a structured SQL database was used collecting all of the milk products for Kroger and HEB websites. A structured database was preferable for this project because the data was scraped into the same format for each grocery store. The database was created using Postgresql using the schema.sql file. An ERD diagram for the database was designed with 4 tables. The main table Milk contains all of the milk attributes and is tied to 3 separate tables. A Store table contains all of the information regarding different store information for both Kroger and HEB. Currently, only one store for each is in the database, but for future upgrades to this system more stores and different chains will be added to this table. The Milk_Type table contains the different types of milk present in the database (2%, 1%, skim, whole, almond, etc.). The final table is a Price_History table that ties to the Milk table based on a created product ID. This table will allow for keeping a price record of the milk products over time for further analysis.


In order to accomplish this a new pandas dataframe was created to match the data structure for each Postgresql table. Python was then used to push the data into the database. When a new data insert is run the an updated dataframe created and checked against a dataframe created from the database table. This is then used to eliminate matches in the dataframes and the unique values are then inserted into the database thus preventing duplicate insertion of the same item.

