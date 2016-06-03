svn2ftp
=======
## Features
When converting my website to SVN, I wanted a tool to allow me to avoid manually
uploading commit changes to my FTP server. I found some solutions online, but most of
them weren't exactly what I was looking for, and many were too complicated.
I ended up making something from scratch using the changelist provided by SVN.

This tool automatically uploads all new and modified files to the server, and deletes
any file or folder that was removed from the SVN repo. The script runs when a commit completes.

## Installation
This script is very simple to install.

1. Copy post-commit.bat and FTP.py to your svn\hooks\ folder.
2. Modify the following variables in FTP.py
 - LOCAL        - The full path location to the SVN working copy (the folder containing trunk)
 - FTP_SERVER   - The full URL to the server to upload to
 - REMOTE_ROOT  - The root directory on the server to upload the repo to
3. Make a commit, enter your username and password, and see the script run.

## Preventing files from uploading
Sometimes you have files that you want to be version controlled but you don't want
on your FTP server. You can let the script know to ignore these files by creating
a file called .svnignore in the trunk folder found in your main working copy folder. 
Files or folders listed in this file will be ignored. Each new file or folder should
be on its own line and spelled correctly. All files or folders should be written 
relative to the folder containing the svnignore file. Files should include their extension. 
Folders are indicated with a / at the end of the name. You can add comments by 
starting the line with a #. The ignore file itself is automatically ignored.

## TODO
- Modify post-commit.bat so the command prompt closes automatically
 - Add a debug variable to make this easily configurable
- Fix bug when "adding" a file that already exists on the server
 - This would be a sign something is out of sync and maybe the script should abort either way