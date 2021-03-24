from bases.settings import *

# 取得環境正式或測試
def getDBEnvFlag():
    return PRODFLAG


# 取得營運中心DB Schema
def getDBSchema(com_name, prod=getDBEnvFlag()):
    com_name = str(com_name).lower()
    return PROD_COM_LIST[com_name] if prod else TEST_COM_LIST[com_name]


# 取得現有營運中心
def getComList():
    com_list = [key for key in PROD_COM_LIST] if PRODFLAG else [key for key in TEST_COM_LIST]
    return com_list