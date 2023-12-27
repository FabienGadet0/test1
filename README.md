## CSV input

I got this csv from Kaggle : https://www.kaggle.com/code/sinaasappel/ecommerce-data-exploration-and-visualization/input
It has duplicates on purpose so i was thinking it would be a good example .

## Duplicates handling

I handle duplicates :

- Set constraints in the tables , such as a superkey
- the json table has a "processed" column that is set to true when processed to avoid reprocessing it .
-

## Procedure

I chose to execute the procedure using a small python script since i assume that you are using a dag system and it will be a lot easier to track any step throught a dag than directly in the database with for example a trigger.

if we wanna make it run every day at 5 am for example we can set the pg_cron to:

```sql
SELECT cron.schedule('0 5 * * *', $$ CALL raw_json_to_parsed_product(); $$);
```

## Environment

Variables are in environment , if you download it you will have dummy values in a .env that will be loaded to each scripts  
in github i setup those variables as secrets as well , for the purpose of the exercise it's the same values but of course in a production environment it wouldn't be.

## Potential upgrade in the future

Use DBT for the whole sql pipeline.
