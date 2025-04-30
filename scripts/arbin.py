# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

import pandas as pd
import yaml

from abstractFileType import AbstractFileType

class Arbin(AbstractFileType):

    def __init__(self):
        with open('mapper.yaml', 'r') as file:
            mapper = yaml.safe_load_all(file)
            for row in mapper:
                if row['tester'] == 'arbin':
                    mapper = row
                    break
        self.tester =  mapper['tester']
        self.reader_func = mapper['reader_func']
        self.col_mapping = mapper['column_names']
        self.unit_mult = mapper['unit_multipliers']
        
    def file_to_df(self, path):
        read_func = getattr(pd, self.reader_func)
        if self.reader_func=='read_excel': #is there a better way to choose this if needed?
            df_ts_file = read_func(path, None)
            for sheet in df_ts_file.keys():
                if 'channel' in sheet.lower():
                    return df_ts_file[sheet], sheet
        else:
            return read_func(path), None