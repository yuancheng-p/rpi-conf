"""
reference: https://github.com/hjwp/book-example/blob/master/deploy_tools/fabfile.py
"""

import os
import random

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, put


REPO_URL = 'https://github.com/yuancheng2013/edupi.git'

SOURCE_DIR_NAME = 'edupi'

EDUPI_SITE_NAME = 'edupi.fondationorange.org'

RASP_USER_NAME = 'pi'

CONFIG_TEMPLATES_FOLDER = 'sysconf'


def config_hotspot():
    run('sudo apt-get update')
    run('sudo apt-get install -y hostapd dnsmasq')
    config_files = [
        '/etc/network/interfaces',
        '/etc/dnsmasq.conf',
        '/etc/hostapd/hostapd.conf.orig',
        '/etc/rc.local',
    ]

    list(map(_send_file, config_files))
    run('sudo reboot')


def install_commons():
    """
    """
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


def deploy_edupi():
    nginx_conf = '/etc/nginx/sites-enabled/%s' % EDUPI_SITE_NAME
    gunicorn_conf = '/etc/init/gunicorn-edupi.fondationorange.org.conf'

    _send_file(nginx_conf)
    _send_file(gunicorn_conf)
    site_folder = '/home/%s/sites/%s' % (RASP_USER_NAME, EDUPI_SITE_NAME)
    source_folder = os.path.join(site_folder, SOURCE_DIR_NAME)
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


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


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', SOURCE_DIR_NAME):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip3'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    # install Front-End packages
    # assume that node.js, npm, bower is installed
    run('cd %s && ../virtualenv/bin/python3 manage.py bower install' % source_folder)
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % source_folder)


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))
