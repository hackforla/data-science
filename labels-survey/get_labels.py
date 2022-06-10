from repos import *

organizations = ['YOUR ORGANIZATIONS HERE'] #suggested orgs: 'hackforla', '100automations', 'civictechindex', 'civictechstructure', 'hackla-engage'
token = 'YOUR GITHUB TOKEN HERE'
username = 'YOUR GITHUB USERNAME HERE'
csv_filename = 'output.csv' #suggested filename is output.csv

authenticate(username, token) # Just to verify token and username are OK

create_csv(csv_filename) # Creates csv file with headers

for organization in organizations:
    my_repos = Repo(organization, token, csv_filename)
    my_repos.get_repo_names()
    for repo in my_repos.repos:
        my_repos.get_issues(organization, repo)
        for issue in my_repos.issues:
            my_repos.get_labels(organization, repo, issue)
            print(repo, issue, my_repos.labels)

