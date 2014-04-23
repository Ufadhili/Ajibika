from fabric.api import run, local, settings, abort
from fabric.contrib.console import confirm
from fabric.operations import prompt


def host_type():
    local('uname -s')

def commit():	
	with settings(warn_only=True):		
		# add any new untracked files
		add_files = local("git add .")
		if add_files.failed and not confirm("Command git add has failed. Continue anyway?"):
			abort("Aborting by user request")
		#Promt for a commit message	
		commit_message = prompt("Please the enter commit message")
		#commit files with entered message
		commit_files = local("git commit -m '%s'" %(commit_message))
		if commit_files.failed and not confirm("Command git commit has failed. Continue anyway?"):
			abort("Aborting by user request")


def push():
	with settings(warn_only=True):
		result = local("git push origin develop")
		if result.failed and not confirm("Git add and commit has failed. Continue anyway?"):
			abort("Aborting by user request")
