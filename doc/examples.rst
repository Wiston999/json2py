.. _examples:

Examples
========

In the examples below, we will try to learn how to model JSON with :mod:`json2py`'.
We will cover how to re-utilize models into bigger ones, like JSON support sub-documents.
We will also learn how to model a list of JSON documents.

Modeling Github API
-------------------

For the examples we will try to model Github's public API (or at least a part of it).
We will be model the *user* response from https://api.github.com/users/{user}
using my user account, we will model this *repo* information on https://api.github.com/users/{user}/{repo_name}
And with a bit more effort we will model the *repo* listing on
https://api.github.com/users/{user}/repos. In this example, :mod:`requests`
module will be used for simplicity, but the way of requesting remote resources is up to you.

Let's begin!

User modelling
______________

The user data used on this example will be extracted from https://api.github.com/users/wiston999

Let's suppose we want to grab the user's id, login, url, type and if user is admin.
This task can be done with the following code.

We will map the *type* key into a field named *user_type* into our model.

.. code-block:: python
    :linenos:
    :caption: models.py
    :name: models.py

    from json2py.models import *

    class User(NestedField):
        login = TextField()
        id = IntegerField()
        url = TextField()
        user_type = TextField(name = 'type')
        site_admin = BooleanField()

And we are all done! Now let's request the Github's user info endpoint.

.. code-block:: python
    :linenos:
    :caption: example1.py
    :name: example1.py

    import requests
    from models import User

    response = requests.get('https://api.github.com/users/wiston999')
    my_user = User(response.json())
    print my_user.login.value, "'s stats:"
    print "id:", my_user.id.value
    print "login:", my_user.login.value
    print "url:", my_user.url.value
    print "type:", my_user.user_type.value
    print "site_admin:", my_user.site_admin.value

Output after executing this code is

.. code-block:: text

    Wiston999 's stats:
    id: 1099504
    login: Wiston999
    url: https://api.github.com/users/Wiston999
    type: User
    site_admin: False

This is how modeling works, all you have to do is define class variables into
the class inheriting from :class:`json2py.models.NestedField`.

Repository modeling
___________________
The next step will be modeling a repository information from Github.
We will use the information from this repository, https://api.github.com/repos/wiston999/json2py.
We want to get the id, name, full_name, is_private, description, size, language, default_branch
and the owner fields. One can notice that owner nested document looks familiar, as it shares several fields
with the data on https://api.github.com/users/wiston999. We notice too that shared data is
already modeled into the previous example, so, let's use a bit of code re-utilization.

.. code-block:: python
    :linenos:
    :caption: models.py
    :name: models.py
    :emphasize-lines: 8-

    class User(NestedField):
        login = TextField()
        id = IntegerField()
        url = TextField()
        user_type = TextField(name = 'type')
        site_admin = BooleanField()

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

Notice how the **owner** field is an instance of **User** class defined above.

Let's try these models

.. code-block:: python
    :linenos:
    :caption: example2.py
    :name: example2.py
    :emphasize-lines: 9

    import requests
    from models import User, Repo

    response = requests.get('https://api.github.com/repos/wiston999/json2py')
    this_repo = Repo(response.json())
    print this_repo.name.value, "'s stats:"
    print "id:", this_repo.id.value
    print "full_name:", this_repo.full_name.value
    print "owner:", this_repo.owner.login.value
    print "private:", this_repo.is_private.value
    print "description:", this_repo.description.value
    print "language:", this_repo.language.value
    print "default_branch:", this_repo.default_branch.value

Will output

.. code-block:: text

    json2py 's stats:
    id: 54333024
    full_name: Wiston999/json2py
    owner: Wiston999
    private: False
    description: Convert JSON/dict to python object and viceversa
    language: Python
    default_branch: master

Repository list modeling
________________________

As a last example, lest loop the loop, we are going to model the data
returned by https://api.github.com/users/Wiston999/repos request. We see that this is
a list of repositories, which we have already modeled, so, this should be as simple as

.. code-block:: python
    :linenos:
    :caption: models.py
    :name: models.py
    :emphasize-lines: 19-

    class User(NestedField):
        login = TextField()
        id = IntegerField()
        url = TextField()
        user_type = TextField(name = 'type')
        site_admin = BooleanField()

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

Everything done! Let's try it

.. code-block:: python
    :linenos:
    :caption: example3.py
    :name: example3.py

    import requests
    from models import RepoList

    response = requests.get('https://api.github.com/users/wiston999/repos')
    user_repo_list = RepoList(response.json())
    print "wiston999's repositories:"
    for repo in user_repo_list:
        print "Repository name:", repo.name.value, "with id:", repo.id.value, "written in", repo.language.value
        print "Repository Owner:", repo.owner.login.value
        print '-'*70

And the output

.. code-block:: text

    wiston999 repositories:
    Repository name: BRTMT with id: 24468609 written in JavaScript
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: cursoJS with id: 14053600 written in JavaScript
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: DDSBox with id: 36035006 written in Java
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: DSS with id: 20038644 written in Python
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: ISIII with id: 3630135 written in None
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: json2py with id: 54333024 written in Python
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: Plataforma with id: 2506501 written in Python
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
    Repository name: repos-git with id: 20038280 written in Python
    Repository Owner: Wiston999
    ----------------------------------------------------------------------
