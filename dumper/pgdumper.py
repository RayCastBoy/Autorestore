#This module is used for autodumping dbases with some extra options
#It works in conjunction with pg_dump utility and dependencer module
#Can make a dbase dump with all dependences for restore on another cluster (looks like you use pgdumpall, but
#directly for one dbase or just few databases, but not for a whole cluster)

def dumper_entry(): #entry point function
    return True
    #global exception is DumperModuleMainError
