from bases.database import bpm_database
from bases.lib_database import getDBEnvFlag


class base_data(object):
    bpmdb = None
    prod = False

    def __init__(self, prod=getDBEnvFlag()):
        self.bpmdb = bpm_database(prod)
        self.prod = prod