#!/usr/bin/python3
import argparse
from pathlib import Path
import os
import subprocess

class myFile():
    def __init__(self, myfile):
        self.__path = os.path.dirname(myfile)
        self.__filename = Path(myfile).stem
        self.__file = myfile
    
    def __contains__(self, key):
        if self.__filename == key:
            return True
        return False
    def __eq__(self, key):
        return self.__contains__(key)
    
    def __ne__(self, key):
        return not(self.__eq__(key))
    
    def __hash__(self):
        ''' 
        Magic happens here: As we return the hash of the filename only (without the path, without the extension (like ORF) 
        we get a unique hash if we compare jpgs with orfs (as the filename is the same).
        '''
        return hash(self.__filename)
    
    def __str__(self):
        return self.__file

def extract_filenames(list_of_files):
    filenames = []
    for i in list_of_files:
        j = str(i)
        if(os.path.isfile(j)):
            myfile = myFile(j)
            filenames.append(myfile)
    return filenames

def main():
    parser = argparse.ArgumentParser(description='Delete orf files having no corresponding jpeg files in the directory')
    parser.add_argument('path', type=str, help="The patch to find the orphans. Warning: This is the root folder, every orf having no matching jpeg will be deleted")
    parser.add_argument('--force', help="Delete the files without seperate acknowledgement", action="store_true")
    parser.add_argument('--dry', help="Dry run, --force is ignored then", action="store_true")
    args = parser.parse_args()
    
    path = str(args.path)
    
    ORFs = Path(path).rglob('*ORF')
    JPGs = Path(path).rglob('*JPG')
    
    filenames_ORF = extract_filenames(ORFs)
    filenames_JPG = extract_filenames(JPGs)
    res = set(filenames_ORF) - set(filenames_JPG)
    
    for i in res:
        print("File to be removed: " + str(i))
        if not args.dry:
            if not args.force:
                myinput = input("Remove this file [y|n]?")
                if myinput == 'y' or myinput == 'Y':
                    print("Removing "+ str(i))
                    os.remove(str(i))
            else:
                print("Removing "+ str(i))
                os.remove(str(i))
    
if __name__ == "__main__":
    print("Running testcode")
    main()