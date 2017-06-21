from github import Github
import base64
import requests
from urlparse import urljoin
import json

from soc.config import GITHUB_ACCESS_TOKEN

g = Github(GITHUB_ACCESS_TOKEN)
# FOSSEE = g.get_organization('FOSSEE') 
# repo = FOSSEE.get_repo('Scilab-TBC-Uploads')

user = g.get_user('appucrossroads')
repo = user.get_repo('Scilab-TBC-Uploads')

# username = user.login
# repo_name = repo.name
headers = {
    'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN,
    'Content-Type': 'application/json'}

base_url = 'https://api.github.com/repos/'


def update_file(file_path,
				commit_message,
				content, # base64 encoded
				sha, # sha checksum of file blob to be updated
				committer, # [name, emails]
				branch='master'):
	url =  urljoin(base_url, 'appucrossroads/Scilab-TBC-Uploads/contents/' + file_path)
	data = {
		"message" : commit_message,
		"committer": {
		    "name": committer[0],
		    "email": committer[1]
		},
		"content": content,
		"sha": sha,
	}
	r = requests.put(url, headers=headers, data=json.dumps(data))
	return r.status_code == requests.codes.ok
