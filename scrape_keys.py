import os
import pycurl
import re
import httplib
from ConfigParser import SafeConfigParser
from cStringIO import StringIO
from datetime import datetime
from subprocess import call
import logging

def curl(request, url, cookie=None):
        """Perform CURL - return_error kwarg returns status after failure - defaults to None"""
        out = StringIO()

        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, str(url))
        curl.setopt(pycurl.WRITEFUNCTION, out.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.COOKIEFILE, cookie)
        curl.setopt(pycurl.COOKIEJAR, cookie)
        curl.perform()

        return out.getvalue(), curl.getinfo(curl.RESPONSE_CODE)

for run in range(304796, 304800):
    print(run)
    res, _ = curl("GET",
                  "https://cmswbm.cern.ch/cmsdb/servlet/RunSummary?RUN=%s" % run,
                  cookie="./ssocookie.txt")
    if "TriggerMode" in res:
        tm = res.split("TriggerMode?KEY=")[1].split(">")[0]
        l1 = res.split("L1Summary?RUN=%s&KEY=" % run)[1].split(">")[0]
        hlt = res.split("HLTSummary?RUN=%s&NAME=" % run)[1].split(">")[0]

        with open('./data/keys.csv', 'a') as file_:
            file_.write("%s,%s,%s,%s\n" % (run, tm, l1, hlt))
