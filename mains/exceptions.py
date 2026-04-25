#File contains custom exceptions for Autorestore programm


#1.All startup exceptions and configure exceptions inherit base class StartUpError

class StartUpError(Exception):
    def __init__(self, message="Unknown StartUp Error!"):
        super().__init__()
    pass

class IncorrectUser(StartUpError):
    def __init__(self):
        super().__init__("Error!!! Incorrect User! The programm is not running under the postgres user!")

class ReqFileNotFound(StartUpError):
    def __init__(self):
        super().__init__("Error!!! Couldn't find requirements file! Reinstall app or move requirements.txt file to .../Autorestore/requirements.txt")

class PackagesNotFound(StartUpError):
    def __init__(self):
        super().__init__("Error!!! Required Packages Not Found! Packages should be installed first or reinstalled!")


