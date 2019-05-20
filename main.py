YOUR_WORKING_DIR = "/home/multifaceted/Rubera/"

import os
os.chdir(YOUR_WORKING_DIR)

from fetch_match_func import fetch_match
import pandas as pd
import sys


urls_2018_df = pd.read_csv("urls/urls2017-2018.txt", header = None)
urls_2017_df = pd.read_csv("urls/urls2018-2019.txt", header = None)

out_file = "players_data/players2016-2017.csv"
in_file = "urls/urls2016-2017.txt"


def collect_player(in_file, out_file):
    import pandas as pd

    urls_df = pd.read_csv(in_file, header = None)
    for url in urls_df[0]:
        res = fetch_match(url)
        if os.path.exists(out_file):
            res.to_csv(out_file, mode = "a", header = False)
        else:
            res.to_csv(out_file, mode = "w", header = True)

collect_player(in_file, out_file)
