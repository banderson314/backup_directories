# backup_directories
Allows user to select two directories: a source directory and a backup directory.

The script will compare all files in the two directories, and if any files don't exit in the backup directory that exists in the source directory, it will copy it to the backup directory.

Additionally, if any files in the source directory has a more recent "date modified" date, that file will be updated in the backup directory.

A report will be generated detailing the files that were copied over.

Please note that if files in the backup location do not exist in the source location, the script will ignore them without notifying the user. Because of this, if the directory structure has been altered, resulting in rearranged files, multiple instances of the same files may exist.