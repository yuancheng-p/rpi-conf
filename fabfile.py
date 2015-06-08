"""
reference: https://github.com/hjwp/book-example/blob/master/deploy_tools/fabfile.py
"""

import os

from fabric.contrib.files import exists
from fabric.api import run, put


__all__ = ['config_hotspot', 'install_commons', 'deploy_edupi']

REPO_URL = 'https://github.com/yuancheng2013/edupi.git'

SOURCE_DIR_NAME = 'edupi'

EDUPI_SITE_NAME = 'edupi.fondationorange.org'

RASP_USER_NAME = 'pi'

DEFAULT_PASSWORD = 'raspberry'

CONFIG_TEMPLATES_FOLDER = 'sysconf'


def _send_file(abs_path, use_sudo=True):
    """
    send local file to remote host
    """
    put(_get_config_file(abs_path), abs_path, use_sudo=use_sudo)
    run('sudo chmod 755 %s' % abs_path)
    if use_sudo:
        run('sudo chown root:root %s' % abs_path)


def _get_config_file(path):
    if path[0] != '/':
        print 'please input the absolute path'
        exit(-1)

    f = os.path.join(os.getcwd(), CONFIG_TEMPLATES_FOLDER, path[1:])
    if not os.path.exists(f):
        print "'%s' does not exist" % f
        exit(-1)
    return f


class EdupiDeployManager():
    def __init__(self):
        self.site_folder = '/home/%s/sites/%s' % (RASP_USER_NAME, EDUPI_SITE_NAME)
        self.source_folder = os.path.join(self.site_folder, SOURCE_DIR_NAME)

    def deploy(self, commit):
        # Nginx conf
        _send_file('/etc/nginx/sites-enabled/%s' % EDUPI_SITE_NAME)
        # Gunicorn conf
        _send_file('/etc/init/gunicorn-edupi.fondationorange.org.conf')

        self._create_directory_structure_if_necessary(self.site_folder)
        self._get_source(self.source_folder, commit)
        self._update_virtualenv(self.source_folder)
        self._update_static_files(self.source_folder)
        self._update_database(self.source_folder)

    @staticmethod
    def _create_directory_structure_if_necessary(site_folder):
        for subfolder in ('database', 'static', 'virtualenv', SOURCE_DIR_NAME):
            run('mkdir -p %s/%s' % (site_folder, subfolder))

    @staticmethod
    def _get_source(source_folder, commit):
        if exists(source_folder + '/.git'):
            run('cd %s && git fetch' % (source_folder,))
        else:
            run('git clone %s %s' % (REPO_URL, source_folder))

        run('cd %s && git reset --hard %s' % (source_folder, commit))

    @staticmethod
    def _update_virtualenv(source_folder):
        virtualenv_folder = source_folder + '/../virtualenv'
        if not exists(virtualenv_folder + '/bin/pip3'):
            run('virtualenv --python=python3 %s' % (virtualenv_folder,))
        run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
        ))

    @staticmethod
    def _update_static_files(source_folder):
        # install Front-End packages
        # assume that node.js, npm, bower is installed
        run('cd %s && ../virtualenv/bin/python3 manage.py bower install' % source_folder)
        run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % source_folder)

    @staticmethod
    def _update_database(source_folder):
        run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
            source_folder,
        ))
        # ensure that there is a default super user.
        run("""
cd %s &&
echo "
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
try:
    User.objects.create_superuser('%s', '', '%s')
except IntegrityError as e:  # user exists
    print(e)
" |
../virtualenv/bin/python3 manage.py shell
            """
            % (source_folder, RASP_USER_NAME, DEFAULT_PASSWORD))


def config_hotspot():
    run('sudo apt-get update')
    run('sudo apt-get install -y hostapd dnsmasq')
    config_files = [
        '/etc/network/interfaces',
        '/etc/dnsmasq.conf',
        '/etc/resolvconf.conf',
        '/etc/hostapd/hostapd.conf.orig',
        '/etc/rc.local',
    ]

    list(map(_send_file, config_files))
    run('sudo reboot')


def install_commons():
    run('sudo apt-get update')
    run('sudo apt-get install -y nginx')
    run('sudo apt-get install -y python3-pip')
    run('sudo apt-get install upstart')  # this will prompt and wait for confirm
    run('sudo apt-get install -y libmagickwand-dev')
    run('sudo pip-3.2 install virtualenv')

    # install nodejs, bower
    nodejs_path = '/tmp/node_latest_armhf.deb'
    if not exists(nodejs_path):
        run('wget http://node-arm.herokuapp.com/node_latest_armhf.deb --directory-prefix=/tmp/')

    run('sudo dpkg -i %s' % nodejs_path)
    run('curl -L https://www.npmjs.com/install.sh | sudo sh')
    run('sudo npm install -g bower')


def deploy_edupi(commit='master'):
    manager = EdupiDeployManager()
    manager.deploy(commit)
