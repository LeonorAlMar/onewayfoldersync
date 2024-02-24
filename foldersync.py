import os
import hashlib
import time
import shutil
import argparse

#---------------------------------------------------------------------------------------------------------------------------

# folder synchronization function
def foldersync(source, replica, logfilepath, timer):
    # check if they exist
    if not os.path.isdir(replica):
        # creates the replica folder if it doesn't exist
        os.makedirs(replica)
        log('Replica folder CREATED',logfilepath)
        print('Replica folder was created.')

    if not os.path.isdir(source):
        log('Source folder NOT FOUND',logfilepath)
        raise argparse.ArgumentError(None, "Invalid Source directory")
        
    log('Beginning file synchronization',logfilepath)

    while True:
        try:
            foldercheck(source,replica, logfilepath)
            time.sleep(timer)
        except KeyboardInterrupt:
            log('Manual Interruption', logfilepath)
            print("Synchronization interrupted. Exiting...")
            raise SystemExit

#---------------------------------------------------------------------------------------------------------------------------

# log function: File creation/copying/removal operations are logged to a file 
def log(logtext,logfilepath):
    # 'logtext' : text  
    currenttime = time.strftime("%Y/%m/%d - %H:%M:%S", time.localtime())
    with open(logfilepath, 'a') as lf:
        lf.write('['+currenttime+'] - '+logtext+'\n')

#---------------------------------------------------------------------------------------------------------------------------
        
# filecheck function: compares 2 files; returns True if they are identical, False if different       
def filecheck(sourcefile, replicafile):
    # 'sourcefile' : path 
    # 'replicafile' : path

    with open(sourcefile, 'rb') as sf, open(replicafile, 'rb') as rf:
        return hashlib.md5(sf.read()).hexdigest() == hashlib.md5(rf.read()).hexdigest()
            
#---------------------------------------------------------------------------------------------------------------------------

# foldercheck function: compares 2 folders; returns True if their contents are identical, False if different
def foldercheck(source, replica, logfilepath):
    updated=0
    copied=0
    deleted=0
    files_source = os.listdir(source)
    files_replica = os.listdir(replica)
     
    for file in files_source:
        #first: check if the file from the source exists in the replica folder
        if file in files_replica:
            if not filecheck(source+'/'+file, replica+'/'+file):
                # the file exists in both folders but the contents are different
                shutil.copy(source+'/'+file, replica+'/'+file)
                log(f'Updated {file}',logfilepath)
                updated += 1
        else:
            # the file does not exist in the replica folder
            shutil.copy(source+'/'+file, replica+'/'+file)
            log(f'Copied {file}',logfilepath)
            copied += 1
        
    for file in files_replica:
        if file not in files_source:
            os.remove(replica+'/'+file)
            log(f'Deleted {file}',logfilepath)
            deleted += 1
    print(f'In this cicle: {updated} files were UPDATED, {deleted} files were DELETED and {copied} files were COPIED'+'\n'+'Ctrl+C to exit')

#---------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='One-way Folder Synchronization')
    parser.add_argument('--source', type=str, default="source", help='Source folder path')
    parser.add_argument('--replica', type=str, default="replica", help='Replica folder path')
    parser.add_argument('--logfilepath', type=str, default='logfile.txt', help='Log file path')
    parser.add_argument('--timer', type=int, default=30, help='Synchronization cycle (seconds)')
    args = parser.parse_args()

foldersync(args.source, args.replica, args.logfilepath, args.timer)
