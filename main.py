import subprocess
import paramiko
import re
import argparse


class GPUStatus():
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
        self.get_GPU_hosts()


    def get_GPU_hosts(self)->list:
        hosts_list = []
        for index in range(1, 31):
            if(index < 10):
                hosts_list.append('gpu0' + str(index)+'.doc.ic.ac.uk')
            else:
                hosts_list.append('gpu' + str(index)+'.doc.ic.ac.uk')
        self.hosts_list = hosts_list

    def check_GPU_status(self)->list:
        GPU_status_list = []
        for host in self.hosts_list:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(host, username=self.username, password=self.password)
            except Exception as e:
                print(host + ': ' + str(e))
            stdin, stdout, stderr = ssh.exec_command('nvidia-smi')
            status = "".join(stdout.readlines())
            # regex to find GPU status
            status = re.findall("\d+MiB / \d+MiB", status)
            if len(status) > 0:
                status = status[0]
                GPU_status_list.append(host+": "+status)
            ssh.close()
        return GPU_status_list


if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Check GPU status')
    parser.add_argument('-u', '--username', help='username', required=True)
    parser.add_argument('-p', '--password', help='password', required=True)
    args = parser.parse_args()
    gpu_status = GPUStatus(args.username, args.password)
    status_list = gpu_status.check_GPU_status()
    for status in status_list:
        print(status)
