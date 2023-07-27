from utils import *
import logging
import os
import pytest
import re
from pathlib import PurePath
from ftplib import FTP
from ssh_client import SSH_Client
from conf_env import config as CFG
from time import time


perf_stat_root = PurePath(CFG['NAS']['RRD_PATH'])
required_perf_stat_files = {
    "CPU_Usage": PurePath("cpu-0/cpu-system.rrd"),
    "DiskUsage": PurePath("df-srv-dev-disk-by-uuid-19986e30-460f-46f1-bc3b-93f4969261bc/df_complex-used.rrd"),
    "MemoryUsage": PurePath("memory/memory-used.rrd"),
    "NetworkUsage": PurePath("interface-enp0s3/if_packets.rrd")
}


@pytest.fixture(scope="session")
def perfmeter():
    pm = PerformaceMeter()
    yield pm


@pytest.fixture(scope="function")
def file_path(test_name):
    file_path = PurePath(
        f"{CFG['NFS']['LOCAL_DIR_PATH']}/{test_name}_{rand.randrange(10000, 99999)}")
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture(scope="function")
def file_path_webdav(test_name):
    file_path = PurePath(
        f"{CFG['WEBDAV']['LOCAL_DIR_PATH']}/{test_name}_{rand.randrange(10000, 99999)}")
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture(scope="function")
def test_name(request):
    # test_10MB_file_upload[9-10] or test_10MB_file_upload[5-10]...
    test_name = request.node.name
    bracket_index = test_name.find('[')
    if bracket_index > 0:
        test_name = test_name[:bracket_index]
    return test_name


@pytest.fixture(scope="session")
def ftp():
    ftpcon = FTP(CFG['FTP']['ADDRESS'])
    ftpcon.login(user=CFG['FTP']['LOGIN'], passwd=CFG['FTP']['PASSWD'])
    logging.info("FTP Welcome message:" + ftpcon.getwelcome())

    yield ftpcon

    ftpcon.quit()


@pytest.fixture(scope="session")
def ssh():
    ssh = SSH_Client()
    ssh.connect(hostname=CFG['SSH']['ADDRESS'], username=CFG['SSH']
                ['LOGIN'], password=CFG['SSH']['PASSWD'])
    yield ssh
    ssh.close()


@pytest.fixture(scope="class")
def target_dir():
    return PurePath(CFG['FTP']['FULL_PATH'])


@pytest.fixture(scope="class")
def target_dir_scp():
    return PurePath(CFG['SSH']['FULL_PATH'])


@pytest.fixture(scope="class")
def target_dir_nfs():
    return PurePath(CFG['NFS']['FULL_PATH'])


@pytest.fixture(scope="class")
def target_dir_webdav():
    return PurePath(CFG['WEBDAV']['FULL_PATH'])


@pytest.fixture(scope="session", autouse=True)
def dump_perf_stat(ssh, perfmeter):
    sesstion_start_timestamp = time()
    yield
    rrd_text_parser = re.compile(r"(?P<timestamp>\d+): (?P<value>\s+)")
    for table_name, rrd_file in required_perf_stat_files.items():
        path_to_rrd_file = perf_stat_root.joinpath(rrd_file)
        rrd_text = ssh.rrdtool_fetch(
            path_to_rrd_file.as_posix(), sesstion_start_timestamp)
        for l in rrd_text:
            m = rrd_text_parser.match(l)
            if not m:
                continue
            if m.groupdict()['value'] == "-nan":
                continue
            perfmeter.insert_perf_stat(table_name, m.groupdict()[
                                       'timestamp'], m.groupdict()['value'])
