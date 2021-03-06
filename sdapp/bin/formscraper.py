import os
from sdapp.models import IssuerCIK, FTPFileList, FullForm
from ftplib import FTP
from StringIO import StringIO
import sys
from datetime import date
import time

cwd = os.getcwd()
today = date.today()


def ftplogin():
    try:
        time.sleep(1)
        if os.environ.get('EMAIL_ADDRESS') is None:
            target = open(cwd + '/' + 'emailaddress.txt')
            email = target.read()
            email = email.strip()
            target.close()
        else:
            email = os.environ.get('EMAIL_ADDRESS')
        ftp = FTP('ftp.sec.gov')
        ftp.login('anonymous', email)
        print "Connected"
        return ftp
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % e
        print "Cannot connect"
        print "Check emailaddress.txt file or EMAIL_ADDRESS global variable"
        print "And check your internet connection"

        exit(0)


# def ftprefresh(ftp):
#     try:
#         ftp.voidcmd('NOOP')
#         return ftp
#     except IOError as e:
#         print "I/O error({0}): {1}".format(e.errno, e.strerror)
#         print "Retrying..."
#         ftp = ftplogin()
#         ftp.voidcmd('NOOP')
#         print "Worked!"
#         return ftp


def ftpdownload(filepath, ftp):
    try:
        r = StringIO()
        ftp.retrbinary('RETR %s' % filepath, r.write)
        return r.getvalue()

    except:
        try:
            ftp = ftplogin()
            r = StringIO()
            ftp.retrbinary('RETR %s' % filepath, r.write)
            return r.getvalue()
        except:
            print "Can't get file in ", filepath


def extractcik(fullpath):
    try:
        return fullpath[:fullpath.find('/')]
    except:
        return 'ERROR'


def saveandclear(formsforsave):
    if len(formsforsave) > 0:
        FullForm.objects.bulk_create(formsforsave)
    formsforsave = []
    return formsforsave


if not(os.path.isfile('emailaddress.txt')) and\
        os.environ.get('EMAIL_ADDRESS') is None:
    print "Let's locally store your email address as an ftp password",
    print "(you won't be logged in yet)."
    target = open(cwd + '/' + 'emailaddress.txt', 'w')
    print "Created an email address storage file in", cwd + '/' + \
        'emailaddress.txt'
    print "What is your email address? (for anonymous ftp password)"
    email = raw_input()
    print>>target, email
    target.close()
    print ''


cik_num_list = IssuerCIK.objects.values_list('cik_num', flat=True)

allforms = set(FullForm.objects.values_list('sec_path',
                                            flat=True))

try:
    filelistobjects = FTPFileList.objects.all()
    filestring = filelistobjects[len(filelistobjects) - 1].files
    filelist = filestring.split(',')
    secfileset = set(filelist)
except:
    print 'SEC download list is absent or improperly formed; ',
    print 'check FTPFileList table in database'
    exit(0)

formdownloadset = secfileset - (secfileset & allforms)
print len(secfileset)
print len(allforms)
print len(formdownloadset)
formdownloadlist = list(formdownloadset)


ftp = ftplogin()
formsforsave = []
count = 0.0
totalformslength = float(len(formdownloadlist))
for formpath in formdownloadlist:
    fullpath = '/edgar/data/' + formpath
    text = ftpdownload(fullpath, ftp)
    a = FullForm(sec_path=formpath,
                 save_date=today,
                 issuer_cik_num=extractcik(formpath),
                 text=text)
    count += 1.0
    percentcomplete = round(count / totalformslength * 100, 2)
    sys.stdout.write("\r%s / %s forms to scrape : %.2f%%" %
                     (int(count), int(totalformslength),
                      percentcomplete))
    sys.stdout.flush()

    if text is not None:
        formsforsave.append(a)
    if len(formsforsave) > 1000:  # 10 mb
        print '\nSaving a batch',
        formsforsave = saveandclear(formsforsave)
        print 'done with this batch, starting next batch'

print '\nSaving'
formsforsave = saveandclear(formsforsave)
print 'Done with all listed files'
