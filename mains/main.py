import questionary
import psutil
import re
import sys
import importlib.metadata
from loguru import logger
from pathlib import Path
from getpass import getuser
from mains.exceptions import IncorrectUser, PackagesNotFound, ReqFileNotFound
from mains.buildinfo import appversion, build

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

def check_user(): #Checks that program is started using user postgres
    required_user = 'postgres'
    current_user = getuser()
    if current_user == required_user:
        return True
    else:
        raise IncorrectUser


def check_requirements(): #Check that all required packages installed
    req_file = Path(__file__).resolve().parent.parent / "requirements.txt"

    if not req_file.exists():
        raise ReqFileNotFound

    with open(req_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Take package name from file
            package = re.split(r'[<>=!]', line)[0].strip()

            try:
                importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                raise PackagesNotFound

def main():
    print(f"Autorestore, version-{appversion}, build-{build}")
    try:
        check_requirements()
    except ReqFileNotFound as e:
        logger.warning(e)
        sys.exit(1)
    except PackagesNotFound as e:
        logger.warning(e)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unknown error!!!-{e}")
        sys.exit(1)

