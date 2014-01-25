svn2ftp
=======
## Purpose
### Short Story
This Python script automatically uploads SVN commits to a specified FTP location.

### Long Story
When converting my website to SVN, I wanted a tool to allow me to avoid manually
uploading changes to my FTP server. I found some solutions online, but most of
them weren't exactly what I was looking for, and many were too complicated.

I ended up making something from scratch using the changelist provided by SVN.
I had to figure out how to pass it the sensitive user information. I decided
to use a local file which the script would use to extract what it needed.
While it's not the most secure solution, it was good enough for my needs.
Feel free to fork this project and implement your own way of passing the ftp information.
An example solution could be to prompt the user each time a commit is pushed.

## Installation
This script is very simple to install.

1. Copy post-commit.bat and FTP.py to your svn\hooks\ folder.
2. Create a file that will contain the necessary FTP server information (each item should be on its own line, in the following order):
 - The full path location to the local SVN repo
 - The full URL to the FTP server
 - The username for the FTP server
 - The password for the FTP server
 - The root directory to upload the repo to (default should be './')
3. Modify FTP.py's SETTINGS_FILE variable to the full location of this file
4. Make a commit and see the script run.

### Example settings file
<pre>
E:\mysite
robbie.ftpserver.org
robbie
thepassword
public_html/
</pre>

## TODO
- Modify post-commit.bat so the command prompt closes automatically
 - Add a debug variable to make this easily configurable
- Fix bug when "adding" a file that already exists on the server