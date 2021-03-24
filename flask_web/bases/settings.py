#現有營運中心DB Config
TEST_COM_LIST = {"eaglesky": "s21", "csi": "s22", "cyber": "s26", "fldcc": "s27", "d6part2": "d6part2"}
PROD_COM_LIST = {"eaglesky": "eaglesky", "csi": "csi", "cyber": "cyber", "fldcc": "fldcc", "double6": "double6", "d6part2": "d6part2"}

#正式環境(True)或測試環境(False)
PRODFLAG = True

#TIPTOP預設正式區Connection帳號
TT_PROD_DB_USER = "eaglesky"
TT_PROD_DB_PW = "eaglesky"
TT_PROD_DB_TNS = "10.77.9.7:1521/topprod"

#TIPTOP預設測試區Connection帳號
TT_TEST_DB_USER = "s21"
TT_TEST_DB_PW = "s21"
TT_TEST_DB_TNS = "10.77.9.101:1521/topprod"

#BPM預設正式區Connection帳號
BPM_PROD_DB_SERVER = "tcp:10.77.9.4"
BPM_PROD_DATABASE = "EFGP"
BPM_PROD_DB_USER = "sa"
BPM_PROD_DB_PW = "Sql#dsc2019"

#BPM預設正式區Connection帳號
BPM_TEST_DB_SERVER = "tcp:10.77.9.104"
BPM_TEST_DATABASE = "EFGP"
BPM_TEST_DB_USER = "sa"
BPM_TEST_DB_PW = "Sql#dsc2019"



