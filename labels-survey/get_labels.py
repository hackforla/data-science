import os
from dotenv import load_dotenv
from repos import *
load_dotenv()



organizations = ['hackforla', '100automations', 'civictechindex', 'civictechstructure', 'hackla-engage'] # suggested orgs: 'hackforla', '100automations', 'civictechindex',
# 'civictechstructure', 'hackla-engage'
token = os.getenv("TOKEN")
username = os.getenv("USERNAME")
csv_filename = 'output.csv'
state = 'all'

authenticate(username, token) # Just to verify token and username are OK


for organization in organizations:
    my_repos = Repo(organization, token, csv_filename)
    my_repos.get_repo_names()
    for repo in my_repos.repos:
        my_repos.get_issues(organization, repo, state)