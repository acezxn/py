###############################################################################
# Brute Method to find password of a zip file
# Concept:
#       Step 1: Generate password table
#       Step 2: Try the table one by one
# Problem:
#       The table is so huge that "out of memory" will happen easily
###############################################################################
import os
import sys
import time
import zipfile
import zlib

start_time = time.time()

zipfilename = "encrypted.zip"
# zipfilename = "folder_encrypted.zip"
MAX_LENGTH = 6
special_chars = "~!@#$%^&*()_+-=`~/.,"
alphabet_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_lowercase = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
# candidates = alphabet_lowercase+alphabet_uppercase+numbers+special_chars
candidates = alphabet_lowercase     # The candidates of characters
# candidates = "youwin"     # The candidates of characters
complete_list = []                  # The guessing password table
pword = ''                          # The true password

# Building a table
print("Started to build password table")
for current in range(MAX_LENGTH):
    ch = [i for i in candidates]
    for y in range(current):
        ch = [x+i for i in candidates for x in ch]
    complete_list = complete_list+ch
    print("Table length up to {}".format(len(complete_list)))
    sys.stdout.flush()
print("Generate password {} list : {:.2f} seconds".format(len(complete_list),(time.time() - start_time)))

# Try the password table
with zipfile.ZipFile( zipfilename, "r" ) as archive:
    for item in archive.infolist():
        if item.filename.endswith('/'):
            directory = "crack_"+item.filename
            if not os.path.exists(directory):
                os.makedirs(directory)
        else:
            fname = item.filename
            print("cracking {}".format(fname),end='')
            i = 0 # Trial count
            for trial in complete_list:
                try:
                    i = i + 1
                    if (i % 1000) == 0 :
                        print('.',end='')
                        sys.stdout.flush()

                    if not pword :
                        word = trial.strip().encode("ASCII")
                    else:
                        word = pword

                    with archive.open(fname, 'r', pwd=word) as member:
                        text = member.read()

                    print( "\n Got Password: {}  with {}/{} trials".format(word.decode("utf-8"),i,len(complete_list)))
                    pword = word

                    break
                except (RuntimeError, zlib.error, zipfile.BadZipFile):
                    pass
            if pword != '':
                outputfile = "crack_"+ fname
                with open(outputfile, 'wb') as ofile:
                    ofile.write(text)
            else:
                print("Cannot find the password")

print("Total time: {:.2f} seconds".format((time.time() - start_time)))
