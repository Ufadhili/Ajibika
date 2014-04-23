from fabric.api import run, local
from fabric.contrib.console import confirm


def host_type():
    local('uname -s')


def commit_changes():	
	with settings(warn_only=True):
		result = local("git add . && git commit -m initial fabric file added.")
		if result.failed and not confirm("Git add and commit has failed. Continue anyway?"):
			abort("Aborting by user request")


def push_changes():
	with settings(warn_only=True):
		result = local("git push origin develop")
		if result.failed and not confirm("Git add and commit has failed. Continue anyway?"):
			abort("Aborting by user request")
