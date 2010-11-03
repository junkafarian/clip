``clip`` Deployment environment
===============================

Deployment environment for buildout-based projects using git.

Installation
------------

Standard workflow for deploying an application using clip is:

         junkafarian$ git clone git://github.com/junkafarian/clip.git PROJECT_NAME
         junkafarian$ python ./virtualenv.py --no-site-packages --distribute .
         junkafarian$ ./bin/python bootstrap.py --distribute
         junkafarian$ ./bin/buildout -U


Configuration
-------------

The environment then needs to be configured using settings within
``fabfile.py``. See ``docs`` for more information on what settings
are required.


Usage
-----

This tool was inspired by Jim Glenn's `Blog Post on KARL release management <http://www.sixfeetup.com/blog/karl-s-new-approach-to-safely-releasing-updates-to-hosted-production-sites>`_.
The anticipated process is designed to ensure the current instance is
unaffected while the newest tag is set up in a new directory. Once the
new version has been tested and is ready to replace the existing
release, symlinks are switched from the old release to the new one.
This allows for the most recent stable release to always be accessible
in a predictable location on the filesystem (default ``current``).
 
