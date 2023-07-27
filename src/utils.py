import hashlib
import os
import sqlite3
import time
import random as rand
import logging
from conf_env import config as CFG


def get_file_with_size_mb(size):
    file_data = os.urandom(size*1024*1024)
    return file_data


def get_md5sum(file_data):
    return hashlib.md5(file_data).hexdigest()


def put_file_to_directory(file_data, file_path):
    fh = open(file_path, 'wb')
    fh.write(file_data)
    fh.close()

    logging.info(f"Save file '{file_path}'")


def wait_for_file(ssh_client, file_path, timeout=150):
    logging.debug(f"Wait for file {file_path} with timeout {timeout} seconds.")

    time_start = time.time()
    while not ssh_client.is_file_exists(file_path):
        if time.time() - time_start > timeout:
            return False
        time.sleep(0.05)
    logging.debug(
        f"File {file_path} is appears in {time.time() - time_start} seconds.")
    return True


class PerformaceMeter:

    def __init__(self):
        self._init_db_connection(CFG['DIAGNOSTIC']['PERF_STAT_DB'])

    def _init_db_connection(self, db_path):
        should_init_db = not os.path.exists(db_path)

        self._db_con = sqlite3.connect(db_path)
        self._db_cur = self._db_con.cursor()

        if should_init_db:
            self._db_cur.execute('''
                CREATE TABLE OperationTime (
                test_name TEXT,
                start_time REAL,
                end_time REAL,
                config_id INTEGER)''')
            self._db_cur.execute('''
                CREATE TABLE NAS_Configuration (
                config_id INTEGER,
                description TEXT)''')
            self._db_cur.execute('''
                CREATE TABLE CPU_Usage (
                time REAL,
                load TEXT)''')
            self._db_cur.execute('''
                CREATE TABLE MemoryUsage (
                time REAL,
                load TEXT)''')
            self._db_cur.execute('''
                CREATE TABLE DiskUsage (
                time REAL,
                load TEXT)''')
            self._db_cur.execute('''
                CREATE TABLE NetworkUsage (
                time REAL,
                load TEXT)''')
            self._db_cur.execute('''
                CREATE TABLE SysLogs (
                time REAL,
                log_message TEXT)''')

    def estimate_func(self, test_name, ssh, target_file, func, *args):
        start_time = time.time()
        func(*args)
        assert wait_for_file(ssh, target_file)

        end_time = time.time()
        func_time = end_time - start_time
        logging.info(f"Test {test_name} - {func_time}")

        self._db_cur.execute("insert into OperationTime values (?, ?, ?, ?)",
                             (test_name, start_time, end_time, 0))
        self._db_con.commit()

    def insert_perf_stat(self, table_name, timestamp, value):
        self._db_cur.execute("insert into ? values (?, ?)",
                             (table_name, timestamp, value))
