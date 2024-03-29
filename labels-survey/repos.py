import requests
import json
import csv


def authenticate(username, token):
    """Can be used to validate GitHub API credentials"""
    response = requests.get('https://api.github.com/users/octocat', auth=(username, token))
    if response.status_code == 200:
        print("Authentication OK")
    else:
        print("Authentication Error. Code " + str(response.status_code))


def create_csv(csv_filename):
    csv_headers = ['Organization', 'Repository', 'IssueNbr', 'LabelName', 'LabelDescription', 'LabelDefaultTag', 'CreatedAt', 'ClosedAt', 'Assignees']
    with open(csv_filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)


class Repo():
    """A representation of a GitHub Repo"""

    def __init__(self, organization, token, filename, repos=[], issues=[], labels=[], headers=[]):
        self.organization = organization
        self.repos = repos
        self.issues = issues
        self.labels = labels
        self.token = token
        self.filename = filename
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + token
        }

    def update_csv(self, row):
        with open(self.filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def get_repo_names(self):
        """This one gets all the repos for a GitHub organization"""
        self.repos = []  # Making sure no repos from a previous org is in memory
        headers = self.headers
        # GitHub API Call to get repos
        page_number = 1
        while page_number > 0:
            response = requests.get(
                'https://api.github.com/orgs/' + self.organization + '/repos?per_page=100&page=' + str(page_number),
                headers=headers)
            json_response = json.loads(response.content)  # Parsing JSON document from GitHub API
            for repo in json_response:  # Iterating thru the repos and fetching the name
                self.repos.append(repo['name'])
            print(str(len(json_response)) + " repositories in " + self.organization + " page #" + str(page_number))
            if len(json_response) == 100:
                page_number = page_number + 1
            else:
                page_number = 0
                break

    def get_issues(self, organization, repo, state):
        """This one gets all the issues for a given repo"""
        headers = self.headers
        self.issues = []  # Making sure no issues from a previous repo is in memory
        page_number = 1
        while page_number > 0:
            response2 = requests.get(
                'https://api.github.com/repos/' + organization + '/' + repo + '/issues?state=' + state +'&per_page=100'
                                                                              '&page=' + str(
                    page_number),
                headers=headers)
            json_response2 = json.loads(response2.content)
            for issue in json_response2:
                self.issues.append(issue['number'])
                my_issue = Issue(organization, self.token, self.filename, repo, issue['number'], issue['labels'], headers,
                                 issue['created_at'], issue['closed_at'], issue['assignees'])
                if  my_issue.labels == []:
                    self.labels.append('null')
                    csv_row = [organization, repo, issue['number'], 'null', 'null', 'null', my_issue.created_at,my_issue.closed_at,len(my_issue.assignees)]
                    self.update_csv(csv_row)
                for label in my_issue.labels:
                    self.labels.append(label['name'])
                    csv_row = [organization, repo, issue['number'], label['name'], label['description'], label['default'], my_issue.created_at, my_issue.closed_at,len(my_issue.assignees)]
                    self.update_csv(csv_row)
            print(str(len(json_response2)) + " issues in " + repo + " page #" + str(page_number))
            if len(json_response2) == 100:
                page_number = page_number + 1
            else:
                page_number = 0
                break


class Issue():
    """A representation of a GitHub Issue"""

    def __init__(self, organization, token, filename, repo=[], issue=[], labels=[], headers=[], created_at=[], closed_at=[], assignees=[]):
        self.organization = organization
        self.repo = repo
        self.created_at = created_at
        self.closed_at = closed_at
        self.issueNbr = issue
        self.labels = labels
        self.assignees = assignees
        self.token = token
        self.filename = filename
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + token
        }

