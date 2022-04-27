#!/usr/bin/python3
"""
This is the deploy_web_static module
"""
from fabric.api import *
import datetime
from os.path import exists

env.hosts = ["35.227.90.48", "34.139.233.64"]


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


path_archive = do_pack()


def do_deploy(archive_path):
    """
    This function distributes an archive to the web servers,
    """
    if not exists(archive_path):
        return False
    try:
        archive_name = archive_path.split("/")[-1][:-4]
        folder = "/data/web_static/releases/"
        put(archive_path, "/tmp")
        run("mkdir -p {}{}/".format(folder, archive_name))
        run("tar -xzf /tmp/{}.tgz -C {}{}".format(archive_name, folder,
                                                  archive_name))
        run("rm /tmp/{}.tgz".format(archive_name))
        run("mv {}{}/web_static/* {}{}/".format(folder,
            archive_name, folder, archive_name))
        run("rm -rf {}{}/web_static".format(folder, archive_name))
        run("rm /data/web_static/current")
        run("ln -s -f {}{}/ /data/web_static/current".format(folder,
                                                             archive_name))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    script that creates and distributes an
    archive to the web servers
    """
    if not path_archive:
        return False
    else:
        return do_deploy(path_archive)
