#!/usr/bin/python3
"""
This is the deploy_web_static module
"""
from fabric.api import *

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ["35.227.90.48", "34.139.233.64"]

path_archive = do_pack()


def deploy():
    """
    script that creates and distributes an
    archive to the web servers
    """
    if not path_archive:
        return False
    else:
        return do_deploy(path_archive)
