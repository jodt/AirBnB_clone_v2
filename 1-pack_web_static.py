#!/usr/bin/python3
"""
This is the pack_web_static module
cript that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo,
using the function do_pack
"""

import datetime
from fabric.api import local


def do_pack():
    """
    This function create an archive
    """
    now = datetime.datetime.now()
    now_str = "{}{}{}{}{}{}".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    name_file = "web_static_"+now_str+".tgz"
    local("mkdir -p versions")
    local("tar -cvzf versions/{} web_static".format(name_file))
    return "versions/{}".format(name_file)
