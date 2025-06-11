# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

import pandas as pd
from .abstractFileType import AbstractFileType

class Uconn(AbstractFileType):
    def __init__(self):
        self.tester =  'generic'#this is problematic for the future
        self.reader_func = 'read_csv'
        self.col_mapping = {'cycle_index' : 'Cycle',
                            'date_time' : 'Timestamp',
                            'i' : 'Current (A)',
                            'v' : 'Voltage (V)'}
        self.unit_mult = {'A' : 1, 'V' : 1, 's' : 1}

    def file_to_df(self, path:str) -> tuple[pd.DataFrame, str]:
        read_func = getattr(pd, self.reader_func)
        if self.reader_func=='read_excel': #is there a better way to choose this if needed?
            df_ts_file = read_func(path, None)
            for sheet in df_ts_file.keys():
                if 'channel' in sheet.lower():
                    return df_ts_file[sheet], sheet
        else:
            return read_func(path), ''

    def datetime_to_testtime(self, df:pd.DataFrame) -> pd.Series:
        df_tt = pd.DataFrame()
        df_tt['pystamp'] = pd.to_datetime(df[self.col_mapping['date_time']])
        df_tt['inttime'] = df_tt['pystamp'].astype(int)
        df_tt['inttime'] = df_tt['inttime'].div(10**9)
        df_tt['Time [s]'] = df_tt['inttime']-df_tt['inttime'].iloc[0]
        return df_tt['Time [s]']