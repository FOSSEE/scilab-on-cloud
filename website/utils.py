from github import Github
import base64
import requests
from urlparse import urljoin
import json

from soc.config import GITHUB_ACCESS_TOKEN, GITHUB_ACCESS_TOKEN_SOCBOT

g = Github(GITHUB_ACCESS_TOKEN_SOCBOT)
# FOSSEE = g.get_organization('FOSSEE') 
# repo = FOSSEE.get_repo('Scilab-TBC-Uploads')

user = g.get_user('socbot')
repo = user.get_repo('Scilab-TBC-Uploads')

TEMP_USER = 'appucrossroads'
MAIN_USER = 'socbot'


def get_commits(file_path, main_repo=True):
	return repo.get_commits(path=file_path)


def get_file_contents(file_path, revision_id):
	return repo.get_file_contents(path=file_path, ref=revision_id)


def get_file(file_path, ref='master', main_repo=False):

	base_url = 'https://api.github.com/repos/'
	access_token = GITHUB_ACCESS_TOKEN_SOCBOT if main_repo else GITHUB_ACCESS_TOKEN
	owner = MAIN_USER if main_repo else TEMP_USER

	headers = {
	    'Authorization': 'token %s' % access_token,
	    'Content-Type': 'application/json'}

	url =  urljoin(base_url, owner + '/Scilab-TBC-Uploads/contents/' + file_path)

	data = {
		"ref": ref,
	}
	r = requests.get(url, headers=headers, data=json.dumps(data))
	if r.status_code == requests.codes.ok:
		return json.loads(r.content)
	else:
		return None


def update_file(file_path,
				commit_message,
				content, # base64 encoded
				committer, # [name, emails]
				branch='master',
				main_repo=False):
	
	base_url = 'https://api.github.com/repos/'
	access_token = GITHUB_ACCESS_TOKEN_SOCBOT if main_repo else GITHUB_ACCESS_TOKEN
	owner = MAIN_USER if main_repo else TEMP_USER

	headers = {
	    'Authorization': 'token %s' % access_token,
	    'Content-Type': 'application/json'}

	url =  urljoin(base_url, owner + '/Scilab-TBC-Uploads/contents/' + file_path)

	file_r = requests.get(url, headers=headers)
	if file_r.status_code == requests.codes.ok:
		file_sha = json.loads(file_r.content)['sha']
		data = {
			"message" : commit_message,
			"committer": {
			    "name": committer[0],
			    "email": committer[1]
			},
			"content": content,
			"sha": file_sha,
		}
		r = requests.put(url, headers=headers, data=json.dumps(data))
		return r.status_code == requests.codes.ok
	else:
		return False












