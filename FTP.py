'''
Created on 2012-08-26

@author: robbie
'''
from ftplib import FTP
import os, sys, subprocess

REMOTE_ROOT     = "./"          # Changed in settings file
TRUNK           = "trunk/"
ADDED           = "A   "
DELETED         = "D   "
UPDATED         = "U   "
OFFSET          = len(ADDED) + len(TRUNK)

def upload(ftp, local_root, files):
    for file_name in files:
        local_path = os.path.join(local_root, file_name).replace("/", "\\")
        remote_path = os.path.join(REMOTE_ROOT, file_name).replace("\\", "/")
        print "Uploading %s to %s" % (local_path, remote_path)
        with open(local_path, "rb") as local_file:
            ftp.storbinary("STOR %s" % remote_path, local_file)

def delete(ftp, files):
    for file_name in files:
        print "Deleting %s from server" % file_name
        remote_path = os.path.join(REMOTE_ROOT, file_name).replace("\\", "/")
        ftp.delete(remote_path)

if __name__ == "__main__":
    # Args: REPO REV LOCAL_REPO FTPUser FTPPass
    repo, rev = sys.argv[1:]
    
    with open("E:\website.txt", "r") as settings:
        local       = settings.readline().rstrip()
        ftp_server  = settings.readline().rstrip()
        user        = settings.readline().rstrip()
        password    = settings.readline().rstrip()
        REMOTE_ROOT = settings.readline().rstrip()

    local_root = os.path.join(local, TRUNK)
    
    # Take SVN changed output and convert it to a list of Added/Deleted/Modified
    changed = subprocess.check_output(["svnlook", "changed", "-r", rev, repo]).split("\r\n")[:-1]
    added = []
    deleted = []
    updated = []
    
    for change in changed:
        file_name = change[OFFSET:]
        if change.startswith(ADDED):
            added.append(file_name)
        elif change.startswith(DELETED):
            deleted.append(file_name)
        elif change.startswith(UPDATED):
            updated.append(file_name)

    ftp = FTP(ftp_server)
    ftp.login(user, password)
    
    print "Adding new files to FTP"
    print "======================="
    upload(ftp, local_root, added)
    
    print
    print "Deleting files"
    print "=============="
    #delete(ftp, deleted)
    
    print
    print "Updating files"
    print "=============="
    upload(ftp, local_root, updated)
    
    print "Done"
    
    ftp.close()