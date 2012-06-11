""" Local scripts to manage cloning new tags and updating the
    currently running version.
"""
from __future__ import with_statement
from os import listdir
from os.path import join, isdir, isfile, dirname
from fabric.api import env, local, cd
from fabric.api import prompt
from fabric.colors import green, red
from fabric.contrib.console import confirm


## Configuration ##

from ConfigParser import SafeConfigParser

here = dirname(__file__)
config = SafeConfigParser({'here': here})
config.read(['clip.cfg'])

if 'env' not in config.sections():
    print red('WARNING: No [env] section found in clip.cfg')
if 'repo' not in config.sections():
    print red('WARNING: No [repo] section found in clip.cfg')

SANDBOX_DIR = config.get('env', 'sandbox_dir')
CURRENT_DIR = config.get('env', 'current_dir')
GIT_REPO = config.get('repo', 'url')


## Scripts ##

def virtualenv():
    #local('../bin/python ../virtualenv.py --no-site-packages --distribute .')
    local('python ../virtualenv.py --no-site-packages .')

def bootstrap():
    #local('../bin/python bootstrap.py --distribute')
    local('bin/python bootstrap.py')

def setup(target=SANDBOX_DIR):
    local('git clone %s %s' % (GIT_REPO, target))
    with cd(target):
        # finish git setup
        local('git submodule init')
        local('git submodule sync')
        local('git submodule update')

        tags = local('git tag')
        if target in tags:
            local('git checkout -b %s %s' % (target, target))
            print(green('Checked out %s' % target))
        else:
            print(red('No tag named %s' % target))
            print(red('Using trunk'))

        virtualenv()
        bootstrap()


def build(target, activate=False):
    with cd(target):
        # Run Buildout
        if not isdir('bin'):
            virtualenv()
        if not isfile('bin/buildout'):
            bootstrap()
        local('bin/buildout -U', capture=False)

        # Run tests
        #local('')

    if 'post_build_scripts' in config.options('env'):
        print green('Running post-build scripts')
        with cd(target):
            scripts = config.get('env', 'post_build_scripts')
            run_scripts(scripts)


    if activate:
        if ('activate_prompt' in config.options('env')) and (config.get('env', 'activate_prompt') not in ('1', 'True', 'true')):
            activate_prompt = False
        else:
            activate_prompt = True

        if (activate_prompt and confirm('Activate %s?' % target)) or not activate_prompt:

            ## Finally, symlink CURRENT_DIR
            # Remove existing CURRENT_DIR
            if CURRENT_DIR in listdir('.'):
                local('rm %s' % CURRENT_DIR)

            local('ln -s %s %s' % (target, CURRENT_DIR))

            if 'post_activation_scripts' in config.options('env'):
                print green('Running post-activation scripts')
                with cd(CURRENT_DIR):
                    scripts = config.get('env', 'post_activation_scripts')
                    run_scripts(scripts)


def update(target=SANDBOX_DIR):

    dirs = [d for d in listdir('.') if isdir(d) and d not in ['bin', 'etc', '.git', 'develop-eggs', 'eggs', 'include', 'lib', 'parts']]

    if target not in dirs:
        setup(target)

    if target == SANDBOX_DIR:
        with cd(target):
            local('git fetch --tags')
            current = local('git describe --abbrev=0 --tags')

        if current not in dirs:
            print 'Setting up current tag:', green(current)
            setup(current)

        build(current, activate=True)
        build(target)

    else:
        build(target, activate=True)


def run_scripts(scripts):
    for script in scripts.split('\n'):
        if 'script:%s' % script in config.sections():
            commands = config.get('script:%s' % script, 'commands')
            for command in commands.split('\n'):
                if command:
                    local(command, capture=False)
        elif script:
            print red('Script "%s" not defined in clip.cfg' % script)

