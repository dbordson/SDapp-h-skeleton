# TO RUN THIS IN HEROKU:
# First run "from sdapp.bin import initialdownload" in a local shell.
# because heroku can't run "initialdownload.py", because indices not stored
# in heroku.
from sdapp.bin import formscraper, formparser, populateintermediate,\
    grabmarketdata,\
    populateformadjustments, supersedeinit, adjsharesremaining

from sdapp.bin import update_affiliation_data

from sdapp.bin import newpopulatesigs
