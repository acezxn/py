###############################################################################
# Brute Method to find password of a zip file
# Concept:
#       Step 1: Loop an iterator
#       Step 2: Try the iterated data in the loop
# Consideration:
#       No big table to avoid "Out of Memory"
#       No recursive to avoid "Stack overflow"
###############################################################################
import os
import sys
import time
import itertools as iter
import zipfile
import zlib
start_time = time.time()

zipfilename = "encrypted.zip"
# zipfilename = "folder_encrypted.zip"

archive = zipfile.ZipFile( zipfilename, "r" )
for item in archive.infolist():
    if item.filename.endswith('/'):
        print("Find directory {}".format(item.filename))
    else:
        fname = item.filename
        print("File {}".format(fname))

special_chars = "~!@#$%^&*()_+-=`~/.,"
alphabet_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_lowercase = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
# candidates = alphabet_lowercase+alphabet_uppercase+numbers+special_chars
candidates = alphabet_lowercase
# candidates = "youwin"
MAX_LENGTH = 6  # Maximum Length
i = 0           # Trial count
n = 6           # Digits of a password
while n < (MAX_LENGTH+1) :
    s = [None]*(n-1)
    print("\n n={}".format(n),end='')
    for i in range(n+1): # length of password
        for word in iter.product(candidates, repeat=i):
            pword = bytes(''.join(word),encoding="ASCII")
            i = i + 1       # Count the iterations
            if (i % 1000) == 0 :
                print('.',end='')
                sys.stdout.flush()

            try:
                with archive.open(fname, 'r', pwd=pword) as member:
                    text= member.read()

                print( "\n Got Password: {} with {} trials".format(pword.decode("utf-8"),i))
                break
            except (RuntimeError, zlib.error, zipfile.BadZipFile):
                pass
    n = n + 1

print("Total time: {:.2f} seconds".format((time.time() - start_time)))
