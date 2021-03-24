import pyodbc
import cx_Oracle

from bases.oracle_dir import ORACLE_LIB_DIR
from bases.settings import *

cx_Oracle.init_oracle_client(lib_dir=ORACLE_LIB_DIR)


class tiptop_database(object):
    conn = None
    prod = False

    def __init__(self, prod=False):
        self.prod = prod

    def create_connection(self):
        try:
            if self.conn is None:
                if self.prod:
                    dsn_tns = TT_PROD_DB_TNS
                    self.conn = cx_Oracle.connect(user=TT_PROD_DB_USER, password=TT_PROD_DB_PW, dsn=dsn_tns)
                else:
                    dsn_tns = TT_TEST_DB_TNS
                    self.conn = cx_Oracle.connect(user=TT_TEST_DB_USER, password=TT_TEST_DB_PW, dsn=dsn_tns)

            return self.conn
        except pyodbc.Error as e:
            print(e)

        return None

    def execute_sql(self, sql):
        conn = self.create_connection()
        cur = self.conn.cursor()
        cur.execute(sql)
        conn.commit()

    def execute_select_sql(self, sql):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        return cur

    def close_connection(self):
        self.conn.close()


class bpm_database(object):
    conn = None
    prod = False

    def __init__(self, prod=False):
        self.prod = prod

    def create_connection(self):
        try:
            if self.conn is None:
                if self.prod:
                    server = BPM_PROD_DB_SERVER
                    database = BPM_PROD_DATABASE
                    username = BPM_PROD_DB_USER
                    password = BPM_PROD_DB_PW
                else:
                    server = BPM_TEST_DB_SERVER
                    database = BPM_TEST_DATABASE
                    username = BPM_TEST_DB_USER
                    password = BPM_TEST_DB_PW

                conn_str = 'DRIVER={SQL Server};SERVER={' + server + '};DATABASE={' + database + '};' \
                           'UID={' + username + '};PWD={' + password + '}'
                self.conn = pyodbc.connect(conn_str)

            return self.conn
        except pyodbc.Error as e:
            print(e)

        return None

    def execute_sql(self, sql):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    def execute_select_sql(self, sql):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        return cur

    def close_connection(self):
        self.conn.close()