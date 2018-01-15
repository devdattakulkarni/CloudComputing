import os
from os.path import expanduser

home_dir = expanduser("~")

def get_cloud_setup():
    cloud_setup = []
    if os.path.exists(home_dir + "/.aws/credentials") and os.path.exists(home_dir + "/.aws/config"):
        cloud_setup.append("aws")
    if os.path.exists(home_dir + "/.config/gcloud"):
        cloud_setup.append("gcloud")
    return cloud_setup
