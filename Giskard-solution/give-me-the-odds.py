# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:31:19 2023

@author: nacha
"""
from Galaxy import *
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description = 'Process the json files.')

parser.add_argument('file1', type = str, help = 'The path to the first file')
parser.add_argument('file2', type = str, help = 'The path to the second file')

args = parser.parse_args()

MF_json = pd.read_json(args.file1, typ='series') 
Empire_json = pd.read_json(args.file2, typ='series')

empire = Empire(Empire_json.countdown, Empire_json.bounty_hunters)
millennium_falcon = Millennium_falcon(MF_json.autonomy, MF_json.departure, MF_json.arrival, MF_json.routes_db,
                                    empire.countdown, empire.bounty_hunters)

result = Millennium_falcon.give_me_the_odds(millennium_falcon)
odds = result[0]
print(odds)