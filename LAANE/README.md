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
    filepath='/home/LAANE/Assessor data/CSV/part1/firstfile.csv/', # File path.
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
Has the code for connecting to SQLite db with SQL Alchemy. 

### outdated
Outdated methods and analysis before ERD were complete. 
(should be deleted after analysis begins.)

### processingscripts
The scripts for each dataset. 

### supplementarymaterial
Extra material such as ERD and Data Dictionary.

### test
Unit tests.

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
## SAMPLE USE CASES
* For a given address, comparing name (per assessor) with name (per HSO registration)
* Is a given listing (from Airbnb scrape) on any other platforms?
* When did a listing enter the universe? Any notable changes over time?
* When did a registrant enter the universe? Any notable changes over time?
* Is any registered address on the ineligible or prohibited lists?
* Has there been any enforcement action taken against a given host and/or address?
* Can we match registrations to scrape listings and/or to hosts?
* Can we match complaint and/or enforcement data to scrape listings?
* Can we overlay shape files (to code an address by council district, congressional district, etc.)?
* For a given name, does the person have a registration? Has enforcement action been taken against the person? Does the person have a TOT payer account?
* I will often want to run a search/match on a defined subset of data by idiosyncratic, on-the-fly criteria. E.g., ‘limit a search to entire-home-listings by hosts-with-more-than-one-listing’ (a likely example, as those are common markers of commercial activity)

## TODO:
Below are some things that I would have liked to do but don't have time for at this moment. These are a great starting point for someone else to continue with the project.
* write some SQL queries for LAANE to start with for their analysis
* help set up the scripts for LAANE
* write data dict
* create a mock database to test the inserts and sql alchemy.
* plenty of room for refactoring.

## License
LAANE Project uses the GNU AFFERO GENERAL PUBLIC LICENSE.
See the COPYING.txt file.
