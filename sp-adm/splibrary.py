# -*- coding: utf-8 -*-

"""Classes for SP Library."""

import json
import subprocess

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
        self.move_content(url, path, recursive, level, False, '')


    def move_content(self, url, path, recursive, level, test, dst):
        """Navigate the folders and files, recursively, if flagged
        Creating the folder tree structure and moving the files."""
        spacer = ''
        for i in range(0, level):
            spacer = spacer + '...'

        folders = self.get_folders(url, path)
        for folder in folders:
            if folder != '':
                print(spacer + folder + '/')

                if recursive:
                    self.get_content(url, path + '/' + folder, recursive, level + 1)

        files = self.get_files(url, path)
        for file in files:
            if file != '':
                print(spacer + file)

        return


