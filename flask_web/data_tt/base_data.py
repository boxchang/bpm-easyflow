from bases.database import tiptop_database
from bases.lib_database import getDBEnvFlag


class base_data(object):
    ttdb = None
    prod = False

    def __init__(self, prod=getDBEnvFlag()):
        self.ttdb = tiptop_database(prod)
        self.prod = prod