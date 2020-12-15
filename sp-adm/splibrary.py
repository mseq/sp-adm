# -*- coding: utf-8 -*-

"""Classes for SP Library."""

import json
import subprocess
import threading
import concurrent.futures

from utility import bcolors
from utility import emulated_result_0
from utility import emulated_result_1

class LibraryManager:
    """Manage a SharePoint Library."""

    def __init__(self):
        """Create a LibraryManager object."""
        self = {}


    def adjust_url(self, url):
        """Get the URL parameter and adjust, removing slash if found."""
        if url[-1] == '/':
            return url[0:len(url)-1]


    def adjust_path(self, path):
        """Get the path parameter and adjust,
        removing the slash in the beginning and removing from the end."""
        if path[0] == '/':
            path = path[1:len(path)]

        if path[-1] == '/':
            path = path[0:len(path)-1]

        return path


    def get_folders(self, url, path):
        """Get folders list."""
        path = self.adjust_path(path)
        result = (subprocess.run(['m365', 'spo folder list --query [*].Name -o json -u', url, '-p', path], \
            stdout=subprocess.PIPE)).stdout.decode('utf-8')

        return result[2:len(result)-3].split("\",\"")

    def get_folder_item_count(self, url, path):
        """Get details of a folder."""
        path = self.adjust_path(path)
        return (subprocess.run(['m365', 'spo folder get --query ItemCount -o json -u', url, '-f', path], \
            stdout=subprocess.PIPE)).stdout.decode('utf-8')


    def get_files(self, url, path):
        """Get files list."""
        path = self.adjust_path(path)
        # return json.loads(subprocess.run(['m365', 'spo file list -o json -u', url, '-f', path], \
        #     stdout=subprocess.PIPE).stdout.decode('utf-8'))
        result = (subprocess.run(['m365', 'spo file list --query [*].Name -o json -u', url, '-f', path], \
            stdout=subprocess.PIPE)).stdout.decode('utf-8')
        
        return result[2:len(result)-3].split("\",\"")


    def get_content(self, url, path, recursive, level):
        """Get the files and folders, recursively if flagged."""
        self.move_content(url, path, recursive, level, True, '', '')


    def move_content(self, url, path, recursive, level, test, targ, dst):
        """Navigate the folders and files, recursively, if flagged
        Creating the folder tree structure and moving the files."""
        folders = self.get_folders(url, path)
        if (test == False):
            # Try to move the folders in threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                for folder in folders:
                    if folder != '':
                        executor.submit(self.move_folder, url, path, folder, targ, dst)

            # All folders not moved, create and dive on it
            folders = self.get_folders(url, path)
            for folder in folders:
                if folder != '':
                    result = self.create_folder(url, dst, folder)
                    if (result.returncode == 0):
                        print('/' + dst + '/' + folder + bcolors.OKGREEN + "  CREATED" + bcolors.ENDC)
                    else:
                        print('/' + dst + '/' + folder + bcolors.FAIL + "  CREATE FAILED: " + bcolors.ENDC + \
                            json.loads(result.stdout.decode('utf-8'))['message'])

                    if recursive:
                        result = self.move_content(url, path + '/' + folder, recursive, level + 1, test, targ, dst + '/' + folder)
                        if test == False and result == 0:
                            result = self.remove_folder(url, path, folder)
                            if result.returncode == 0:
                                print('/' + path + '/' + folder + bcolors.OKBLUE + "  REMOVED" + bcolors.ENDC)
                            else:
                                print('/' + path + '/' + folder + bcolors.FAIL + "  REMOVE FAILED: " + bcolors.ENDC + \
                                    json.loads(result.stdout.decode('utf-8'))['message'])

        else:
            folders = self.get_folders(url, path)
            for folder in folders:
                print(path + '/' + folder + '/')

                if recursive:
                    result = self.move_content(url, path + '/' + folder, recursive, level + 1, test, targ, dst + '/' + folder)

        files = self.get_files(url, path)
        if (test == False):
            # Move files in threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                for file in files:
                    if file != '': 
                        executor.submit(self.move_file, url, path, file, targ, dst)
        else:
            for file in files:
                if file != '': 
                    print(path + '/' + file)

        return int(self.get_folder_item_count(url, path))


    def create_folder(self, url, path, folder):
        """Create a folder a given path, from an URL."""
        path = self.adjust_path(path)
        # print('\n m365 spo folder add -o json -u {0} -p {1} -n {2}'.format(url, path, folder))
        # return emulated_result_0 
        return (subprocess.run(['m365', 'spo folder add -o json -u', url, '-p', path, '-n', folder], \
            stdout=subprocess.PIPE))


    def move_file(self, url, path, file, targ, dst):
        """Move the FILE from URL/Path to DST."""
        targ = self.adjust_path(targ)
        dst = self.adjust_path(dst)
        # print('\n m365 spo file move -o json -u {0} -s {1} -t {2}'.format(url, path + '/' + file, '/' + targ + '/' + dst + '/'))
        # return emulated_result_1 
        result = (subprocess.run(['m365', 'spo file move -o json -u', url, '-s', path + '/' + file, '-t', '/' + targ + '/' + dst + '/'], \
            stdout=subprocess.PIPE))

        if (result.returncode == 0):
            print('/' + path + '/' + file + bcolors.BOLD + ' ==> ' + bcolors.ENDC, end='')
            print('/' + dst + '/' + bcolors.OKCYAN + "  FILE MOVED" + bcolors.ENDC)
        else:
            print('/' + path + '/' + file + bcolors.BOLD + ' ==> ' + bcolors.ENDC, end='')
            print(dst + '/' + bcolors.FAIL + "  FILE MOVE FAILED: " + bcolors.ENDC + \
                json.loads(result.stdout.decode('utf-8'))['message'])
                
        return


    def move_folder(self, url, path, folder, targ, dst):
        """Move the FOLDER from URL/Path to DST."""
        targ = self.adjust_path(targ)
        dst = self.adjust_path(dst)
        # print('\n m365 spo folder move -o json -u {0} -s {1} -t {2}'.format(url, path + '/' + folder, '/' + targ + '/' + dst + '/'))
        # return emulated_result_1 
        result = (subprocess.run(['m365', 'spo folder move -o json -u', url, '-s', path + '/' + folder, '-t', '/' + targ + '/' + dst + '/'], \
            stdout=subprocess.PIPE))

        if result.returncode == 0:
            print('/' + path + '/' + folder + bcolors.BOLD + ' ==> ' + bcolors.ENDC, end='')
            print('/' + dst + '/' + bcolors.OKGREEN + "  FOLDER MOVED" + bcolors.ENDC)
        else:
            print('/' + path + '/' + folder + bcolors.BOLD + ' ==> ' + bcolors.ENDC, end='')
            print('/' + dst + '/' + bcolors.FAIL + "  FOLDER MOVE FAILED: " + bcolors.ENDC + \
                json.loads(result.stdout.decode('utf-8'))['message'])

        return


    def remove_folder(self, url, path, folder):
        """Remove a FOLDER from URL/Path."""
        path = self.adjust_path(path)
        # print('\n m365 spo folder remove --confirm -o json -u {0} -f {1}'.format(url, '/' + path + '/' + folder))
        # return emulated_result_0 
        return (subprocess.run(['m365', 'spo folder remove --confirm -o json -u', url, '-f', '/' + path + '/' + folder], \
            stdout=subprocess.PIPE))