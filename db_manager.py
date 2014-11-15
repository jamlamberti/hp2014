#!/usr/bin/python
import MySQLdb
import logging
from borg import Borg

class CredentialManager(Borg):
    # WARNING: This is using a monostate pattern
    def __init__(self, host, user, password, name, port=3306):
        Borg.__init__(self)
        self.db_host = host
        self.db_user = user
        self.db_pass = password
        self.db_name = name
        self.port = port
class DatabaseAccess(object):
    def __init__(self, db_host, db_user, db_pass, db_name, port=3306):
        self.creds = CredentialManager(db_host, db_user, db_pass, db_name, port)
        self.conn = None
        self.cursor = None
    def __connect(self):
        try:
            db = MySQLdb.connect(host=self.creds.db_host, port=self.creds.port, user=self.creds.db_user, passwd=self.creds.db_pass, db=self.creds.db_name)
        except MySQLdb.Error, e:
            if (e.args[0] == 1049): # Unknown database
                logging.error("DB doesn't exist")
                raise e
        except MySQLdb.Error, e:
            logging.error('Database error %d: %s' % (e.args[0], e.args[1]))
            raise
        return db

    def connect(self):
        if self.conn is not None or self.cursor is not None:
            self.close()
        self.conn = self.__connect()
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None
            if self.conn is not None:
                self.conn.commit()
                self.conn.close()
                self.conn = None
                logging.debug("Closed MySQLdb connection...")

        except MySQLdb.OperationalError, ex:
            logging.warning("Database connection already gone")            

    def execute(self,sql,*args):
        try:
            self.cursor.execute(sql,args)
            self.conn.commit()
        except MySQLdb.OperationalError, ex:
            logging.error("database connection went away, reconnecting...")
            self.connect()
            logging.warning("Trying query again...")
            self.cursor.execute(sql,args)
            self.conn.commit()
        except MySQLdb.Error, ex:
            self.conn.rollback()
            raise
        r = self.cursor.fetchone()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return r

    def get_next_result(self):
        r = self.cursor.fetchone()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return r

    def execute_all(self,sql,*args):
        try:
            self.cursor.execute(sql,args)
            self.conn.commit()
        except MySQLdb.OperationalError, ex:
            logging.error("database connection went away, reconnecting...")
            self.connect()
            logging.warning("Trying query again...")
            self.cursor.execute(sql,args)
            self.conn.commit()
        except MySQLdb.Error as ex:
            self.conn.rollback()
            raise
        r = self.conn.fetchall()
        self.lr_id = self.cursor.lastrowid
        self.conn.commit()
        return r

def test_connect():
    da = DatabaseAccess('localhost', 'root', 'root', 'grader')
    da.connect()
if __name__ == "__main__":
    test_connect()
