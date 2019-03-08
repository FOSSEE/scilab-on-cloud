import requests
from urllib.parse import urljoin
import json
from hyper.contrib import HTTP20Adapter
from git import Repo
from soc.config import MAIN_REPO
from soc.config import GITHUB_ACCESS_TOKEN, GITHUB_ACCESS_TOKEN_SOCBOT,\
    TEMP_USER, MAIN_USER


def get_commits(file_path, main_repo=True):
    repo_path = MAIN_REPO + file_path
    """
    return: list of commits, which affected the files in filepath
    """
    repo = Repo(repo_path, search_parent_directories=True)
    commit_message = []
    #print(list(repo.iter_commits(paths =  file_path)))
    for commit in list(repo.iter_commits(paths=file_path)):
        commit_message.append((commit.message, commit.hexsha))
    return commit_message


def get_file(file_path, commit_sha, main_repo=False):

    repo_path = MAIN_REPO + file_path
    repo = Repo(repo_path, search_parent_directories=True)
    file_contents = repo.git.show('{}:{}'.format(commit_sha, file_path))
    return file_contents


def update_file(file_path,
                commit_message,
                content,  # base64 encoded
                committer,  # [name, emails]
                branch='master',
                main_repo=False):
    """
    return: commit sha of new commit, after updating the file
    """
    base_url = 'https://api.github.com/repos/'
    access_token = GITHUB_ACCESS_TOKEN_SOCBOT if main_repo\
        else GITHUB_ACCESS_TOKEN
    owner = MAIN_USER if main_repo else TEMP_USER

    headers = {
        'Authorization': 'token %s' % access_token,
        'Content-Type': 'application/json'}

    url = urljoin(base_url, owner +
                  '/Scilab-TBC-Uploads/contents/' + file_path)

    requestsh2 = requests.Session()  # New HTTP 2
    requestsh2.mount(url, HTTP20Adapter())  # New HTTP 2
    file_r = requestsh2.get(url, headers=headers)  # New HTTP 2
    if file_r.status_code == requests.codes.ok:
        file_sha = json.loads(file_r.content)['sha']
        data = {
            "message": commit_message,
            "committer": {
                "name": committer[0],
                "email": committer[1]
            },
            "content": content,
            "sha": file_sha,
        }

        requestsh2 = requests.Session()  # New HTTP 2
        requestsh2.mount(url, HTTP20Adapter())  # New HTTP 2
        r = requestsh2.put(
            url,
            headers=headers,
            data=json.dumps(data))  # New HTTP 2
        if r.status_code == requests.codes.ok:
            return r.json()['commit']['sha']
    return None


def get_category(category_id):
    categories = [
        'Fluid Mechanics',
        'Control Theory & Control Systems',
        'Chemical Engineering',
        'Thermodynamics',
        'Mechanical Engineering',
        'Signal Processing',
        'Digital Communications',
        'Electrical Technology',
        'Mathematics & Pure Science',
        'Analog Electronics',
        'Digital Electronics',
        'Computer Programming',
        'Others',
    ]
    if category_id <= len(categories):
        return categories[category_id - 1]
    else:
        return 'Others'
