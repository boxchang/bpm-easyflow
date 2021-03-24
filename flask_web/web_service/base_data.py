from bases.database import tiptop_database
from bases.lib_database import getDBEnvFlag


class base_data(object):
    ttdb = None
    prod = False
    bpm_url = ""

    def __init__(self, prod=getDBEnvFlag()):
        self.ttdb = tiptop_database(prod)
        self.prod = prod
        if prod:
            bpm_url = "10.77.9.3"
        else:
            bpm_url = "10.77.9.103"