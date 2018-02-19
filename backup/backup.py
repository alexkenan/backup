#!/usr/bin/env python3
#####################################
#    LAST UPDATED     16 FEB 2018   #
#####################################
"""
Automates computer management without a GUI
"""
from zipfile import ZipFile
import os
import shutil
import re
import subprocess
from datetime import datetime
from time import sleep


def backup_to_zip(folder: str, path: str, number: int=None) -> None:
    """
    :param folder: Path of the folder you want to backup
    :param path: Path where you want to backup the zip
    :param number: Optional param to create folder_number at path
    :return: None
    """
    if os.path.exists(folder) and os.path.exists(path):
        os.chdir(path)

        folder = os.path.abspath(folder)

        if number:
            zipfilename = '{}_{}.zip'.format(os.path.basename(folder), number)
        else:
            zipfilename = '{}.zip'.format(os.path.basename(folder))

        # create the ZIP file
        if debug:
            print('Creating {}...'.format(zipfilename))

        backupzip = ZipFile(zipfilename, 'w', allowZip64=True)
        amount = 0

        # Walk the entire folder tree and compress the files in each folder.
        for foldername, __, filenames in os.walk(folder):
            # Add the current folder to the ZIP file.
            # backupzip.write(foldername)
            # Add all the files in this folder to the ZIP file.
            for filename in filenames:
                newbase = os.path.basename(folder) + '_'
                if (filename.startswith(newbase) and filename.endswith('.zip')) or 'Camera Uploads' in filename:
                    continue  # don't backup the backup ZIP files
                backupzip.write(os.path.join(foldername, filename))
                amount += 1

        backupzip.close()

        if debug:
            print('Backed up {} files!'.format(amount))

    else:
        if not os.path.exists(path) and not os.path.exists(folder):
            print('Error: Both "{}" and "{}" do not exist!'.format(folder, path))
        elif not os.path.exists(folder):
            print('Error: Folder path "{}" does not exist'.format(folder))
        elif not os.path.exists(path):
            print('Error: Target path "{}" does not exist!'.format(path))


def selectnumber() -> int:
    """
    Select a number to name the new backup file based on number.txt
    :return: Number 1 thru 4, inclusive, based on number.txt
    """
    # figure out the file name
    with open('/Users/Alex/Documents/Python3/backup/number.txt') as files:
        number = int(files.read())
    to_return = number
    if number < 4:
        number += 1
    else:
        number = 1

    with open('/Users/Alex/Documents/Python3/backup/number.txt', 'w') as numberwrite:
        numberwrite.write('{}'.format(number))

    return to_return


def cleanup_latex(folder_path: str) -> None:
    """
    :param folder_path: Folder that should be cleaned up. Puts all LaTeX generated files
    (.pdf, .aux, .log, etc) into its own folder with the name of the main LaTeX file
    :return: None
    """
    folder_exists = os.path.exists(folder_path)
    if folder_exists:
        i = 0
        for folder_name, __, filenames in os.walk(folder_path):
            for filename in filenames:
                if 'DS' not in filename and '.' in filenames:
                    indexof = filename.index('.')
                    temppath = os.path.join(folder_path, filename[:indexof])

                    if os.path.exists(temppath):
                        shutil.move(os.path.join(folder_name, filename), temppath)
                        i += 1
                    else:
                        os.makedirs(temppath)
                        shutil.move(os.path.join(folder_path, filename), temppath)
                        i += 1
        if debug:
            if i > 0:
                print('{} LaTeX files cleaned up.\n'.format(i))
            if i == 0:
                print('No LaTeX files to clean up!\n')

    else:
        print('Path "{}" does not exist!\n'.format(folder_path))


def remove(path: str) -> None:
    """
    Removes all files in path
    :param path: Absolute path to directory
    :return: None
    """
    os.chdir(path)
    for fol in os.listdir(os.getcwd()):
        if not fol.startswith('.'):
            try:
                shutil.rmtree(fol)
            except OSError:
                os.remove(fol)


def run_shell(path: str) -> None:
    """
    Run a bash script as shell (DANGEROUS)
    :param path: Path to Unix executable
    :return: None
    """
    if os.path.exists(path):
        subprocess.call(path)


def clear_temp_folders() -> None:
    """
    Clears Spark mail client temporary folders
    :return: None
    """
    pathe = os.getcwd()
    path1 = '/Users/Alex/Library/Group Containers/3L68KQB4HG.group.com.readdle.smartemail/cache/messagesData'

    remove(path1)

    os.chdir(pathe)


def mainhd() -> None:
    """
    Run main program. Backup folders to zip, clean up any LaTeX files, clear temp folders
    :return: None
    """
    debug = False
    backup_to_zip(folder='/Users/Alex/Desktop/College/', path='/Users/Alex/Box Sync/',
                  number=selectnumber())
    backup_to_zip('/Users/Alex/Desktop/Clutter/', '/Users/Alex/Dropbox/Backups/')
    cleanup_latex('/Users/Alex/Documents/LaTeX/Files')
    backup_to_zip('/Users/Alex/Documents/', '/Users/Alex/Box Sync/')
    clear_temp_folders()


if __name__ == '__main__':
    mainhd()
