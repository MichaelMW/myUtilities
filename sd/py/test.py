#!/usr/bin/env python
# encoding: utf-8


import os

##os.chdir("/Users/Michael_MW/")
#
#
#import os
#
#class cd:
#    """Context manager for changing the current working directory"""
#    def __init__(self, newPath):
#        self.newPath = os.path.expanduser(newPath)
#
#    def __enter__(self):
#        self.savedPath = os.getcwd()
#        os.chdir(self.newPath)
#
#    def __exit__(self, etype, value, traceback):
#        #os.chdir(self.savedPath)
#        pass
#
#
#import subprocess # just to call an arbitrary command e.g. 'ls'
#
## enter the directory like this:
#with cd("~/Library"):
#   # we are in ~/Library
#   subprocess.call("ls")


#os.system("cd /Users/Michael_MW/")



from contextlib import contextmanager
import os

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


os.chdir('/home')

with cd('/tmp'):
    # ...
    raise Exception("There's no place like home.")
# Directory is now back to '/home'.



