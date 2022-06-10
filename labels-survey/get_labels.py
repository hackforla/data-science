from repos import *

organizations = ['YOUR ORGANIZATIONS HERE'] #suggested orgs: 'hackforla', '100automations', 'civictechindex', 'civictechstructure', 'hackla-engage'
token = 'YOUR GITHUB TOKEN HERE'
username = 'YOUR GITHUB USERNAME HERE'
csv_filename = 'output.csv' #suggested filename is output.csv
state = 'open' #status of the issues. Values are open, closed or all

authenticate(username, token) # Just to verify token and username are OK



for organization in organizations:
    my_repos = Repo(organization, token, csv_filename)
    my_repos.get_repo_names()
    for repo in my_repos.repos:
        my_repos.get_issues(organization, repo, state)