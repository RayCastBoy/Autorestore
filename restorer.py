import questionary
from loguru import logger
import sys
import os
import subprocess
#This module is used for autorestoring dbases with some extra options
#It works in conjunction with pg_restore or ?psql? utility and dependencer module
#Can make a dbase restore with all dependences
#directly for one dbase or just few database

#global exception is RestorerModuleMainError

def simple_restore():
    print("=== Set up simple restorer ===")

    database_name = questionary.text(
        "What database need to be restored?:",
        validate = lambda x: (
            True if x.strip() else "Database name could not be empty!!!"
        ),
    ).ask()


    if not database_name:
        print("Canceled")
        return

    dump_path = questionary.path(
        "Set a path to a dump folder/file (Can use autocomplete):",
        only_directories=False,
        valide = lambda x: (
            True if os.path.exists(x) else "File or folder could not exists!"
        ),
    ).ask()

    if not dump_path:
        print("Canceled")
        return

    restore_mode = questionary.select(
        "Set up restore mode:",
        choices=[
            "All (schema + data), default setting",
            "Only schema",
            "Only data",
        ],
    ).ask()

    if not restore_mode:
        print("Canceled")
        return

    cpu_cores = os.cpu_count()

    print(f"You can use <= jobs {cpu_cores} to restore.")

    jobs_mode = questionary.text(
        "Set up amount of jobs (default 1):",
        default = "1",
        validate = lambda x: (
            True if x.isdigit() and x <= cpu_cores else "Set up correct amount of jobs"
        ),
    ).ask()

    if not jobs_mode:
        print("Canceled")
        return

    cmd = ["pg_restore", "-v"]

    cmd.extend(["-d", database_name])
    cmd.extend(["-j", jobs_mode])

    if "Only schema" in restore_mode:
        cmd.append("-s") # --schema-only key
    elif "Only data" in restore_mode:
        cmd.append("-d") # --data-only key

    cmd.append(dump_path)

    print("\nFinal command is:")
    print(" ".join(cmd))

    confirm = questionary.confirm(
        "Do you want to continue?", default=False
    ).ask()

    if not confirm:
        print("Canceled")
        return

    print("Restoring from dump...")
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\nSuccess! Restored from dump. Exit code: {result.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"\nSomething went wrong restoring from dump: {e}")
        logger.warning(e)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\nSomething went wrong restoring from dump: {e}")
        logger.warning(e)
        sys.exit(1)
    except Exception as e:
        print(f"\nSomething went wrong restoring from dump: {e}")
        logger.warning(e)
        sys.exit(1)

def full_restore():
    return True

def restorer_entry(): #entry point function
    actions = {
        "Standart database restore" : simple_restore,
        "Restore database with dependencies" : full_restore
    }

    while True:
        solution = questionary.select(
            "What type of restore do you want to do?",
            choices=[*actions.keys(), "Back"]).ask()

        if solution == "Back":
            return None

        action_func = actions.get(solution)
        try:
            action_func()
            return None
        except Exception as e:
            print(e)
            logger.warning(e)
            sys.exit(1)