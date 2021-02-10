## ETL-project
SmartMilk

### Kroger Folder 

The Kroger folder contains all Kroger Milk Price and Location data used in our SmartMilk program

Our Notebook files are using the Python "Request" module to draw location and product information from the Kroger API Developers reference (see https://developer.kroger.com/# for futher details on the process)  The api endpoints referenced were:  

https://api.kroger.com/v1/products  
https://api.kroger.com/v1/locations

A free account was established and once we registered an application, we were provided with an individual "Secret" code.

When wanting to retrieve data, the secret code is submitted in an an authorization request. The authorization request returns a Token key which is used to permit the API get command to draw the requested information. 

The token key expires after 30 minutes and a new one must be generated to continue data runs.

Separate API requests were prepared to gather location and product information. The data search filtered on term "milk" to find products containing the word "milk" anywhere in its description. 

The product api had a max limit per page of 50 so a "get_milk_price" function was built with a while loop stacking the 50 responses and resetting the start point on the next run to start +=50. 

The max records allowed for a product api run was 1000, so the "get_milk_price" funtion was coded to stop after 20 passes (20*50 = 1000).   

1000 records allowed for a complete run on dairy related milk products. The search feature appears to take relavance into consideration as we noted after 4 to 5 hundred "dairy" related responses, products containing the work "milk" went on to dog biscuits (Milk bones), candy (Milk Chocolate), and comsmetics (milk shampoos). For the purpose of our exercise, non dairy "milk" termed products are being excluded.  

The location api allowed for a search-near zip code filter so center of Houston zip code 77002 was used to find stores within a radius of 50 miles of that code. The record limit of this api is 200 so no paging or looping was required. 

The api's search filter for Brand (Kroger, Shell, ect) was disabled, so our query run was excessively loaded with Shell location data and only contain 21 Kroger sites. We put in a ticket with the Kroger Developers page to look into the filter issue. 

As we've opted not to include zipcode searching at this stage in our project, we've left the location search work as a placeholder for potential future development. 

For product and location APIs, we used pd.json_normalize to draw out and de-nest the JSON formatted results received. The dataframes were then converted to CSV format (df.to_csv) and saved to be used in our database.

### Notebook File: Kroger_locations.ipynb

#### Api authorization and run scripts to generate:

JSON display within the file - milk_location

Pandas Dataframe showing only required fields - df

CSV output of Pandas Dataframe - kroger_locations.csv


### Notebook File: Kroger_milk_get_price.ipynb

#### Content: Api authorization and run scripts to generate:

JSON display within the file - milk_price_list

Pandas Dataframe showing only required fields - df

CSV output of Pandas Dataframe - kroger_milk_prices.csv


