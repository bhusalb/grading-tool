from paramiko import SSHClient, AutoAddPolicy
import os


def connect():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hostname=os.getenv('MU_HOST'), port=22, username=os.getenv('PAW_PRINT'),
                   password=os.getenv('MU_PASSWORD'))

    return client
