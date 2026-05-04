#File contains custom exceptions for Autorestore programm


#1.All startup exceptions and configure exceptions inherit base class StartUpError

class StartUpError(Exception):
    def __init__(self, message):
        super().__init__()

class IncorrectUser(StartUpError):
    def __init__(self):
        super().__init__("Error!!! Incorrect User! The programm is not running under the postgres user!")

class ReqFileNotFound(StartUpError):
    def __init__(self):
        super().__init__("Error!!! Couldn't find requirements file! Reinstall app or move requirements.txt file to .../Autorestore/requirements.txt")

class PackagesNotFound(StartUpError):
    def __init__(self):
        super().__init__("Error!!! Required Packages Not Found! Packages should be installed first or reinstalled!")


#2. All modules exceptions inherit base class ModuleProblemError

class ModuleProblem(Exception):
    def __init__(self, message):
        super().__init__()

class DumperModuleMain(ModuleProblem):
    def __init__(self):
        super().__init__("Error!!! Dumper module indefinite error!")


class RestorerModuleMain(ModuleProblem):
    def __init__(self):
        super().__init__("Error!!! Restore module indefinite error!")


class RolemasterModuleMain(ModuleProblem):
    def __init__(self):
        super().__init__("Error!!! Rolemaster module indefinite error!")

