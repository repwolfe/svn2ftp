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
 - LOCAL        - The full path location to the local SVN repo
 - FTP_SERVER   - The full URL to the FTP server
 - REMOTE_ROOT  - The root directory to upload the repo to
3. Make a commit, enter your username and password, and see the script run.

## TODO
- Modify post-commit.bat so the command prompt closes automatically
 - Add a debug variable to make this easily configurable
- Fix bug when "adding" a file that already exists on the server