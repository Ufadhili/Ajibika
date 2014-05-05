from fabric.api import run, local, settings, abort, env, sudo
from fabric.contrib.console import confirm
from fabric.operations import prompt, put
from fabric.colors import red, green, blue, cyan, magenta
from fabric.utils import puts
from cuisine import package_install, file_exists


env.hosts = ['54.73.56.28']
env.user = 'ubuntu'
env.key_filename = '/home/james/Downloads/eumicro.pem'
web_root = '/var/www/ufadhili/'

def host_type():
    run('uname -s')

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

def bootstrap_pombola_server():
	"""
	"Install and configure the required packages on conf/packages file"
	
	---Some commands I am running on this instance
	sudo apt-get update

	"""
def install_base_packages():
	#Do this on all new servers
	package_install("python-software-properties git-core python-dev python-all-dev python-setuptools libapache2-mod-wsgi")
	package_install("build-essential python-pip nginx")
	package_install("libxml2-dev libxslt1-dev libjpeg-dev mercurial python-docutils poppler-utils \
					python-markdown python-yaml python-openid python-beautifulsoup python-dateutil antiword")
	sudo("pip install --upgrade pip")
	sudo("pip install --upgrade virtualenv")

def update_server():
	run("sudo aptitude update")
	run("sudo aptitude -y safe-upgrade")

def install_postgres_postgis():
	package_install("postgresql postgresql-client postgresql-contrib pgadmin3 postgis postgresql-9.3-postgis-2.1")

def configure_db_template():
	# run("sudo -u postgres createuser pombola")
	# run("sudo -u postgres createuser ubuntu")
	run("sudo su")
	run("su postgres")
	run("createdb -E UTF8 template_postgis")
	run("createlang -d template_postgis plpgsql")
	run("psql -d postgres -c 'UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';'")
	run("psql -U postgres -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql")
	run("psql -U postgres -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql")
	run("psql -U postgres -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis_comments.sql")
	run("psql -d template_postgis -c 'GRANT ALL ON geometry_columns TO PUBLIC;'")
	run("psql -d template_postgis -c 'GRANT ALL ON geography_columns TO PUBLIC;'")
	run("psql -d template_postgis -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'")
	run("createdb -T template_postgis pombola")

def gdal_setup():
	package_install("libgdal1-dev python-gdal gdal-bin")
	"""
	--------Alternatively you can install gdal directly from osgeo----------
	--------Warning: This takes long to compile ---------------

	run("wget http://download.osgeo.org/gdal/gdal-1.9.0.tar.gz")
	run("tar xvfz gdal-1.9.0.tar.gz")
	run("cd gdal-1.9.0")
	run("./configure --with-python")
	run("make")
	run("sudo make install")
	"""

def install_elasticsearch():
	package_install("openjdk-7-jre-headless")
	run("wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.deb")
	run("sudo dpkg -i elasticsearch-1.1.1.deb")
	run("sudo service elasticsearch start")

def get_the_code():
	run("git clone https://github.com/mysociety/pombola.git")

def configure_nginx():
	#Do this for new servers only	
	run("sudo /etc/init.d/nginx start")	
	print green("Copying nginx.config virtual host file for ajibika.org to the sites-available directory")
	with settings(warn_only=True):
		if not file_exists("/etc/nginx/sites-available/www.ajibika.org"):
			result = put("conf/www.ajibika.org", "/etc/nginx/sites-available/", use_sudo=True)
			if result.failed and not confirm("Unable to copy www.ajibika.org to sites-enabled dir. Continue anyway?"):
				abort("Aborting at user request.")
	print green("conf/www.ajibika.org has been copied")
	print red("Removing old nginx configs")	
	if file_exists("/etc/nginx/sites-enabled/default"):
		result = run("sudo rm /etc/nginx/sites-enabled/default")
		if result.failed and not confirm("Unable to Removing old nginx configs. Continue anyway?"):
			abort("Aborting at user request.")
	print magenta("Now Symlinking the ajibika virtual host file to sites sites-enabled")
	if not file_exists("/etc/nginx/sites-enabled/www.ajibika.org"):
		with settings(warn_only=True):
			result = run("sudo ln -s /etc/nginx/sites-available/www.ajibika.org /etc/nginx/sites-enabled/www.ajibika.org")
			if result.failed and not confirm("Unable to symlink the angani \
			 virtual host file to sites sites-enabled. Continue anyway?"):
				abort("Aborting at user request.")

	print "sudo reload nginx"
	run("sudo /etc/init.d/nginx reload")

def reload_nginx():
	puts(green("Reloading nginx"))
	with settings(warn_only=True):
		result = run("sudo /etc/init.d/nginx restart")
		if result.failed and not confirm("Unable to restart nginx. Continue anyway?"):
			abort("Aborting at user request.")	

def configure_gunicorn():
	print green("We will now daemonize gunicorn")
	with settings(warn_only=True):
		if not file_exists("/etc/init/ajibika.conf"):
			result = put("conf/ajibika.conf", "/etc/init/", use_sudo=True)
			if result.failed and not confirm("Unable to copy ajibika.conf to /etc/init/. Continue anyway?"):
				abort("Aborting at user request.")
			puts(green("Now adding a soft link to upstart for the ajibika.conf job"))
			#This helps us do service ajibika restart
			run("sudo ln -s /lib/init/upstart-job /etc/init.d/ajibika")
		else:
			print red("Gunicorn has already been daemonized")

def restart_gunicorn():
	puts(green("Now Restarting Gunicorn"))
	with settings(warn_only=True):
		result = run("sudo service ajibika restart")
		if result.failed and not confirm("Failed to start gunicorn. Continue anyway?"):
			abort("Aborting at user request.")

def remote_logs():	
	run("sudo cat /var/www/logs/gunicorn/access.log")
	run("sudo cat /var/www/logs/nginx/access.log")
	run("sudo cat  /var/www/logs/nginx/error.log")

def update_server():
	run("sudo aptitude update")
	run("sudo aptitude -y safe-upgrade")

def install_local_packages():
	local("sudo apt-get install python-software-properties git-core python-dev python-all-dev python-setuptools libapache2-mod-wsgi")
	local("sudo apt-get install build-essential python-pip nginx libgdal1-dev python-gdal gdal-bin")
	local("sudo apt-get install libxml2-dev libxslt1-dev libjpeg-dev mercurial python-docutils poppler-utils \
					python-markdown python-yaml python-openid python-beautifulsoup python-dateutil antiword")