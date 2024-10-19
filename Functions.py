from pathlib import Path
from configparser import ConfigParser
import traceback
import shutil
import logging
import xml.etree.ElementTree as ET


def search_project(path, name):
    projects = list()
    try:
        for project in Path(path).rglob(name):
            projects.append(project)
    except PermissionError:
        pass
    except OSError:
        pass
    return projects
