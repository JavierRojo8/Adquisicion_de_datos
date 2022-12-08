from git import Repo    
import re          
from github import Github

REPO_DIR = './skale/skale-manager'
info = ['key','keys','password','username','credentials','login','secret']

def extract(repo_dir):
    repo = Repo(repo_dir) # path al repositorio con el que deseamos trabajar
    commits = list(repo.iter_commits('develop'))
    return commits

if __name__ == '__main__':
    commits = extract(REPO_DIR)
    for commit in commits:
        for _ in info:
            if re.search(_, commit.message, re.IGNORECASE):
                print('Commit: {} - {}'.format(commit.hexsha, commit.message))
                
                

    