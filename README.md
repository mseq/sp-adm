
# sharepoint-adm with python

Repository for M365 Automation with Python
It is mainly based on the PnP CLI for M365
Link: https://pnp.github.io/cli-microsoft365/cmd/spo/folder/folder-remove/

## sp-adm

 Implements few tweaks to help manage Large Libraries on SharePoint Online
 
### List Folders

 It lists the folders inside a SPO Library, at a given path.

### List Files

It lists the files inside a SPO Library, at a given path.

### List Contents

It lists the folders and files inside a SPO Library, at a given path.
But diferently from previous commands, there is a flag you can pass to it
to make it run recursively diving on the folders.

### Move Contents

It lists the folders and filesd inside a SPO Library, at a given path,
then it tries to move these folders and files to the target destination
If the move fails, it dives on the folders recursively to decrease the ammount of items
being moved, increasing the chances of success. 

### TO-DO Improvements
Planning to add a threaded execution to help speed up the script.
The idea is to open parallel threads to move the files.
To avoid breaking the system, I'm thinking on a SEMAPHORE to limit the ammount of threads
So the file move would run on chunks, much faster then it currently does.
