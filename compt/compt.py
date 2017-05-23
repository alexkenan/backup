"""
Automates computer management without a GUI
"""
from zipfile import ZipFile
import os
import shutil
import re


def backup_to_zip(folder, path, number=None):
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
        print 'Creating {}...'.format(zipfilename)

        backupzip = ZipFile(zipfilename, 'w', allowZip64=True)
        amount = 0

        # Walk the entire folder tree and compress the files in each folder.
        for foldername, __, filenames in os.walk(folder):
            # Add the current folder to the ZIP file.
            backupzip.write(foldername)
            # Add all the files in this folder to the ZIP file.
            for filename in filenames:
                newbase = os.path.basename(folder) + '_'
                if (filename.startswith(newbase) and filename.endswith('.zip')) or 'Camera Uploads' in filename:
                    continue  # don't backup the backup ZIP files
                backupzip.write(os.path.join(foldername, filename))
                amount += 1

        backupzip.close()
        print 'Backed up {} files!\n'.format(amount)

    else:
        if not os.path.exists(path) and not os.path.exists(folder):
            print 'Error: Both "{}" and "{}" do not exist!\n'.format(folder, path)
        elif not os.path.exists(folder):
            print 'Error: Folder path "{}" does not exist\n'.format(folder)
        elif not os.path.exists(path):
            print 'Error: Target path "{}" does not exist!\n'.format(path)


def selectnumber():
    """
    :return: Number 1 thru 4, inclusive, based on number.txt
    """
    # figure out the file name
    with open('/Users/Alex/Documents/Python/number.txt') as files:
        number = int(files.read())
    to_return = number
    if number < 4:
        number += 1
    else:
        number = 1

    with open('/Users/Alex/Documents/Python/number.txt', 'w') as numberwrite:
        numberwrite.write('{}'.format(number))

    return to_return


def cleanup_latex(folder_path):
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
        if i > 0:
            print '{} LaTeX files cleaned up.\n'.format(i)
        if i == 0:
            print 'No LaTeX files to clean up!\n'

    else:
        print 'Path "{}" does not exist!\n'.format(folder_path)


def mainhd():
    with open('/.paths.txt') as files:
        one, two, three, four, five, six, seven = files.read().split('\n')

    backup_to_zip(folder=one, path=two, number=selectnumber())
    backup_to_zip(three, four)
    cleanup_latex(five)
    backup_to_zip(six, seven)


if __name__ == '__main__':
    mainhd()
