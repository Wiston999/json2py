from __future__ import print_function
import requests
from json2py.models import *

__author__ = 'Victor'


class User(NestedField):
    login = TextField()
    id = IntegerField()
    url = TextField()
    user_type = TextField(name = 'type')
    site_admin = BooleanField()
    email = TextField(required = False)
    full_name = TextField(name = 'name', required = False)


class Repo(NestedField):
    id = IntegerField()
    name = TextField()
    full_name = TextField()
    owner = User()
    is_private = BooleanField(name = 'private')
    description = TextField()
    size = IntegerField()
    language = TextField()
    default_branch = TextField()


class RepoList(ListField):
    __model__ = Repo


github_user = 'wiston999'
github_repo = 'json2py'

response = requests.get('https://api.github.com/users/%s' % github_user)
if response.status_code == 200:
    my_user = User(response.json())
    print (my_user.login.value, "'s stats:")
    print ("id:", my_user.id.value)
    print ("email:", my_user.email.value)
    print ("full_name:", my_user.full_name.value)
    print ("login:", my_user.login.value)
    print ("url:", my_user.url.value)
    print ("type:", my_user.user_type.value)
    print ("site_admin:", my_user.site_admin.value)
else:
    print ("User response status code", response.status_code)

response = requests.get('https://api.github.com/repos/%s/%s' %(github_user, github_repo))
if response.status_code == 200:
    this_repo = Repo(response.json())
    print (this_repo.name.value, "'s stats:")
    print ("id:", this_repo.id.value)
    print ("full_name:", this_repo.full_name.value)
    print ("owner:", this_repo.owner.login.value)
    print ("private:", this_repo.is_private.value)
    print ("description:", this_repo.description.value)
    print ("language:", this_repo.language.value)
    print ("default_branch:", this_repo.default_branch.value)
else:
    print ("Repo response status code", response.status_code)

response = requests.get('https://api.github.com/users/%s/repos' % github_user)
if response.status_code == 200:
    user_repo_list = RepoList(response.json())
    print (github_user, "repositories:")
    for repo in user_repo_list:
        print ("Repository name:", repo.name.value, "with id:", repo.id.value, "written in", repo.language.value)
        print ("Repository Owner:", repo.owner.login.value)
        print ('-'*70)
else:
    print ("RepoList response status code", response.status_code)
