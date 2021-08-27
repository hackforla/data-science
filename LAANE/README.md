### Temp folder for LAANE project

## TODO:
* write data dict
* insert ERD into docs
* create a requirements file
* Process:
    - each file will have it's own custom file so that we can run it sperately, we can also do all of them on the main (?)
   - Each file will contain custom code for that data source if there is no transformation file for that data source it means that little to no normalization is needed and it can be handled in the main program main program will open the files and process them and enter them into the sqlite db
main will be the only executable file as of right now.Main will also need to dedup data before processing to minimize any duplication in database

## Notes on how to use normalize_address module
### Below are some notes for how to use normalize_address for the project since it's replacing a lot of custom code.
* **tot** TOT_df[['Address1','Address2']]=[itemgetter('address_line_1','address_line_2')(normalize_address_wrapper(x)) for x in TOT_df['STREET_ADDRESS'].tolist()]
* **exempt** exempt_df import re normalize_address_wrapper(re.sub('^0+','', '08800 S BROADWAY                        '))
* **assessor** see below

```
# Possible way to use the normalize function in assessor/mailing
# rewrite this to optimize it (remove all strs) 
df["Mailing Full"] = (df['Mail House No'].astype(str)
                      .str.cat(df['M Fraction'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['M Unit'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['M Direction'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['M Street Name'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['M City State'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['M Zip'].astype(str).str[:5], sep=" ", na_rep="")
                      .str.strip()
                     )

df['Mailing Full']
# then use see the tot above to seperate

# Same example but for assessorr not mailing address:
df['address full'] = (df['Situs House No'].astype(str)
                      .str.cat(df['Fraction'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['Unit'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['Direction'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['Street Name'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['City State'].str.strip(), sep=" ", na_rep="")
                      .str.cat(df['Zip'].astype(str).str[:5], sep=" ", na_rep="")
                      .str.strip()
                     )
df['address full']
running the code:
PYTHONPATH="$PWD/" python transformations/hso_denials.py
```

### Notes about the normalize module
In some cases it can't figure it out but it'll save the entire address to address1 which is fine, it's mainly an issue with PO boxes but that's only secondary data.

### break up large files:

```
# read excel files usecol option
# process files into 10 files

    for idx, chunk in enumerate(np.array_split(assesor_df, 10)):
        chunk.to_csv("CSVprocessed/DSO43_{0}.csv".format(idx))
```
