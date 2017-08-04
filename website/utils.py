import requests
from urlparse import urljoin
import json

from soc.config import GITHUB_ACCESS_TOKEN, GITHUB_ACCESS_TOKEN_SOCBOT,\
TEMP_USER, MAIN_USER

def get_commits(file_path, main_repo=True):
    """
    return: list of commits, which affected the files in filepath
    """
    base_url = 'https://api.github.com/repos/'
    access_token = GITHUB_ACCESS_TOKEN_SOCBOT if main_repo\
        else GITHUB_ACCESS_TOKEN
    owner = MAIN_USER if main_repo else TEMP_USER

    headers = {
        'Authorization': 'token %s' % access_token,
        'Content-Type': 'application/json'}

    url = urljoin(base_url, owner + '/Scilab-TBC-Uploads/commits')
    params = {
        'path': file_path,
    }

    r = requests.get(url, headers=headers, params=params)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


def get_file(file_path, ref='master', main_repo=False):

    base_url = 'https://api.github.com/repos/'
    access_token = GITHUB_ACCESS_TOKEN_SOCBOT if main_repo\
        else GITHUB_ACCESS_TOKEN
    owner = MAIN_USER if main_repo else TEMP_USER

    headers = {
        'Authorization': 'token %s' % access_token,
        'Content-Type': 'application/json'}

    url = urljoin(base_url, owner + '/Scilab-TBC-Uploads/contents/' + file_path)

    params = {
        "ref": ref,
    }

    r = requests.get(url, headers=headers, params=params)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return None


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

    url = urljoin(base_url, owner + '/Scilab-TBC-Uploads/contents/' + file_path)

    file_r = requests.get(url, headers=headers)
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
        r = requests.put(url, headers=headers, data=json.dumps(data))
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
