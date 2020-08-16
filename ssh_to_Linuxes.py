#!/usr/bin/python3

import paramiko

username = "administrator"
password = "*********"
Nessus_UserPass = "*********"
AddNewUser = "useradd -m -d /home/test -g wheel -p $(openssl passwd -1 '*********') -s /bin/bash test"
ChangPassword = "usermod -l cyber -m -d /home/cyber -p $(openssl passwd -1 '*********') administrator"
AddNessusUser1 = '/opt/nessus/sbin/nessuscli adduser cyber'
AddNessusUser2 = '/opt/nessus/sbin/nessuscli adduser admin'
RemoveNessusUser = '/opt/nessus/sbin/nessuscli rmuser administrator'
commands = [ChangPassword, AddNessusUser1, AddNessusUser2, RemoveNessusUser]


class SSH:
    def __init__(self, host, username, password, nessus_pass, command):
        self.host = host
        self.username = username
        self.password = password
        self.nessus_pass = nessus_pass
        self.command = f"sudo -S -p '' {command}"
        self.status = None

    def ssh_connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.host,
                                username=self.username, password=self.password)
        except Exception as err:
            print(f"{err}: {self.host}")
        else:
            print(f"Connected to {self.host}")
            self.status = True
        return self.status

    def command_exec(self):
        if self.status:
            stdin, stdout, stderr = self.client.exec_command(
                self.command)
            if "adduser" in self.command:
                print(f"adding new Nessus user in {self.host}")
                stdin.write(f"{self.password}\n")
                stdin.write(self.nessus_pass + "\n")
                stdin.write(self.nessus_pass + "\n")
                stdin.write("y\n")
                stdin.write("\n")
                stdin.write("y\n")
                stdin.flush()
                ret = stdout.read()
                print("\nOUTPUT\n-----------------\n"+str(ret))
                print(ret)
                err = stderr.read()
                print("\nERROR\n------------------\n"+str(err))

            elif "rmuser" in self.command:
                print(f"removing administrator from {self.host}")
                stdin.write(f"{self.password}\n")
                stdin.write("y\n")
                stdin.flush()
                ret=stdout.read()
                print("\nOUTPUT\n-----------------\n"+str(ret))
                print(ret)
                err = stderr.read()
                print("\nERROR\n------------------\n"+str(err))


            else:
                stdin.write(f"{self.password}\n")
                stdin.flush()
                print("OUTPUT\n--------------------")
                for line in stdout:
                    print(line)
                print("ERROR\n---------------------")
                for line in stderr:
                    print(line)

            # TODO check the command is executed!

    def close_connection(self):
        self.client.close()
        print(f"connection to {self.host} closed!")


for i in range(11, 41):
    for command in commands:
        command1 = SSH(f"10.77.8.{i}", username, password, Nessus_UserPass, command)
        command1.ssh_connect()
        command1.command_exec()
        command1.close_connection()
