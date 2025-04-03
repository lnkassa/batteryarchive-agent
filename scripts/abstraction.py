# coding: utf-8
# Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

import os
import glob
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import psycopg2
from sqlalchemy import create_engine
import yaml
import logging
import logging.config
import time

class abstractModule():
    def __init__(self):
        self.module_metadata_table = 'module_metadata'
        self.cycle_metadata_table = 'cycle_metadata'
        self.timeseries_table = 'cycle_timeseries'
        self.buffer_table = 'cycle_timeseries_buffer'
        self.stats_table = 'cycle_stats'

    def create_cell_df(self, path, row):
        pass
    
    def populate_metadata(self, df_m_md, file_id):
        pass
            
class abstractCell():
    def __init__(self, md):
        self.cell_metadata_table = ''
        self.cycle_metadata_table = ''
        self.timeseries_table = ''
        self.buffer_table = ''
        self.stats_table = ''
        self.cell_md = md #to get fixed md
        #self.slash = slash #replace with os.join

    def calc_timeseries(self, df_t, ID, engine):
        pass
    
    def calc_stats(self, df_t, ID, engine):
        pass
    
    def calc_cycle_quantities(self,df):
        pass
    
    def create_mapper(self,tester, source):
        pass

    def populate_metadata(self, df_c_md): ##conflict need to pass cell type from main
        pass
    
def file_reader(path, name, **kwargs):
    #reads yaml function name to chose pandas function for file reading
    read_func = getattr(pd, name)
    if name=='read_excel':
        return read_func(path)(**kwargs)
    else:
        return read_func(path)
    
def convert_datetime_time(df,col_name):
    df['pystamp']=pd.to_datetime(df[col_name]) #convert to python date-time format in ns
    df['inttime']=df['pystamp'].astype(int)
    df['inttime']=df['inttime'].div(10**9)
    df['Time [s]']=df['inttime']-df['inttime'].iloc[0]
    return df['Time [s]']