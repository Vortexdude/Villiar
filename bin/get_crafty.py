import json
import os
import stat
import paramiko
import tarfile
import datetime as dt

CONF_FILE = 'conf.json'


class Utils:
    @staticmethod
    def read_json(file):
        with open(file, 'r') as f:
            return json.load(f)

    @staticmethod
    def archive(files, archive_name="/tmp/crafty.tar.gz"):
        with tarfile.open(archive_name, 'w:gz') as tar:
            for file in files:
                tar.add(file, arcname=os.path.basename(file))
        return archive_name

    @staticmethod
    def check_file_permission(file, mode='0a600'):
        if not os.path.isfile(file):
            return False
        ssh_file_permission = oct(
            stat.S_IMODE(
                os.stat(file, follow_symlinks=False).st_mode
            )
        )
        if mode != ssh_file_permission:
            return False
        return True


class CraftMan(Utils):
    def __init__(self, conf_file):
        self.data = self.read_json(conf_file)
        self.use_password = False
        self.sftp_client = None
        archive_base_name = "crafty"
        _date_post_fix = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        self.archive_file_name = f"{archive_base_name}{_date_post_fix}.tar.gz"

    def run(self):
        for server in self.data.get('servers', []):
            if server['ssh_key']:
                if self.check_file_permission(server['ssh_key']):
                    print("[ERROR] with the file")
                    continue
            self.establish_ssh_connection(**{k: v for k, v in server.items() if k.startswith("ssh_")})

            archive_path = os.path.join("/tmp/", self.archive_file_name)

            archive_path = self.archive(server['local_directories'], archive_path)
            destination = os.path.join(server['remote_path'], self.archive_file_name)
            self.send_file(source=archive_path, dest=destination)

    def establish_ssh_connection(self, ssh_username=None, ssh_password=None, ssh_host=None, ssh_key=None):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.use_password:
            client.connect(ssh_host, username=ssh_username, password=ssh_password)
        else:
            pkey = paramiko.Ed25519Key.from_private_key_file(ssh_key)
            client.connect(ssh_host, username=ssh_username, pkey=pkey)

        self.sftp_client = client.open_sftp()

    def send_file(self, source, dest):
        self.sftp_client.put(source, dest)


cm = CraftMan(CONF_FILE)
cm.run()




