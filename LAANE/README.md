# LA Alliance for a New Economy, Housing Project (AKA LAANE)
This repository is for the data cleaning portion of the Hack For LA + LAANE project. The project assists the Nonprofit LAANE by joining multiple data sources into a sqlite database.

## Installation
Use the requirements file to create the proper environment to run the project.

## Usage
There are multiple scripts in the processing folder. Each script is either a single file or multiple file processing scripts. Below are the arguments that are necessary to each type. After filling out the arguments, you run the python file in the `python file_name.py` format. 
```python
# if it's a single file
# fill out the arguments below
function(
    filepath='/home/LAANE/Assessor data/CSV/part1/firstfile.csv/, # File path.
    session=SessionLocal(), # SQL Alchemy session object.
)

# if it's a script that processes multiple files.
# Fill out the arguments below 
multiple_files(
    filepath='/home/LAANE/Assessor data/CSV/part1', # Folder path
    filetype='csv', # The file ending for example csv.
    process_function=process_assessor, # The main processing function.
    session=SessionLocal(), # SQL Alchemy session object.
)

```
## Folder Layout:
### database
Has the code for connecting to SQL Alchemy. 

### outdated
Outdated methods and analysis before ERD were complete. 

### processingscripts
The scripts for each dataset. 

### supplementarymaterial
Extra material such as ERD and Data Dictionary.

### test
tests for functions

### transformations
This folder holds files that help multiple processing scripts.

## List of datasets to maintain
* Assessor table - almost never
* Builds table - almost never
* Mailing table - almost never
* Categorically ineligible table - 1-2 times per year
* Exempt table - 1-2 times per year
* TOT table - almost never
* Warnings table - frequent
* Citation table - frequent
* Recipient table [This seems to be of a piece with the warnings & citation tables]
* Noncompliant list - frequent
* Complaints table - 1-2 times per year
* HSO registrant table (& associated) - frequent
* City of LA hosting platform table - 1-2 times per year
* Airbnb table (& associated) - frequent

## TODO:
Below are some things that I would have liked to do but don't have time for at this moment. These are a great starting point for someone else to continue with the project.
* write data dict
* create a requirements file
* create a mock database to test the inserts and sql alchemy.

## License
LAANE Project uses the GNU AFFERO GENERAL PUBLIC LICENSE.
See the COPYING.txt file.
