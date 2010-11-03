""" Local scripts to manage cloning new tags and updating the
    currently running version.
"""

from os import listdir
from os.path import join, isdir, isfile
from fabric.api import env, local, cd
from fabric.api import prompt
from fabric.colors import green, red


## Configuration ##

SANDBOX_DIR = 'dev'
CURRENT_DIR = 'current'
GIT_REPO = 'git@github.com:largeblue/openideo.git'


## Scripts ##

def virtualenv():
    #local('../bin/python ../virtualenv.py --no-site-packages --distribute .')
    local('../bin/python ../virtualenv.py --no-site-packages .')

def bootstrap():
    #local('../bin/python bootstrap.py --distribute')
    local('../bin/python bootstrap.py')

def setup(target=SANDBOX_DIR):
    local('git clone %s %s' % (GIT_REPO, target))
    with cd(target):
        # finish git setup
        local('git submodule init')
        local('git submodule sync')
        local('git submodule update')
        
        tags = local('git tag')
        if target in tags:
            local('git checkout %s' % target)
            print(green('Checked out %s' % target))
            return
        else:
            print(red('No tag named %s' % target))
            print(red('Using trunk'))

        virtualenv()
        bootstrap()


def update(target=SANDBOX_DIR):

    dirs = [d for d in listdir('.') if isdir(d) and d not in ['bin', 'etc', '.git', 'develop-eggs', 'eggs', 'include', 'lib', 'parts']]
    
    if target not in dirs:
        setup(target)

    if target == SANDBOX_DIR:
        current = local('git describe --abbrev=0 --tags')
        if current not in dirs:
            print 'Setting up current tag:', green(current)
            setup(current)
    

    with cd(target):
        # Run Buildout
        if not isdir('./%s/bin' % target):
            virtualenv()
        if not isfile('./%s/bin/buildout' % target):
            bootstrap()
        local('./bin/buildout -U', capture=False)

        # Run tests
        #local('')

    ## Finally, symlink CURRENT_DIR
    # Remove existing CURRENT_DIR?
    local('ln -s %s %s' % (target, CURRENT_DIR))
    # Prompt user for additional directory links outside the buildout
    # while True:
    #     d = prompt('Link directory:')
    #     if d:
    #         local('ln -s %s %s' % (d, join(target, d)))


