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
        self.md = md 
        self.child_type = type(LithiumCell)

        self.module_id = self.md['module_id']
        self.set_file_id()
        self.set_tester()
        self.set_file_type()
        self.set_path(path)
        self.set_num_cells()
    

    def set_tester(self):
        self.tester = self.md['tester']
        
    def set_path(self, path:str):
        self.file_path = pathlib.PurePath(path).joinpath(self.file_id)
        self.config_path = pathlib.PurePath(self.file_path).joinpath(self.file_id + '.xlsx')
    
    def set_file_id(self):
        self.file_id = self.md['file_id']
    
    def set_file_type(self):
        self.file_type = self.md['file_type']

    def set_num_cells(self):
        self.num_cells = self.md['# cells in parallel'] * self.md['# cell in series']


    def calc_timeseries(self, df_t:pd.DataFrame) -> pd.DataFrame:
        df_t['cycle_time'] = 0
        no_cycles = int(df_t['cycle_index'].max())

        for c_ind in pd.RangeIndex(30):
            x = no_cycles + c_ind - 29
            
            df_f = df_t[df_t['cycle_index'] == x]
            df_f['ah_c'] = 0
            df_f['e_c'] = 0
            df_f['ah_d'] = 0
            df_f['e_d'] = 0

            if not df_f.empty:
                try:
                    df_f['dt'] = df_f['test_time'].diff() / 3600.0
                    df_f = self.calc_cycle_quantities(df_f)
                    df_t['cycle_time'] = df_t['cycle_time'].astype('float64') #to address dtype warning
                    
                    df_t.loc[df_t.cycle_index == x, 'cycle_time'] = df_f['cycle_time']
                    df_t.loc[df_t.cycle_index == x, 'ah_c'] = df_f['ah_c']
                    df_t.loc[df_t.cycle_index == x, 'e_c'] = df_f['e_c']
                    df_t.loc[df_t.cycle_index == x, 'ah_d'] = df_f['ah_d']
                    df_t.loc[df_t.cycle_index == x, 'e_d'] = df_f['e_d']
                except Exception as e:
                    logging.info("Exception @ x: " + str(x))
                    logging.info(e)
        df_tt = df_t[df_t['cycle_index'] > 0]
        return df_tt
    
    def calc_cycle(self, df_t:pd.DataFrame, *args) -> pd.DataFrame:
        logging.info('calculate cycle time and cycle statistics')
        no_cycles = int(df_t['cycle_index'].max())
        # Initialize the cycle_data time frame
        a = [x for x in range(no_cycles-30, no_cycles)] 
        df_c = pd.DataFrame(data=a, columns=["cycle_index"]) 

        df_c['cell_id'] = self.module_id
        df_c['cycle_index'] = 0
        df_c['v_max'] = 0
        df_c['i_max'] = 0
        df_c['v_min'] = 0
        df_c['i_min'] = 0
        df_c['ah_c'] = 0
        df_c['ah_d'] = 0
        df_c['e_c'] = 0
        df_c['e_d'] = 0
        df_c['v_c_mean'] = 0
        df_c['v_d_mean'] = 0
        df_c['test_time'] = 0
        df_c['ah_eff'] = 0
        df_c['e_eff'] = 0
        df_c['component_level'] = 'module'
        convert_dict = {'cell_id': str,
            'cycle_index': int,
            'v_max': float,
            'i_max': float,
            'v_min': float,
            'i_min': float,
            'ah_c': float,
            'ah_d': float,
            'e_c': float,
            'e_d': float,
            'v_c_mean': float,
            'v_d_mean': float,
            'test_time': float,
            'ah_eff': float,
            'e_eff': float,
            'component_level':str
        }
        df_c = df_c.astype(convert_dict)
        for c_ind in df_c.index:
            x = no_cycles + c_ind - 29
            
            df_f = df_t[df_t['cycle_index'] == x]
            df_f['ah_c'] = 0
            df_f['e_c'] = 0
            df_f['ah_d'] = 0
            df_f['e_d'] = 0
            
            if not df_f.empty:
                try:
                    df_f['dt'] = df_f['test_time'].diff() / 3600.0
                    df_f_c = df_f[df_f['i'] > 0]
                    df_f_d = df_f[df_f['i'] < 0]

                    df_f = self.calc_cycle_quantities(df_f)
                    df_c.iloc[c_ind, df_c.columns.get_loc('cycle_index')] = x
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_max')] = df_f.loc[df_f['v'].idxmax()].v
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_min')] = df_f.loc[df_f['v'].idxmin()].v
                    df_c.iloc[c_ind, df_c.columns.get_loc('i_max')] = df_f.loc[df_f['i'].idxmax()].i
                    df_c.iloc[c_ind, df_c.columns.get_loc('i_min')] = df_f.loc[df_f['i'].idxmin()].i
                    df_c.iloc[c_ind, df_c.columns.get_loc('test_time')] = df_f.loc[df_f['test_time'].idxmax()].test_time
                    
                    df_c.iloc[c_ind, df_c.columns.get_loc('ah_c')] = df_f['ah_c'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('ah_d')] = df_f['ah_d'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('e_c')] = df_f['e_c'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('e_d')] = df_f['e_d'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_c_mean')] = df_f_c['v'].mean()
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_d_mean')] = df_f_d['v'].mean()
                   
                    if df_c.iloc[c_ind, df_c.columns.get_loc('ah_c')] == 0:
                        df_c.iloc[c_ind, df_c.columns.get_loc('ah_eff')] = 0
                    else:
                        df_c.iloc[c_ind, df_c.columns.get_loc('ah_eff')] = df_c.iloc[c_ind, df_c.columns.get_loc('ah_d')] / \
                                                                        df_c.iloc[c_ind, df_c.columns.get_loc('ah_c')]
                    if df_c.iloc[c_ind, df_c.columns.get_loc('e_c')] == 0:
                        df_c.iloc[c_ind, df_c.columns.get_loc('e_eff')] = 0
                    else:
                        df_c.iloc[c_ind, df_c.columns.get_loc('e_eff')] = df_c.iloc[c_ind, df_c.columns.get_loc('e_d')] / \
                                                                        df_c.iloc[c_ind, df_c.columns.get_loc('e_c')]

                except Exception as e:
                    logging.info("Exception @ x: " + str(x))
                    logging.info(e)
                    
        logging.info("cycle: " + str(x))
        logging.info("cell_id: "+ df_c['cell_id'])
        df_cc = df_c[df_c['cycle_index'] > 0]
        return df_cc
    
    def calc_cycle_quantities(self, df:pd.DataFrame) -> pd.DataFrame:
        logging.info('calculate quantities used in statistics')

        tmp_arr = df[["test_time", "i", "v", "ah_c", 'e_c', 'ah_d', 'e_d', 'cycle_time']].to_numpy()

        start = 0
        last_time = 0
        last_i = 0
        last_v = 0
        last_ah_c = 0
        last_e_c = 0
        last_ah_d = 0
        last_e_d = 0
        initial_time = 0

        for x in tmp_arr:
            if start == 0:
                start += 1
                initial_time = x[0]
            else:
                if x[1] > 0:
                    x[3] = (x[0] - last_time) * (x[1] + last_i) * 0.5 + last_ah_c
                    x[4] = (x[0] - last_time) * (x[1] + last_i) * 0.5 * (x[2] + last_v) * 0.5 + last_e_c
                    last_ah_c = x[3]
                    last_e_c = x[4]
                elif x[1] < 0:
                    x[5] = (x[0] - last_time) * (x[1] + last_i) * 0.5 + last_ah_d
                    x[6] = (x[0] - last_time) * (x[1] + last_i) * 0.5 * (x[2] + last_v) * 0.5 + last_e_d
                    last_ah_d = x[5]
                    last_e_d = x[6]

            x[7] = x[0] - initial_time

            last_time = x[0]
            last_i = x[1]
            last_v = x[2]
            
        df_tmp = pd.DataFrame(data=tmp_arr[:, [3]], columns=["ah_c"])
        df_tmp.index += df.index[0]
        df['ah_c'] = df_tmp['ah_c']/3600.0

        df_tmp = pd.DataFrame(data=tmp_arr[:, [4]], columns=["e_c"])
        df_tmp.index += df.index[0]
        df['e_c'] = df_tmp['e_c']/3600.0

        df_tmp = pd.DataFrame(data=tmp_arr[:, [5]], columns=["ah_d"])
        df_tmp.index += df.index[0]
        df['ah_d'] = -df_tmp['ah_d']/3600.0

        df_tmp = pd.DataFrame(data=tmp_arr[:, [6]], columns=["e_d"])
        df_tmp.index += df.index[0]
        df['e_d'] = -df_tmp['e_d']/3600.0
        
        df_tmp = pd.DataFrame(data=tmp_arr[:, [7]], columns=["cycle_time"])
        df_tmp.index += df.index[0]
        df['cycle_time'] = df_tmp['cycle_time']
        return df
    
    def populate_metadata(self) -> tuple[pd.DataFrame,pd.DataFrame]:
        # Build module metadata
        df_module_md = pd.DataFrame()
        df_module_md['module_id'] = [self.md['module_id']]
        df_module_md['configuration'] = [self.md['configuration']] # ensure capitalization correct in md file
        df_module_md['num_parallel'] = [self.md['# cells in parallel']]
        df_module_md['num_series'] = [self.md['# cell in series']]
        # Create virtual 'cell_list.xlsx' as a dataframe
        list_cell_md = []
        list_cycle_md = []
        for c in range(self.num_cells): 
            list_cell_row = (
                'internal',
                self.module_id + '_' + str(c+1), #create cell_id from module_id
                self.md['cathode'],
                self.md['anode'],
                self.md['temperature'],
                self.md['soc_max'],
                self.md['soc_min'],
                self.md['source'],
                self.md['crate_c'],
                self.md['crate_d'],
                self.md['ah'],
                self.md['form_factor'],
                self.md['tester'],
                self.md['test'],
                self.md['file_type']
            )
            list_cell_md.append(list_cell_row)
        df_cell_md = pd.DataFrame(list_cell_md, columns=['file_id', 'cell_id', 'cathode', 'anode', 'temperature', 'soc_max', 'soc_min', 'source', 'crate_c', 'crate_d', 'ah', 'form_factor', 'tester', 'test', 'file_type'])
        return df_module_md, df_cell_md
    
    def create_df(self, module_df_ts:pd.DataFrame, row) -> pd.DataFrame:
        # Creates timeseries dataframe for a single cell from the module data timeseries excel file
        df_ts = pd.DataFrame(columns = ['date_time', 'cycle_index', 'test_time', 'i', 'v'])
        df_ts['date_time'] = module_df_ts[row['Timestamp column']]
        df_ts['cycle_index'] = module_df_ts[row['Cycle index column']]
        df_ts['test_time'] = module_df_ts[row['Test time column']]
        df_ts['i'] = module_df_ts[row['Current column']]
        df_ts['v'] = module_df_ts[row['Voltage column']]
        df_ts['env_temperature'] = module_df_ts[row['Ambient temperature column']]
        df_ts['component_level'] = row['Type'].lower()
        if row['Type'] == 'Cell':
            df_ts['cell_temperature'] = module_df_ts[row['Internal temperature column']]
        elif row['Type'] == 'Module':
            df_ts['cell_id'] = self.module_id
        return df_ts
    