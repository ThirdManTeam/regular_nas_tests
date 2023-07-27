import pytest
import logging
import random as rand
from pathlib import PurePath
from utils import *
from conf_env import config as CFG


class TestNFS:

    def test_nfs_10MB_file_upload(self, perfmeter, test_name, target_dir_nfs, file_path, ssh):
        file_name = file_path.name
        target_file = target_dir_nfs / file_name

        file_data = get_file_with_size_mb(10)
        md5sum_source = get_md5sum(file_data)
        perfmeter.estimate_func(
            test_name, ssh, target_file, put_file_to_directory, file_data, file_path)

        md5sum_target = ssh.md5sum(target_file)
        assert md5sum_source == md5sum_target

    def test_nfs_500MB_file_upload(self, perfmeter, test_name, target_dir_nfs, file_path, ssh):
        file_name = file_path.name
        target_file = target_dir_nfs / file_name

        file_data = get_file_with_size_mb(500)
        md5sum_source = get_md5sum(file_data)
        perfmeter.estimate_func(
            test_name, ssh, target_file, put_file_to_directory, file_data, file_path)

        md5sum_target = ssh.md5sum(target_file)
        assert md5sum_source == md5sum_target


class TestWebDAV:

    def test_webdav_10MB_file_upload(self, perfmeter, test_name, target_dir_webdav, file_path_webdav, ssh):
        file_name = file_path_webdav.name
        target_file = target_dir_webdav / file_name

        file_data = get_file_with_size_mb(10)
        md5sum_source = get_md5sum(file_data)
        perfmeter.estimate_func(test_name, ssh, target_file,
                                put_file_to_directory, file_data, file_path_webdav)

        md5sum_target = ssh.md5sum(target_file)
        assert md5sum_source == md5sum_target

    def test_webdav_500MB_file_upload(self, perfmeter, test_name, target_dir_webdav, file_path_webdav, ssh):
        file_name = file_path_webdav.name
        target_file = target_dir_webdav / file_name

        file_data = get_file_with_size_mb(500)
        md5sum_source = get_md5sum(file_data)
        perfmeter.estimate_func(test_name, ssh, target_file,
                                put_file_to_directory, file_data, file_path_webdav)

        md5sum_target = ssh.md5sum(target_file)
        assert md5sum_source == md5sum_target


class TestFTP:

    def test_ftp_10MB_file_upload(self, ftp, perfmeter, test_name, ssh, target_dir):
        file_data = get_file_with_size_mb(10)
        md5sum_source = get_md5sum(file_data)

        file_name = PurePath('test_ftp_file_10MB.bin')
        source_file = PurePath('/tmp') / file_name
        target_path = target_dir / file_name

        with open(source_file, 'wb') as fh:
            fh.write(file_data)
            fh.close()

        with open(source_file, 'rb') as fh:
            ftp.cwd(CFG['FTP']['PATH'])
            logging.info(f"Current path: {ftp.pwd()}")
            logging.info(f"List before operation: {list(ftp.mlsd())}")
            perfmeter.estimate_func(
                test_name, ssh, target_path, ftp.storbinary, f"STOR {file_name}", fh)
            logging.info(f"List after operation: {list(ftp.mlsd())}")

        md5sum_target = ssh.md5sum(target_path)
        assert md5sum_source == md5sum_target

    def test_ftp_500MB_file_upload(self, ftp, perfmeter, test_name, ssh, target_dir):
        file_data = get_file_with_size_mb(500)
        md5sum_source = get_md5sum(file_data)

        file_name = PurePath('test_ftp_file_500MB.bin')
        source_file = PurePath('/tmp') / file_name
        target_path = target_dir / file_name

        with open(source_file, 'wb') as fh:
            fh.write(file_data)
            fh.close()

        with open(source_file, 'rb') as fh:
            ftp.cwd(CFG['FTP']['PATH'])
            logging.info(f"Current path: {ftp.pwd()}")
            logging.info(f"List before operation: {list(ftp.mlsd())}")
            perfmeter.estimate_func(
                test_name, ssh, target_path, ftp.storbinary, f"STOR {file_name}", fh)
            logging.info(f"List after operation: {list(ftp.mlsd())}")

        md5sum_target = ssh.md5sum(target_path)
        assert md5sum_source == md5sum_target


class TestSCP:

    def test_scp_10MB_file_upload(self, ssh, perfmeter, test_name, target_dir_scp):
        file_data = get_file_with_size_mb(10)
        md5sum_source = get_md5sum(file_data)
        logging.info(f"MD5SUM source: {md5sum_source}")

        file_name = PurePath('test_ssh_file_10MB.bin')

        target_file = target_dir_scp / file_name
        source_file = PurePath('/tmp') / file_name

        with open(source_file, 'wb') as fh:
            fh.write(file_data)
            fh.close()

        ssh.ls(target_dir_scp)
        perfmeter.estimate_func(test_name, ssh, target_file, ssh.scp, str(
            source_file), str(target_file))
        ssh.ls(target_dir_scp)

        md5sum_target = ssh.md5sum(target_file)
        assert md5sum_source == md5sum_target

    def test_scp_500MB_file_upload(self, ssh, perfmeter, test_name, target_dir_scp):
        file_data = get_file_with_size_mb(500)
        md5sum_source = get_md5sum(file_data)
        logging.info(f"MD5SUM source: {md5sum_source}")

        file_name = PurePath('test_ssh_file_500MB.bin')

        target_file = target_dir_scp / file_name
        source_file = PurePath('/tmp') / file_name

        with open(source_file, 'wb') as fh:
            fh.write(file_data)
            fh.close()

        ssh.ls(target_dir_scp)
        perfmeter.estimate_func(test_name, ssh, target_file, ssh.scp, str(
            source_file), str(target_file))
        ssh.ls(target_dir_scp)

        md5sum_target = ssh.md5sum(target_file)
        assert md5sum_source == md5sum_target
