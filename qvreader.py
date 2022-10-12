#!/usr/bin/env python

#******************************************
#qvreader is a Python module to handle the output measurements of the Mitutoyo QVPAK software.
#qvreader can be used as a standalone script or as a module to be imported in other scripts.
#EXAMPLE: python3 qvreader.py -f file.txt
#HELP: python3 qvreader.py --help
#Repository: github.com/guescio/QVReader
#Author: Francesco Guescini.
__author__ = 'Francesco Guescini'

#******************************************
#import stuff
import argparse

#******************************************
class qvreader:
    
    #******************************************
    #init
    def __init__(self, filename="", lines=[]):

        #------------------------------------------
        #set parameters
        self.filename=filename
        self.lines=lines

        #------------------------------------------
        #set input file
        if self.filename == "":
            print("no QVPAK file specified yet")
        else:
            self.setFile(self.filename)

    #******************************************
    #check for possible problems
    def __check__(self):
    
        #------------------------------------------
        #file
        if self.filename is None:
            raise SystemExit("\n***ERROR*** no file provided")
            
    #******************************************
    #set input file
    def setFile(self, filename="", debug=False):
        if debug:
            print("\nreading file: %s"%filename)
        self.lines=[]
        with open(filename, 'r') as f:
            self.lines = f.readlines()
            f.close()
        return len(self.lines)

    #******************************************
    #get list of items
    def list(self, item="", name="", debug=False):

        self.__check__()
        
        #------------------------------------------
        #search for item
        results = []
        if debug:
            if item!="" or name != "":
                print("searching for \"%s\" named \"%s\"..."%(item, name))
            else:
                print("searching...")
        for i, line in enumerate(self.lines):
            if ( (item+":" in line and name+"(ID:" in line) or #e.g.: "Plane: sensor-plane(ID:113, From 100 Pts.)"
                 (item+":" in line and name+"\n" in line and line.count(":")==1) ): #e.g.: "Ebene: plane"
                results.append(line.rstrip().lstrip())
        return results
        
    #******************************************
    #get item
    def get(self, item="", name="", debug=False):

        self.__check__()

        #------------------------------------------
        #check for multiple matches
        if len(self.list(item, name))>1:
            print("multiple items match the item and name specified: %s, %s"%(item, name))
            return
        
        #------------------------------------------
        #search for item
        results = {}
        if debug:
            print("getting \"%s\" named \"%s\"..."%(item, name))

        #loop over all lines
        for i, line in enumerate(self.lines):
            if item in line and name in line and i<len(self.lines):
                results['item']=line.split(":")[0]
                if "(ID:" in line:
                    results['name']=line.split(": ")[1].split("(ID")[0].rstrip()
                else:
                    results['name']=line.split(": ")[1].rstrip()
                j=i+1
                while "=" in self.lines[j]:
                    results[self.lines[j].lstrip().split(" =")[0]] = self.lines[j].split(" =")[1].lstrip().rstrip()
                    j+=1
                    if j>=len(self.lines):
                        break
        return results


#******************************************
if __name__ == '__main__':

    #------------------------------------------
    #parse input arguments
    parser = argparse.ArgumentParser(description='%prog [options]')
    parser.add_argument('-f', '--file', dest='filename', default='', required=True, help='QVPAK results file')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    #------------------------------------------
    #read file
    qvr = qvreader(args.filename)

    #get items
    items = qvr.list(debug=args.debug)

    #print items
    for item in items:
        print("\n%s"%item)
        if "(ID:" in item:
            d = qvr.get(item.split(":")[0], item.split(":")[1].split("(ID")[0].lstrip().rstrip(), debug=args.debug)
        else:
            d = qvr.get(item.split(":")[0], item.split(":")[1].lstrip().rstrip(), debug=args.debug)
        if d is not None:
            for k in d:
                print("    %s: %s"%(k, d[k]))
    print()
