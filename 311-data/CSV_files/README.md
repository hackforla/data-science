README:

## 311 Data Cleaning \& Hosting Project

### Overview

This project provides a reproducible pipeline for processing the large 311 Service Request dataset. The pipeline downloads, cleans, and splits the data into smaller, manageable files, making it easier to work with in local or in-browser environments.

For background, methodology, and details on how to use Google Colab instead of this repo, please see the \[Project Wiki](https://github.com/hackforla/data-science/wiki/311-Data-Cleaning-\&-Hosting-Overview)

### Repository Contents

- 311\_data\_cleaning.ipynb – Jupyter Notebook for acquisition, cleaning, and splitting

- CSV\_files/Docs/CleaningRules.txt – Documentation of cleaning rules

- README.md – This file.

### How to Use

#### Run Locally

<!-- Forking ensures you can make changes and contribute back via Pull Requests -->



-  Fork this repository on GitHub.  



-  Clone your forked copy:

```

git clone https://github.com/<your-username>/data-science.git   # clone your fork


```

```

cd data-science/311-data        # move into 311-data folder

```

-   Open the Jupyter Notebook

    -  311-data/CSV\_files

    -  jupyter notebook 311\_data\_cleaning.ipynb

-  Run the notebook

   -  Download raw 311 Service Request data (provide open data URL for the desired year).

   -  Apply cleaning rules by running the notebook

   -  Automatically split and save the dataset into monthly files

  

OR

#### Run in Google Colab

Use the hosted notebook (no fork or download required):

-   \[Open in Colab](https://colab.research.google.com/drive/1\_HFqnSOIDqDCtF3jmslmzkZ82eho10lY?usp=sharing)

### References

- \[Project Wiki](https://github.com/hackforla/data-science/wiki/311-Data-Cleaning-\&-Hosting-Overview)

- \[Documentation of cleaning rules](https://github.com/hackforla/data-science/blob/main/311-data/CSV\_files/Docs/CleaningRules.txt)

- GitHub Tutorials

&nbsp;  -  https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo


