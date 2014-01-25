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
        if (os.path.isdir(local_path)):
            # Create the folder on the server
            print "Creating folder %s" % remote_path
            ftp.mkd(remote_path)
        else:
            # It's a file, upload it
            print "Uploading %s to %s" % (local_path, remote_path)
            with open(local_path, "rb") as local_file:
                ftp.storbinary("STOR %s" % remote_path, local_file)

def recursive_delete_files(ftp):
    # WARNING: Very dangerous. Deletes all the files within the cwd of ftp
    files = ftp.nlst()
    for file in files:
        if file == "." or file == "..":
            continue

        if "." in ftp.nlst(file):
            # Folder, recurse
            print "Going into folder %s" % file
            ftp.cwd(file)
            recursive_delete_files(ftp)
            ftp.cwd("..")
            # Now delete the folder
            print "Deleting folder %s" % file
            ftp.rmd(file)
        else:
            print "Deleting file %s" % file
            ftp.delete(file)

def delete(ftp, files):
    cwd = ftp.pwd()
    folder_names = []
    file_names   = []
    
    for file in files:
        if file.endswith("/"):
            folder_names.append(file)
        else:
            file_names.append(file)

    # First delete the files
    for file_name in file_names:
        remote_path = os.path.join(REMOTE_ROOT, file_name).replace("\\", "/")
        print "Deleting file %s from server" % file_name
        ftp.delete(remote_path)

    # Then delete the folders
    for folder_name in folder_names:
        remote_path = os.path.join(REMOTE_ROOT, folder_name).replace("\\", "/")
        print "Deleting folder %s and all its contents from server" % folder_name
        ftp.cwd(remote_path)
        # First delete the folders contents
        recursive_delete_files(ftp)
        # Then delete the folder itself
        ftp.cwd(cwd)    # Go back to root directory
        ftp.rmd(remote_path)

if __name__ == "__main__":
    repo, rev = sys.argv[1:]
	
    if repo == "" or rev == "":
        raise Exception("Empty repo or rev")
    
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
    delete(ftp, deleted)
    
    print
    print "Updating files"
    print "=============="
    upload(ftp, local_root, updated)
    
    print "Done"
    
    ftp.close()