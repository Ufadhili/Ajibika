from fabric.api import run, local, settings, abort, env, sudo
from fabric.contrib.console import confirm
from fabric.operations import prompt
from cuisine import package_install


env.hosts = ['54.73.196.197']
# env.hosts = ["ec2-54-228-1-80.eu-west-1.compute.amazonaws.com"]
env.user = 'ubuntu'
env.key_filename = '/home/james/Downloads/eumicro.pem'

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
	# run("sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable")
	# run("sudo apt-get -y install postgis postgresql-9.3 postgresql-9.3-postgis-2.1")
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
	# run("wget http://download.osgeo.org/gdal/gdal-1.9.0.tar.gz")
	# run("tar xvfz gdal-1.9.0.tar.gz")
	# run("cd gdal-1.9.0")
	# run("./configure --with-python")
	# run("make")
	# run("sudo make install")

def install_elasticsearch():
	package_install("openjdk-7-jre-headless")
	run("wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.deb")
	run("sudo dpkg -i elasticsearch-1.1.1.deb")
	run("sudo service elasticsearch start")

def get_the_code():
	run("git clone https://github.com/mysociety/pombola.git")
