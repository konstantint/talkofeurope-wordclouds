# -*- coding: UTF-8 -*-
"""
TalkOfEurope: Deployment automation script (for deploying the site to talkofeurope.ing.ee under uWSGI+NginX)

Usage: fab -l

Copyright 2016, Konstantin Tretyakov
License: MIT
"""
import colorama, os
from datetime import datetime
from fabric.api import *
from fabric.colors import red, green, yellow, blue

colorama.init() # Enable ANSI colors in windows command-line

SITE='talkofeurope.ing.ee'
SITE_KEY='kt@ut.ee'

env.roledefs = {'root': ['ubuntu@%s' % SITE],
                'site': ['%s@%s' % (SITE, SITE)]}

@task
@roles('root')
def destroy_account():
    """Remove the site deployment account along with all the data. Very destructive!"""
    if raw_input(red("Are you sure? Type YES if you are: ", True)) == "YES":
        print(red("Deleting site..."))
        run('sudo service uwsgi stop %s' % SITE)
        run('sudo rm -f /etc/uwsgi/apps-available/%s' % SITE)
        run('sudo rm -f /etc/uwsgi/apps-enabled/%s' % SITE)
        run('sudo rm -f /etc/nginx/sites-available/%s' % SITE)
        run('sudo rm -f /etc/nginx/sites-enabled/%s' % SITE)
        run('sudo rm -rf /var/run/uwsgi/app/%s' % SITE)
        run('sudo deluser --remove-home %s' % SITE)
        run('sudo deluser --group %s || true' % SITE)
        run('sudo service nginx restart')

@task
@roles('root')
def create_account():
    """Create the user account for hosting the site. Needs to be done once for a server."""
    print(green("Creating a user...", True))
    run('sudo adduser --disabled-password --home /sites/{0} --gecos "" {0}'.format(SITE))

    print(green("Enabling PKI access...", True))
    run('sudo -u {0} mkdir -p /sites/{0}/.ssh'.format(SITE))
    run('sudo -u {0} chmod 700 /sites/{0}/.ssh'.format(SITE))
    run('cat ~/.ssh/authorized_keys | grep {1} | sudo -u {0} tee /sites/{0}/.ssh/authorized_keys'.format(SITE, SITE_KEY))

@task
@roles('site')
def install_site():
    """Installs the site for the first time (assumes the account exists)."""
    print(green('Setting up venv...', True))
    run('virtualenv ~/venv')

    #print(green('Installing requirements...', True))
    #put('requirements.txt', '~/')
    #run('~/venv/bin/pip install -r requirements.txt')

    print(green('Preparing package...', True))
    local("python setup.py sdist")

    import glob
    pkg_file = glob.glob("dist/talkofeuropeweb-*.zip")[0]
    print(green('Uploading package file: %s' % pkg_file, True))
    uploaded = list(put(pkg_file, "~/"))[0]

    print(green('Installing package...', True))
    run('~/venv/bin/pip install %s' % uploaded)

@task
@roles('root')
def configure_site():
    """Configures UWSGI and NGINX to serve the site. Needs to be done once."""
    print(green("Registering UWSGI site...", True))
    put("deploy/uwsgi.ini", "/etc/uwsgi/apps-available/%s.ini" % SITE, use_sudo=True)
    run("sudo dos2unix /etc/uwsgi/apps-available/%s.ini" % SITE)
    run("sudo ln -sf /etc/uwsgi/apps-available/%s.ini /etc/uwsgi/apps-enabled/" % SITE)
    run("sudo service uwsgi restart %s" % SITE)

    print(green("Registering NGINX site...", True))
    put("deploy/nginx.conf", "/etc/nginx/sites-available/%s" % SITE, use_sudo=True)
    run("sudo dos2unix /etc/nginx/sites-available/%s" % SITE)
    run("sudo ln -sf /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/" % SITE)
    run("sudo service nginx reload")

@task
def first_deploy():
    """Performs the sequence {create_account, install_site, configure_site}, needed when launching the site for the first time."""
    execute(create_account)
    execute(install_site)
    execute(configure_site)

@task
@roles('site')
def update():
    """Updates the package on the server."""
    print(blue('Preparing package...', True))
    local("python setup.py sdist")

    import glob
    pkg_file = glob.glob("dist/talkofeuropeweb-*.zip")[0]
    print(yellow('Uploading package file: %s' % pkg_file))
    uploaded = list(put(pkg_file, "~/"))[0]

    print(green('Installing package...', True))
    run('~/venv/bin/pip install --no-deps --ignore-installed %s' % uploaded)

    print(green('Reloading server...', True))
    run('touch ~/touch-reload')