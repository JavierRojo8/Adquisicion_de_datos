from git import Repo    
import re          
from github import Github

REPO_DIR = './skale/skale-manager'
sensible = ['key','keys','password','username','credentials','login','secret']

def extract(repo_dir):
    repo = Repo(repo_dir) # path al repositorio con el que deseamos trabajar
    extracted = list(repo.iter_commits('develop'))
    return extracted

def search(_):
    for word in sensible:
        if re.search(word, _.message):
            print('Commit: {} - {}'.format(_.hexsha, _.message))

if __name__ == '__main__':
    extracted = extract(REPO_DIR)
    for _ in extracted:
        search(_)
        
                
                

    