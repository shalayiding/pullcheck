from config import *
import subprocess
import requests



class fetch:
    
    
    """_summary_
    init the git repo
    """
    def __init__(self, repo_owner,repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.branchs = []
        self.branch_holder = set()
        self.student_branch_map = {}
        self.headers = {
            "Accept": "application/vnd.github+json"
        }
        self.student_pr_map = {}
        self.pulls = []
        

    
    #lets first fetch all branch -r remote only 
    def fetch_all_branch(self) -> list:
        
        # api documentation https://docs.github.com/en/rest/branches/branches?apiVersion=2022-11-28
        branches = []
        page = 1
        try:
            while page:
                response = requests.get(f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/branches", headers=self.headers, params={"page": page, "per_page": 100})
                if response.status_code != 200:
                    print(f"Error fetching branches: {response.status_code}")
                    break
                data = response.json()
                if not data:
                    break

                branches.extend([branch['name'] for branch in data])
                page += 1

        except requests.exceptions.RequestException as e:
            print(f"request exception : {e}")

        self.branchs = branches
        return self.branchs
        
        
    
    #create student map with branches
    def create_map(self) -> dict:
        for branch in self.branchs:
            parts = branch.split('/')
            if len(parts) == 2:
                branch_holder_name = parts[0]
                branchtype = parts[1]
                if branch_holder_name not in self.student_branch_map:
                    self.student_branch_map[branch_holder_name] = []
                self.student_branch_map[branch_holder_name].append(f"{branch_holder_name}/{branchtype}")
        return self.student_branch_map
    
        
    
    def fetch_all_pr(self)->list:
        pull_requests = []
        page = 1

        try:
            while True:
                response = requests.get(f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls", headers=self.headers, params={"state":"all","page": page, "per_page": 100})
                if response.status_code != 200:
                    print(f"Error fetching pull requests: {response.status_code}")
                    break

                data = response.json()
                if not data:
                    break
                pull_requests.extend(data)
                page += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        return pull_requests
    
    # list file in directory 
    def list_files_in_directory(self, directory_path, branch_name):
        params = {
            "ref": branch_name
        }
        try:
            response = requests.get(f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents{directory_path}", headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching directory contents: {response.status_code}")
                return []

            data = response.json()
            res = []
            for d in data:
                res.append(d['name'])
            return res
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []
    

    
    
    # get all the user pr by it is name 
    def all_pr_by_student(self) -> dict:
        pr_response = self.fetch_all_pr()
        for pr in pr_response:
            pr_author = pr['head']['ref'].split('/')[0]
            pr_from = pr['head']['ref']
            pr_link = pr['html_url']
            if pr['head']['ref'].split('/')[0] not in self.student_pr_map:
                self.student_pr_map[pr_author] = []
            self.student_pr_map[pr_author].append(f"{pr_from} : {pr_link}")
        return self.student_pr_map