# onewayfoldersync
This is a program that synchronizes two folders.
  *   Synchronization is carried out periodically and changes(file update, copying, removal operations) are displayed in the console and written to a log file.
  *   Folder paths, synchronization interval and log file path can be provided using command line arguments, with default values.   

## Requirements

  *   Python 3.x
  *   Libraries: os, hashlib, time, shutil, argparse


## Usage

```
python main.py [--source SOURCE] [--replica REPLICA] [--logfilepath LOG_FILE_PATH] [--timer CYCLE_DURATION]
```

- `--source`: Path to the folder meant to be synchronized (default: "source").
- `--replica`: Path to the folder meant to replicate the source (default: "replica").
- `--logfilepath`: Path to the log file (default: "logfile.txt").
- `--timer`: Duration of synchronization cycles in seconds (default: 30).

## Example

To synchronize a folder named "folder01" to "folder02" with a time interval of 45 seconds and log the synchronization process to "logfile00.txt", run the following command:

```
python foldersync.py --source folder01 --replica folder02 --logfilepath logfile00.txt --timer 45
```

## Notes

- If the replica folder does not exist, it will be created.
- If the source folder does not exist, the script will raise an error.
- The script will replicate the source folder into the replica folder every cycle according to the cycle duration that was set.
- The script uses the MD5 hash of files to compare files.
