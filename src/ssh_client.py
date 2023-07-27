import paramiko
import logging
from conf_env import config as CFG
import re


class SSH_Client:

    def __init__(self):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, hostname, username, password=None):
        if password:
            logging.info(f"ssh {username}@{hostname} with password {password}")
            self._client.connect(
                hostname=hostname, username=username, password=password)
        else:
            logging.info(f"ssh {username}@{hostname} without password")
            self._client.connect(hostname=hostname, username=username)

        self._sftp = self._client.open_sftp()

    def exec(self, cmd):
        logging.debug(f"exec$ {cmd}")
        stdin, stdout, stderr = self._client.exec_command(cmd, get_pty=True)
        stdin.close()

        out = stdout.readlines()
        out_text = ''.join(out)
        logging.debug(f"STDOUT:\n{out_text}")
        err = stderr.readlines()
        err_text = ''.join(err)
        logging.debug(f"STDERR:\n{err_text}")

        return out, err

    def scp(self, source, target):
        print(self._sftp.put(source, target))

    def ls(self, path):
        cmd = f"ls -lh {path}"
        out, err = self.exec(cmd)
        return out

    def is_file_exists(self, path):
        cmd = f"if [ -f {path} ]; then echo 'True'; fi"
        out, err = self.exec(cmd)
        return len(out) > 0 and out[0].strip() == "True"

    def md5sum(self, path):
        out, err = self.exec(f"md5sum {path}")
        md5sum = None
        for l in out:
            if re.match(r"\S{32} ", l):
                md5sum = l[:32]
                break
        return md5sum

    def rrdtool_dump(self, path):
        cmd = f"rrdtool dump {path}"
        out, err = self.exec(cmd)
        return out

    def rrdtool_fetch(self, path, timestamp):
        cmd = f"rrdtool fetch {path} LAST --start {int(timestamp)}"
        out, err = self.exec(cmd)
        return out

    def close(self):
        self._sftp.close()
        self._client.close()


if __name__ == "__main__":
    client = SSH_Client()
    client.connect("192.168.10.20", "test", "test")
    print(client.ls("/"))
    client.close()
