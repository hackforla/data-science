# Tech stacks

The docker container will output 
    1. A json with tech stacks of websites for the NC survey.
    2. A csv pivot table showing websites in columns and techs in rows 

 
JSON Format:

[ ..., {"url": NC survey website, "tech": tech from the url , "href": builtwith link with stats on tech }, ... ]

Find the CSV on [google sheets](https://docs.google.com/spreadsheets/d/1oOBfaKLSQAeOB4V7gwjQYyeOdz6a5IBmkH_Lr2Kzn40/edit?usp=sharing)

## Commands:
```
docker build -t selenium_image .

docker container  run -it --name selenium_container selenium_image

docker cp selenium_container:/app/data.json data.json

docker cp selenium_container:/app/tech_table.csv tech_table.csv
```