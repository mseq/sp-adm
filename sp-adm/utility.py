# -*- coding: utf-8 -*-

"""Class Terminal Colors"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class emulated_result_0:
    stdout = 'success feedback'
    returncode = 0

class emulated_result_1:
    stderr = 'failed feedback'
    returncode = 1