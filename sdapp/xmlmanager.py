# IMPORTANT Note:
# This script only works if your dropbox folder is still in your user folder


def filemapper(CIK, form):
    import os
    xmldirectory = []
    dropboxdir = os.path.expanduser('~/Dropbox')

    if form == '4/A':
        form = '4A'

    for root, dirs, files in os.walk(dropboxdir + "/AutomatedFTP/storage/" +
                                     str(CIK) + "/" + str(form) + "/"):
        for file in files:
            if file.endswith('.xml'):
#               if os.path.join(root, file).find("0001179110") == -1:
#                   print os.path.join(root, file)
                xmldirectory.append(os.path.join(root, file))
    return xmldirectory