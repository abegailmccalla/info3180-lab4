import os
 
rootdir = os.getcwd()
print(rootdir)
 
for subdir, dirs, files in os.walk(rootdir + r'\uploads'):
    for file in files:
        print(os.path.join(subdir, file))