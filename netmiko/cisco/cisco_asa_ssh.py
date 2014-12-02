from netmiko.ssh_connection import SSHConnection
from netmiko.netmiko_globals import MAX_BUFFER
import time

class CiscoAsaSSH(SSHConnection):

    def __init__(self, ip, username, password, secret='', port=22, device_type='', verbose=True):

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.secret = secret
        self.device_type = device_type

        if not verbose:
            self.establish_connection(verbose=False)
        else:
            self.establish_connection()

        # ASA must go into enable mode to disable_paging
        self.enable()
        self.disable_paging()
        self.find_prompt()


    def disable_paging(self, delay_factor=1):
        '''
        Cisco ASA paging disable 
        Ensures that multi-page output doesn't prompt for user interaction 
        (i.e. --MORE--)

        Must manually control the channel at this point.
        '''

        # ASA disables paging from configuration mode
        self.remote_conn.send("config term\n")
        time.sleep(1*delay_factor)
        self.remote_conn.send("pager 0\n")
        time.sleep(1*delay_factor)
        self.remote_conn.send("end\n")
        time.sleep(1*delay_factor)

        output = self.remote_conn.recv(MAX_BUFFER)

        return output


    def restore_paging(self):
        '''
        A paging requires a configuration change i.e. it is retained
        Restore the default paging after execution
        '''

        # Reset paging to 'pager 24' for ASA
        return self.send_config_set(['pager 24'])


    def enable(self, delay_factor=1):
        '''
        Enter enable mode

        Must manually control the channel at this point for ASA
        '''

        self.clear_buffer()
        self.remote_conn.send("\nenable\n")
        time.sleep(1*delay_factor)

        output = self.remote_conn.recv(MAX_BUFFER)
        if 'assword' in output:
            self.remote_conn.send(self.secret+'\n')
            self.remote_conn.send('\n')
            time.sleep(1*delay_factor)
            output += self.remote_conn.recv(MAX_BUFFER)

        return None


    def cleanup(self):
        '''
        Any needed cleanup before closing connection
        '''
        return self.restore_paging()