import pandas as pd
import json




def parse_blkgrp() :
    headers = ['userid', 'timecome','date','lat','long','count','timeleave','duration']
    stay_07 = pd.read_csv('../data/stay_points_07/2017-07-02.txt', names=headers)
    
    processed_df = stay_07[['userid','lat','long',]]
    processed_df['hour'] = pd.to_datetime(stay_07['timecome'], format='%Y-%m-%d %H:%M:%S').dt.hour

    