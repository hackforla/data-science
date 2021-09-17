### Temp folder for LAANE project

## TODO:
* write data dict
* insert ERD into docs
    * ERD Needs to be updated to match builds changes
* create a requirements file
* create a mock database to test the inserts
* write a process for each file type that will need to be added to the database
* Process:
    - each file will have it's own custom file so that we can run it sperately, we can also do all of them on the main (?)
   - Each file will contain custom code for that data source if there is no transformation file for that data source it means that little to no normalization is needed and it can be handled in the main program main program will open the files and process them and enter them into the sqlite db
main will be the only executable file as of right now.Main will also need to dedup data before processing to minimize any duplication in database

## Misc scripting notes:
    - one fine stay data doesn't work with pandas as excel files, first needs to convert to csv

### Notes about the normalize module
In some cases it can't figure it out but it'll save the entire address to address1 which is fine, it's mainly an issue with PO boxes but that's only secondary data.
