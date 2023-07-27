import configparser
import os
import logging


DEFAULT_CONFIG = """
[NAS]
RRD_PATH=PERF_STAT_ROOT=/var/lib/rrdcached/db/localhost
CONFIG_ID=DEFAULT
CONFIG_DESCRIPTION=No description

[DIAGNOSTIC]
ROOT_PATH=~/nas_tests/test_logs/
PERF_STAT_DB=~/nas_tests/test_logs/perf_stat.db

[FTP]
PATH=/VK_Share
FULL_PATH=/srv/dev-disk-by-uuid-19986e30-460f-46f1-bc3b-93f4969261bc/VK_Share
LOGIN=test
PASSWD=test
ADDRESS=10.0.2.5

[NFS]
FULL_PATH=/srv/dev-disk-by-uuid-19986e30-460f-46f1-bc3b-93f4969261bc/Music
LOCAL_DIR_PATH=/home/vkovalev/nfs_music/

[WEBDAV]
FULL_PATH=/srv/dev-disk-by-uuid-5c2aebc7-baad-45ca-a418-703fda90f8db/webdav/data
LOCAL_DIR_PATH=/home/vkovalev/webdavtest

[SSH]
ADDRESS=10.0.2.5
LOGIN=test
PASSWD=test
"""

config = configparser.ConfigParser()
conf_path = os.environ.get("NAS_TEST_CONFIG")
if conf_path:
    config.read(conf_path)
else:
    config.read_string(DEFAULT_CONFIG)

logging.info(f"Test environment config:\n{config}")
