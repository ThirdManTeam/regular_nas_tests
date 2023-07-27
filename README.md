# regular_tests



## Tests installation

...

## NAS configuration

..

## Tests configuration

```
[NAS]
RRD_PATH=/var/lib/rrdcached/db/localhost
CONFIG_ID=DEFAULT
CONFIG_DESCRIPTION=No description

[DIAGNOSTIC]
ROOT_PATH=/path/to/test_logs/
PERF_STAT_DB=/path/to/perf_stat.db

[FTP]
PATH=/home/test
FULL_PATH=/home/test
LOGIN=test
PASSWD=test
ADDRESS=192.168.10.10

[NFS]
FULL_PATH=/absolute/path/to/nfs/on/nas
LOCAL_DIR_PATH=/absolute/path/to/nfs/on/client

[WEBDAV]
FULL_PATH=/absolute/path/to/webdav/on/nas
LOCAL_DIR_PATH=/absolute/path/to/webdav/on/client

[SSH]
ADDRESS=192.168.10.20
LOGIN=test
PASSWD=test
FULL_PATH=/absolute/path/to/scp/on/nas
```

## Run tests

```
NAS_TEST_CONFIG=x86nas_conf.ini pytest src/test_simple.py --log-cli-level=INFO --count=50
```

## Results

...
