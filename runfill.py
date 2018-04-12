import pandas as pd
from rhapi import RhApi

DEFAULT_URL = "http://vocms00170:2113"
api = RhApi(DEFAULT_URL, debug = False)

MAX_FILL = 6291
MIN_FILL = 6018

for fill in range(MIN_FILL, MAX_FILL + 1):
    query = ("select * from wbm.runs r where r.lhcfill = %s" % fill)
    response = api.csv(query)

    with open('tmp.csv', 'w') as file:
        file.write(response)
    df = pd.read_csv('tmp.csv')

    lhcFills = {}
    for _, row in df.iterrows():
        with open('lhcFills.csv', 'a+') as file:
            file.write("%s, %s \n" % (row["RUNNUMBER"], fill))
