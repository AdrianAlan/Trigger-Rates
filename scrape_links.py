import os
import pycurl
import re
from lxml import html
import httplib
from ConfigParser import SafeConfigParser
from cStringIO import StringIO
from datetime import datetime
from subprocess import call
import logging
import pandas as pd

def curl(request, url, cookie=None):
        """Perform CURL - return_error kwarg returns status after failure - defaults to None"""
        out = StringIO()
        print(url)
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, str(url))
        curl.setopt(pycurl.WRITEFUNCTION, out.write)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.COOKIEFILE, cookie)
        curl.setopt(pycurl.COOKIEJAR, cookie)
        curl.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_1_0)
        curl.perform()

        return out.getvalue(), curl.getinfo(curl.RESPONSE_CODE)

keys = pd.read_csv("./data/keys.csv", names=["run", "trigger_mode", "l1_key", "hlt_key"])

for run in ['304333', '304292', '304291',
       '304209', '304204', '304200', '304199', '304198', '304196',
       '304170', '304169', '304158', '304144', '304125', '304120',
       '304119', '304062', '304000', '303999', '303989', '303948',
       '303885', '303838', '303832', '303825', '302663', '302661',
       '302654', '302651', '302635', '302634', '302597', '302596',
       '302573', '302572', '302571', '302570', '302567', '302566',
       '302555', '302553', '302548', '302526', '302525', '302523',
       '302522', '302513', '302509', '302494', '302492', '302485',
       '302484', '302479', '302476', '302474', '302473', '302472',
       '302448', '302393', '302392', '302388', '302350', '302344',
       '302343', '302342', '302337', '302328', '302322', '302280',
       '302279', '302277', '302263', '302262', '302240', '302229',
       '302228', '302225', '302166', '302165', '302163', '302159',
       '302131', '302043', '302042', '302041', '302040', '302037',
       '302036', '302034', '302033', '302031', '302029', '302026',
       '302019', '301998', '301997', '301987', '301986', '301985',
       '301984', '301969', '301960', '301959', '301941', '301914',
       '301913', '301912', '301694', '301665', '301664', '301627',
       '301567', '301532', '301531', '301530', '301529', '301528',
       '301525', '301524', '301519', '301480', '301476', '301475',
       '301472', '301461', '301450', '301449', '301448', '301447',
       '301417', '301399', '301397', '301396', '301394', '301393',
       '301392', '301391', '301384', '301359', '301330', '301323',
       '301298', '301283', '301281', '301183', '301180', '301179',
       '301165', '301161', '301142', '301141', '301086', '301046',
       '300817', '300816', '300812', '300811', '300806', '300785',
       '300781', '300780', '300777', '300742', '300676', '300675',
       '300674', '300673', '300636', '300635', '300633', '300632',
       '300631', '300576', '300575', '300574', '300560', '300558',
       '300552', '300551', '300548', '300545', '300539', '300538',
       '300517', '300516', '300515', '300514', '300498', '300497',
       '300467', '300466', '300464', '300463', '300462', '300461',
       '300459', '300401', '300400', '300399', '300398', '300397',
       '300396', '300395', '300394', '300393', '300392', '300391',
       '300390', '300389', '300375', '300374', '300373', '300371',
       '300370', '300369', '300368', '300367', '300366', '300365',
       '300364', '300284', '300283', '300282', '300280', '300240',
       '300239', '300238', '300237', '300236', '300235', '300234',
       '300233', '300226', '300157', '300156', '300155', '300124',
       '300123', '300122', '300117', '300107', '300106', '300105',
       '300087', '300079']:

    print(run)

    key = keys[keys.run == int(run)]["hlt_key"].values[0]

    # Generate cookie upfront
    res, _ = curl("GET",
                  "https://cmswbm.cern.ch/cmsdb/servlet/HLTSummary?RUN=%s&NAME=%s" % (run, key),
                  cookie="./ssocookie.txt")

    tree = html.fromstring(res)
    table = tree.xpath('/html/body/table[3]/tr')

    for e in table:
        dqm = None
        for x, element in enumerate(e.iter()):
            if x == 3:
                hlt = element.text
            if x == 4:
                dqm = element.text
            if x == 5:
                l1 = element.text
            
        if dqm == "DQM":
            if l1 is not "null":
                l1list = l1[1:-1].split(" OR ")
                for foo in l1list:
                    with open("./data/links%s.csv" % run, "a") as file_:
                        file_.write("%s,%s,%s\n" % (run, hlt.split("_v")[0], foo))
