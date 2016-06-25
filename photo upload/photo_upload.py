import os
import time
import appex
import photos
import console
import paramiko
import clipboard

class photo_upload(object):
    def __init__(self):
        console.show_activity()
        
        # edit to make your own #
        self.domain_name = ''
        self.username = ''
        self.port = 22
        self.key_file = '' # ssh key file
        self.web_root = '' # your web servers root folder where you'll want to store your uploaded photos
        #                       #
        
        # dates
        self.year = str(time.strftime("%Y"))
        self.month = str(time.strftime("%m"))
        self.day = str(time.strftime("%d"))
        self.hour_min_sec = str(time.strftime("%H%M%S"))
        
        # variable setup
        self.file_count = 0
        self.link_list = []
        self.pkey = paramiko.RSAKey.from_private_key_file(self.key_file)
        self.file_name = '{0}-{1}@.jpg'.format(self.day, self.hour_min_sec) # the @ gets replaced with count
        self.remote_path = os.path.join(self.web_root, self.year, self.month)
        
        self.get_photo()
        self.architect()
        self.upload_logic()
        self.clippy()
        
    def get_photo(self):
        if appex.is_running_extension():
            p = appex.get_images_data()
            if p == None:
                print("No photo selected, exiting.")
                exit(0)
            else:
                self.p = p
        else:
            print("Please run as an extension in Photos, exiting.")
            exit(0)
            
    def architect(self):
        print('Creating directory...')
        
        cmd = 'mkdir -p {0}'.format(self.remote_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.domain_name, port=self.port, username=self.username, key_filename=self.key_file)
        client.exec_command(cmd)
        client.close
        
        print('directory created.')
    
    def upload_logic(self):
        if isinstance(self.p, list):
            for _ in self.p:
                self.upload_photo(_)
        else:
            self.upload_photo(self.p)
    
    def upload_photo(self, p):
        print('Uploading photo...')
        
        file_name = self.file_name.replace('@', str(self.file_count))
        file = os.path.join(self.remote_path, file_name)
        self.file_count += 1
        
        client = paramiko.Transport((self.domain_name, self.port))
        client.connect(username=self.username, pkey=self.pkey)
        
        sftp = paramiko.SFTPClient.from_transport(client)
        
        f = sftp.open(file, 'wb')
        f.write(p)
        f.close
        
        sftp.close()
        client.close()
        
        link = "http://{0}/{1}/{2}/{3}".format(self.domain_name, self.year, self.month, file_name)
        self.link_list.append(link)
        
        print("Photo uploaded.")
        print("Link: {0}".format(link))
    
    def clippy(self):
        print("Upload complete, the link[s] have been copied to the clipboard")
        
        link_string = '\n'.join(self.link_list)
        clipboard.set(link_string)
        
    
    
photo_upload()
