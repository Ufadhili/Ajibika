from fabric.api import run, local, settings, abort
from fabric.contrib.console import confirm


def host_type():
    local('uname -s')

def commit():	
	with settings(warn_only=True):
		result = local("git add . && git commit -m 'test commit and deploy via fabric.'")
		if result.failed and not confirm("Git add and commit has failed. Continue anyway?"):
			abort("Aborting by user request")

def push():
	with settings(warn_only=True):
		result = local("git push origin develop")
		if result.failed and not confirm("Git add and commit has failed. Continue anyway?"):
			abort("Aborting by user request")
