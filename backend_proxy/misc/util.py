import os
import sys
import json
import random
import string
import subprocess

KEYWORDS = ["panel", "about", "home", "test", ""]


def get_specs_from_git(git_url):
    lind = git_url.rfind("/")
    rind = git_url.rfind(".")
    dname = git_url[lind+1: rind]
    dname = "backups/{}".format(dname)
    # check if folder exists, if so, delete it
    if not os.path.isdir("backups"):
        os.mkdir("backups")
    if os.path.isdir(dname):
        subprocess.run(["rm", "-rf", dname])
    p = subprocess.run(["git", "clone", "--depth", "1", git_url, dname])
    if p.returncode != 0:
        raise Exception("Git clone is not successfull. Check the git URL")
    # check if dip_specs folder exists
    if not os.path.isdir("{}/dip_specs".format(dname)):
        subprocess.run(["rm", "-rf", dname])
        raise Exception("The project does not contain the folder dip_specs. "
                        "Fix the project's root according to the tutorial")
    # read the 4 files:
    fnames = ["author_specs.json", "form_data.json", "root.json"]
    jsons = []
    for fname in fnames:
        if not os.path.isfile("{}/dip_specs/{}".format(dname, fname)):
            subprocess.run(["rm", "-rf", dname])
            raise Exception("{} file is missing in the project".format(fname))
        with open("{}/dip_specs/{}".format(dname, fname), "r") as f:
            json_dict = json.load(f)
        jsons.append(json_dict)
    return jsons


def check_is_auth(request):
    raise NotImplementedError
    # raise Exception("Not Authenticated. You should login"
    # "If you see that you can go to /login to authenticate")
