import questionary
#import psutil unknown import
import sys
import importlib.metadata
from re import split as re_split
from loguru import logger
from pathlib import Path
from getpass import getuser
from dumper.pgdumper import dumper_entry
from restorer import restorer_entry
from rolemaster import rolemaster_entry
from mains.exceptions import ReqFileNotFound, PackagesNotFound, IncorrectUser, DumperModuleMain, RestorerModuleMain, RolemasterModuleMain
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
            package = re_split(r'[<>=!]', line)[0].strip()

            try:
                importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                raise PackagesNotFound

def module_choice(): #ask user to choose what to do and call required module. Allow come back to menu from module
    actions = {
        "Dump database(s)": dumper_entry,
        "Restore database(s)": restorer_entry,
        "Configure role(s)": rolemaster_entry
    }

    while True:
        solution = questionary.select(
            "What do you want to do?",
            choices=[*actions.keys(), "Exit programm"]).ask()


        if solution == "Exit programm" or solution is None:
            print("Goodbye")
            break

        action_func = actions.get(solution)
        if action_func:
            try:
                action_func()
            except (DumperModuleMain, RestorerModuleMain, RolemasterModuleMain) as e:
                print("Some module error! Programm is stopping")
                logger.warning(e)
                sys.exit(1)


def main(): #entry point function
    print(f"Autorestore, version-{appversion}, build-{build}")
    try:
        check_requirements()
    except ReqFileNotFound as e:
        print("Couldn't find requirements file for check\n"
        "Reinstall app or move requirements.txt file to .../Autorestore/requirements.txt")
        logger.warning(e)
        sys.exit(1)
    except PackagesNotFound as e:
        print("Some packages not found\n"
        "DO: 1) cd to ../Autorestore\n"
        "2) ../Autorestore/.venv/bin/pip install -r requirements.txt\n")
        logger.warning(e)
        sys.exit(1)
    except Exception as e:
        print("Something went wrong! Program is stopping")
        logger.exception(f"Unknown error!!!-{e}")
        sys.exit(1)
    print("Packages found")
    try:
        check_user()
    except IncorrectUser as e:
        print(e)
        logger.warning(e)
        sys.exit(1)
    except Exception as e:
        print("Something went wrong! Program is stopping")
        logger.exception(f"Unknown error!!!-{e}")
        sys.exit(1)
    try:
        module_choice()
        print("Everything is done")
    except Exception as e:
        print("Something went wrong! Program is stopping")
        logger.exception(f"Unknown error!!!-{e}")
        sys.exit(1)