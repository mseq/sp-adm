#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MOVE: cmd to move filestrutures between M365 Libraries.

Calling sp-adm MOVE, you'll need to pass the following info
-u 'SP Online URL'
-s 'The library folder you want to move'
-t 'The library folder to where you want to move the file structure'

The script will you M365 CLI to execute the task
- List the files on the root folder, 
- Move the files,
- List the folders on the root folder,
- Loop the folders list
- And for each folder, create a local folder, and execute the script in the listed folder
- After looping all folders, it will return

"""

import sys
import click
import json
import subprocess

from splibrary import LibraryManager
from termcolors import bcolors

library_manager = None

@click.group()
def cli():
    """sp-adm can be used to move files and folders across libraries."""
    global library_manager

    library_manager = LibraryManager()


@cli.command('list-folders')
@click.argument('url')
@click.argument('path')
def list_folders(url, path):
    """Lists the SP folders of the url/path"""
    # path = "/{0}".format(path)
    # result = json.loads(subprocess.run(['m365', 'spo folder list -o json -u', url, '-p', path], \
    #     stdout=subprocess.PIPE).stdout.decode('utf-8'))
    result = library_manager.get_folders(url, path)

    for folder in result:
        print(folder['Name'])


@cli.command('list-files')
@click.argument('url')
@click.argument('path')
def list_files(url, path):
    """Lists the SP files of the url/path"""
    # result = json.loads(subprocess.run(['m365', 'spo file list -o json -u', url, '-f', path], \
    #     stdout=subprocess.PIPE).stdout.decode('utf-8'))
    result = library_manager.get_files(url, path)
    
    for file in result:
        print(file['Name'])


@cli.command('list-content')
@click.argument('url')
@click.argument('path')
@click.option('--recursive/--no-recursive', default=False)
def list_content(url, path, recursive):
    """Lists the folders and files, recursively if flagged"""
    library_manager.get_content(url, path, recursive, 0)


@cli.command('move-content')
@click.argument('url')
@click.argument('path')
@click.argument('dst')
@click.option('--recursive/--no-recursive', default=False)
def move_content(url, path, dst, recursive):
    """Lists the folders and files, recursively if flagged"""
    library_manager.move_content(url, path, recursive, 0, True, dst)


if __name__ == '__main__':
    cli()
