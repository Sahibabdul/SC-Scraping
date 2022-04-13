import os
import sys
import datetime

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

def work(path):
    start= datetime.datetime.now()
    list = os.listdir(path) # lists all folders and files contained in the specified path
    print(list)

 # constructs a stack where if its a file index it 
 # else call the function recursively with the new path
 # limitation subfolders of subfolders may cause problems currently
    for i in list:
        if os.path.isfile(i):
            # calls the indexing function with verbose and force settings
            print(os.system('opensemanticsearch-index-file -v -f '+str(path+"/"+i)))
            print("--------------------------------------------------------------------")
        else:
            print(os.listdir(str(path+"/"+i)))
            work(path + "/" + i)

    print(str(start) + " -- " + str(datetime.datetime.now()) + " --- Time elapsed: " + str(datetime.datetime.now()-start))

def createList(path, subfolders):
    with open("list.txt","a",encoding="UTF-8") as writer:
        contents = os.listdir(path)
        for content in contents:
            if os.path.isdir(content):
                writer.write(str(path + "/" + content + "\n"))
                if subfolders:
                    createList(str(path + "/" + content), True)

usage_msg = "Usage: " + sys.argv[0] + " \n -h Print this message" + " \n -i index needs other arguments" + " \n -c go with current folder" + " \n -p PATH goes through the provided path" + " \n -f reads specified file and works with the data passed line break means new location" + " \n -l create a list to be used as a watchlist" + " \n -s include subfolders" + " \n Args folder path "

if "-h" in opts:
    print(usage_msg)

elif "-i" in opts:
    if "-c" in opts:
        work(os.getcwd())
    elif "-p" in opts:
        work(args[0])
    else:
        print("Please specify where you would like to index files: \n -c current folder \n -p FOLDERPATH folderpath which is going to be indexed")

elif "-p" in opts:
    print("looking at provided path" + args)
    

elif "-f" in opts:
    with open(args[0],"r", encoding="UTF-8") as input:
        for line in input.readlines():
            work(line)
elif "-l" in opts:
    if os.path.isfile(os.getcwd()+"/list.txt"):
        sys.exit("The list.txt file already exists please make sure to delete or move it before running this command again!")
        
    if "-c" in opts:
        path = os.getcwd()
    else:
        path = args[0]
    if "-s" in opts:
        createList(path, True)
    else:
        createList(path, False)

elif len(args) < 1:
    print("Please pass a folder location to start with.")
else:
    raise SystemExit(f"Usage: {sys.argv[0]} {usage_msg}")