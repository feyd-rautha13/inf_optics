# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Thu Nov 15 15:06:32 2018
Modified on 
File description: SSH interface for groove
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"


import paramiko
import time

class SSH(object):
    def __init__(self, host='172.29.150.195', port = 8022, username = 'administrator' , password = 'e2e!Net4u#'):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self._host, self._port , self._username, self._password)

        self.shell = self.ssh.invoke_shell()
    
    def SSH_close(self):
        self.ssh.close()
        print(self.__class__.__name__ + ' connection is closed.')
    
    def write(self, command):
        command = str(command)+'\n'
        self.shell.send(command)
        time.sleep(0.5)
    
    def read_raw(self, buffer_size = 9999):
        if self.ready_to_read() == True:
            data = self.shell.recv(buffer_size)
        else:
            print('nothing to read!')
        
        try:
            while self.ready_to_read == True:
                data = data + self.shell.recv(buffer_size)
            return data
        except:
            print('no more data')
    
    def ready_to_read(self):
        return self.shell.recv_ready()
    
    def clear_buffer(self):
        if self.ready_to_read() == True:
            self.read_raw()
        else:
            pass
    
    def inspection(self, section):      
        data = self.read_raw().decode()
 
        if section in data:
            return True
        else:
            return False

   
class groove_cli(SSH):
    def __init__(self, host = '172.29.150.195',port = 8022, username = 'administrator' , password = 'e2e!Net4u#'):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        
        self._ssh_prompt = '~$ '
        self._cli_prompt = '> '
            
        SSH.__init__(self, self._host, self._port, self._username, self._password)
        time.sleep(2)
        
        if self.inspection(self._ssh_prompt):
            print('ssh connection successful!')
        else:
            print('ssh connection failed!')
            
        
        self.clear_buffer()
        self.write('\n')
        self.write("client")
        
        if self.inspection(self._cli_prompt):
            print ('Login to Groove CLi successful!')
        else:
            print('login failed!')
    
    def close_session(self):
        '''
        close ssh connection
        '''
        self.SSH_close()
        
    
    def cli_interactive_mode(self, cmd = 'disabled'):
        cmd = "set cli-config interactive-mode " + cmd
        self.clear_buffer()
        self.write(cmd)
        self.write('y')
    
    @property
    def show_inventory(self):
        '''
        show inventory
        '''
        self.clear_buffer()
        self.write('show inventory')
        invenroty = self.read_raw().decode()
        print (invenroty)
        
class groove_Hal(SSH):
    def __init__(self, host = '172.29.150.195',port = 8022, username = 'administrator' , password = 'e2e!Net4u#'):
        
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        
        self._ssh_prompt = '~$'
        self._hal_prompt = '/home/administrator# '
        self._hal_prompt_2 = 'HAL>'
        self._hal_username = 'su'
        self._hal_password = 'cosh1$'
        self._hal_path = 'cd /usr/local/bin'
        self._hal_paht_2 = './HAL'
        
        print('start to connect to server..')
        SSH.__init__(self, self._host, self._port, self._username, self._password) 
        
        time.sleep(1)

        if self.inspection(self._ssh_prompt):
            print('ssh connection successful!')
        else:
            print('ssh connection failed!')
            self.close_session()
        
        time.sleep(0.5)
        print ('start to connect to HAL.')
        self.write('\n')
        
        self.write(self._hal_username)
        
        if self.inspection('Password'):
            print('enter password now..')
        else:
            pass
        
        self.write(self._hal_password)
        time.sleep(0.5)
        if self.inspection(self._hal_prompt):
            print ('Login in super user successfull.')
        else:
            print('Fail!')
        
        self.write(self._hal_path)
        time.sleep(1)
        self.write(self._hal_paht_2)
        time.sleep(1)
        self.write('\n')
        if self.inspection(self._hal_prompt_2):
            print ('Login HAL successfull!')
        else:
            print('Fail!')

            
    def close_session(self):
        '''
        close ssh connection
        '''
        self.SSH_close()
        
        
        
        
        
