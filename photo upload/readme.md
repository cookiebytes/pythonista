# photo_upload

photo_upload.py is written for [Pythonista](https://itunes.apple.com/us/app/pythonista-3/id1085978097 "Pythonista") on iOS. It's goal is to allow you to upload a photo or photos from the Pythonista extension in the Photos app to your own web server via SSH and copy the link[s] to your clipboard for posting on social media. The intention of this is so that you always maintain ownership of the photos that you take and share on social media.

For this to work you'll need SSH access to your web server and your SSH key. Copy the photo_upload.py script into Pythonista and edit lines 14-18 to fit your server.<br />
self.domain_name is used to specify your base domain: 'example.com'<br />
self.username is your SSH username<br />
self.port is your SSH port (Int)<br />
self.key_file is to specify the path to your SSH key file<br />
self.web_root is used to specify your web servers root folder. This is where photo_upload.py will create the folder structure to store your photos. It's typically something like: '/var/www'

Once you've got photo_upload.py setup you can run the script from the Pythonista extension in the Photos share sheet.

Enjoy!