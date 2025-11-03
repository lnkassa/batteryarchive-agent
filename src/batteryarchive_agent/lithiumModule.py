# coding: utf-8
# Copyright 2025 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

import logging
import pandas as pd
import pathlib

from .abstractModule import AbstractModule
from .lithiumCell import LithiumCell

class LithiumModule(AbstractModule):
    def __init__(self, path:str, md:pd.DataFrame):
        self.module_metadata_table = 'module_metadata'
        self.cycle_metadata_table = 'cycle_metadata'
        self.timeseries_table = 'cycle_timeseries'
        self.buffer_table = 'cycle_timeseries_buffer'
        self.stats_table = 'cycle_stats'
        self.md = md #metadata from module?
        self.child_type = type(LithiumCell)

        self.module_id = self.md['module_id']
        self.set_file_id()
        self.set_tester()
        self.set_file_type()
        self.set_path(path)
    

    def set_tester(self):
        self.tester = self.md['tester']
        
    def set_path(self, path:str):
        self.file_path = pathlib.PurePath(path).joinpath(self.file_id)
        self.config_path = pathlib.PurePath(self.file_path).joinpath(self.file_id + '.xlsx')
    
    def set_file_id(self):
        self.file_id = self.md['file_id'] #use get functions
    
    def set_file_type(self):
        self.file_type = self.md['file_type']

    def populate_metadata(self) -> tuple[pd.DataFrame,pd.DataFrame]:
        # Build module metadata
        df_module_md = pd.DataFrame()
        df_module_md['module_id'] = [self.md['module_id']]
        df_module_md['configuration'] = [self.md['configuration']] #capitalization issue
        df_module_md['num_parallel'] = [self.md['# cells in parallel']]
        df_module_md['num_series'] = [self.md['# cell in series']]
        # create virtual 'cell_list.xlsx' as a dataframe
        #config = pd.read_excel(self.config_path)
        num_cells = df_module_md.at[0, 'num_parallel'] * df_module_md.at[0, 'num_series']
        list_cell_md = []
        list_cycle_md = []
        for c in range(num_cells): 
            list_cell_row = (
                'internal',
                 self.module_id + '_' + self.file_id,
                 self.md['cathode'],
                 self.md['anode'],
                 self.md['source'],
                 self.md['ah'],
                 self.md['form_factor'],
                 self.md['tester'],
                 self.md['test']
            )
            list_cycle_row = (
                self.module_id + '_' + self.file_id,
                self.md['temperature'],
                self.md['soc_max'],
                self.md['soc_min'],
                self.md['crate_c'],
                self.md['crate_d']
            )
            list_cell_md.append(list_cell_row)
            list_cycle_md.append(list_cycle_row)
        df_cell_md = pd.DataFrame(list_cell_md, columns=['file_id', 'cell_id', 'cathode', 'anode', 'source', 'ah', 'form_factor', 'tester', 'test'])
        df_cycle_md = pd.DataFrame(list_cycle_md, columns=['cell_id', 'temperature', 'soc_max', 'soc_min', 'crate_c', 'crate_d'])
        return df_module_md, df_cell_md, df_cycle_md
    
    def create_cell_df(self, path:str, row) -> pd.DataFrame:
        #creates timeseries dataframe for a single cell from the module data timeseries excel file
        data_files = [file for file in pathlib.Path(path).glob('./*') if not any(part.startswith('.') for part in file.parts)]
        #data_files = [file for file in data_files if not self.configuration_file and "~$" not in os.path.basename(file)]
        df_module_file = pd.ExcelFile(data_files[0])
        df_cell_ts = pd.DataFrame
        #Column names
        df_cell_ts.columns = ['Date_Time', 'Cycle_Index', 'Test_Time(s)', 'Current(A)', 'Voltage(V)']
        #Timeseries data
        df_cell_ts['Date_Time'] = df_module_file[row['Timestamp Column']]
        df_cell_ts['Cycle_Index'] = df_module_file[row['Cycle index column']]
        df_cell_ts['Test_Time(s)'] = df_module_file[row['Test time column']]
        df_cell_ts['Current(A)'] = df_module_file[row['Current column']]
        df_cell_ts['Voltage(V)'] = df_module_file[row['Voltage column']]
        return df_cell_ts