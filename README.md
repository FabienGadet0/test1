# Installation

## Prerequisites

### Install Docker

If you don't have Docker installed, you can follow the official Docker installation guide for your operating system.

## Run it

Since there are 2 containers and the database need to initialize first i suggest to not run everything in one time but in two like this :

```
docker-compose up db
```

And in a separate terminal :

```
docker-compose up pipeline
```

## Connect to the database

Once docker-compose is running you can exec in a new terminal `psql` in the db container to query what you want , just run this
it will prompt for a password , the default password is `pwd`

```

docker exec -it rehub-db-1 psql -h localhost -U user -d production -W

```

# Explanations

## Basic overview

Every parts except the views are python scripts that can all be executed all at once using `poetry run pipeline` (which is what the pipeline docker container do)

- unzip()  
  Unzip the input zip file to csv

- convert_to_json()  
  Convert the csv file to a json format

- load_to_db()  
  Load the json file to the database

- call_procedure()
  Call the procedure called `raw_json_to_parsed_product()` that handle the json in `landing.raw_products` and extract it to `public.raw_parsed_products`

![Alt text](pipeline.png)

## CSV input

I got this csv from Kaggle : https://www.kaggle.com/code/sinaasappel/ecommerce-data-exploration-and-visualization/input
It has duplicates on purpose so i was thinking it would be a good example .

The content is as following :

| Column      | Type      | Example                              |
| ----------- | --------- | ------------------------------------ |
| InvoiceNo   | VARCHAR   | "536365"                             |
| StockCode   | VARCHAR   | "85123A"                             |
| Description | VARCHAR   | "WHITE HANGING HEART T-LIGHT HOLDER" |
| Quantity    | INTEGER   | 6                                    |
| InvoiceDate | TIMESTAMP | "12/1/2010 8:26"                     |
| UnitPrice   | DECIMAL   | 2.55                                 |
| CustomerID  | INTEGER   | 17850                                |
| Country     | VARCHAR   | "United Kingdom"                     |

## Duplicates handling

I handled duplicates using the following:

- I set a superkey constraint to the columns : `invoice_date`, `description`, `quantity`, `invoice_no`
- the json table has a `processed` column that is set to true when processed to avoid reprocessing it.

## Procedure

I chose to execute the procedure using a small python script since i assume that you are using a dag system and it will be a lot easier to track any step throught a dag than directly in the database with for example a trigger.
if we wanna make it run every day at 5 am for example we can set the pg_cron to:

```sql
SELECT cron.schedule('0 5 * * *', $$ CALL raw_json_to_parsed_product(); $$);
```

## Environment

In the context of a production pipeline we would use environment or secret file or github secrets to handle the variables  
Here for the sake of simplicity i just wrote it directly in the corresponding Dockerfiles

## Potential upgrade in the future

- Use DBT for the whole sql pipeline.
- Use a dag system
