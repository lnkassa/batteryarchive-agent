#!/usr/bin/env python
# coding: utf-8

import os
import glob
import pandas as pd
import numpy as np #for mat files
import h5py #for mat files
pd.options.mode.chained_assignment = None  # default='warn'
import yaml
import sys, getopt
import logging
import logging.config
import time

from abstraction import *

# Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.
    
class arbin():
    def __init__(self):
        self.column_mapping = {'cycle_index':'Cycle_Index',
                               'test_time':'Test_Time(s)',
                               'i':'Current(A)',
                               'v':'Voltage(V)',
                               'date_time':'Date_Time'}

class liCell(abstractCell):
    def __init__(self,md):
        super().__init__(md)
        self.cell_metadata_table = 'cell_metadata'
        self.cycle_metadata_table = 'cycle_metadata'
        self.timeseries_table = 'cycle_timeseries'
        self.buffer_table = 'cycle_timeseries_buffer'
        self.stats_table = 'cycle_stats'
        self.batt_type = 'li-ion'
        
    def calc_timeseries(self, df_t, ID, engine):
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
    
    def calc_stats(self, df_t, ID, engine):
        logging.info('calculate cycle time and cycle statistics')
        no_cycles = int(df_t['cycle_index'].max())
        a = [x for x in range(no_cycles-30, no_cycles)]
        # Initialize the cycle_data time frame
        a = [x for x in range(no_cycles-30, no_cycles)]  # using loops
        df_c = pd.DataFrame(data=a, columns=["cycle_index"]) 
    
        df_c['cell_id'] = ID
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
                    df_f_c = df_f[df_f['i'] > 0]
                    df_f_d = df_f[df_f['i'] < 0]
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
    
    def buffer(self, engine, conn, path, cell_id, file_id, mapper): ##conflict need to pass file_type
        # with open('mapper.yaml', 'r') as file:
        #     mapper = yaml.safe_load(file)
        logging.info('adding files')
        md = self.cell_md
        file_type = md.iloc[0]['file_type']
        file_path = os.path.join(path, file_id)
        print(file_path)
        listOfFiles = glob.glob(file_path + '*.'+ file_type +'*') ##rconflict
        #listOfFiles = glob.glob(file_path + '*.xls*')
        for i in range(len(listOfFiles)):
            listOfFiles[i] = listOfFiles[i].replace(file_path[:-1], '')
        logging.info('list of files to add: ' + str(listOfFiles))
        df_file = pd.DataFrame(listOfFiles, columns=['filename'])
        df_file.sort_values(by=['filename'], inplace=True)
        if df_file.empty:
            print('No files to import found.')
            return
        df_file['cell_id'] = cell_id
        start_time = time.time()
        cycle_index_max = 0
        for ind in df_file.index:
            filename = df_file['filename'][ind]
            cellpath = file_path + filename
            print(cellpath)
            logging.info('buffering file: ' + filename)
            '''
            if 'sheetname' in mapper: #check if file has multiple sheets
                timeseries_sheet = self.get_sheetname(cell_id,conn,cellpath,filename)
                if timeseries_sheet == None:
                    print('No matching sheetname found. Buffering for cell '+ cell_id + ' failed.') 
                    continue
                else:
                    df_time_series = pd.DataFrame()
            else: 
                timeseries_sheet = '' #what to call this
            '''
            if True:
                df_time_series = pd.DataFrame()
                timeseries_sheet = ''
            # if mod_flag==True: #if this cell is part of a module, the timeseries df is passed down from the module class
            #      df_time_series_file = df_cell_ts
            # elif os.path.exists(cellpath):
            #     if file_type=='csv':
            #         df_time_series_file = pd.read_csv(cellpath)
            #     elif file_type=='excel':
                try:
                    df_time_series_file = file_reader(cellpath, mapper['reader_func'],sheet_name=timeseries_sheet)
                except ValueError as e:
                    print('\nI got a ValueError - reason: ' + str(e))
                    print('Make sure metadata and data files (and hidden files) are closed. \n')
                try:
                    keys = {'cycle_index','i','v','date_time','test_time','env_temperature','cell_temperature'}
                    for key in keys:
                        if key in mapper['column_names']:
                            df_time_series[key] = df_time_series_file[mapper['column_names'][key]]
                        if 'date_time' == key and 'test_time' not in mapper['column_names']:
                            df_time_series['test_time']=convert_datetime_time(df_time_series_file,mapper['column_names'][key])
                        elif 'test_time' not in mapper['column_names'] and 'date_time' not in mapper['column_names']:#change to check if all necessary columns exist
                            print('There is no time data in the timeseries file.')
                    df_time_series['cell_id'] = cell_id
                    df_time_series['sheetname'] = filename + "|" + timeseries_sheet
                    df_time_series['component_level'] = 'cell'
                    cycle_index_file_max = df_time_series.cycle_index.max()
                    if cycle_index_file_max > cycle_index_max:
                        cycle_index_max = cycle_index_file_max

                    print('saving sheet: ' + timeseries_sheet + ' with max cycle: ' +str(cycle_index_file_max))

                    df_time_series.to_sql('cycle_timeseries_buffer', con=engine, if_exists='append', chunksize=1000, index=False)

                    print("saved=" + timeseries_sheet + " time: " + str(time.time() - start_time))

                    start_time = time.time()

                except KeyError as e:
                    print("I got a KeyError - reason " + str(e))
                    print("processing:" + timeseries_sheet + " time: " + str(time.time() - start_time))
                    start_time = time.time()

        return cycle_index_max
    
    def populate_metadata(self, df_c_md): ##conflict need to pass cell type from main
        # Build cell metadata
        df_cell_md = pd.DataFrame()
        df_cell_md['cell_id'] = [df_c_md['cell_id']]
        df_cell_md['anode'] = [df_c_md['anode']]
        df_cell_md['cathode'] = [df_c_md['cathode']]
        df_cell_md['source'] = [df_c_md['source']]
        df_cell_md['ah'] = [df_c_md['ah']]
        df_cell_md['form_factor'] = [df_c_md['form_factor']]
        df_cell_md['test'] = [df_c_md['test']]
        df_cell_md['tester'] = [df_c_md['tester']]
        # Build cycle metadata
        df_cycle_md = pd.DataFrame()
        df_cycle_md['cell_id'] = [df_c_md['cell_id']]
        df_cycle_md['crate_c'] = [df_c_md['crate_c']]
        df_cycle_md['crate_d'] = [df_c_md['crate_d']]
        df_cycle_md['soc_max'] = [df_c_md['soc_max']]
        df_cycle_md['soc_min'] = [df_c_md['soc_min']]
        df_cycle_md['temperature'] = [df_c_md['temperature']]

        return df_cell_md, df_cycle_md

class flowCell(abstractCell):
    def __init__(self,md):
        super().__init__(md)
        self.cell_metadata_table = 'flow_cell_metadata'
        self.cycle_metadata_table = 'flow_cycle_metadata'
        self.timeseries_table = 'flow_cycle_timeseries'
        self.buffer_table = 'flow_cycle_timeseries_buffer'
        self.stats_table = 'flow_cycle_stats'
        self.batt_type = 'flow'

    def calc_stats(self):
    #'cmltv' = 'cumulative'
        if self.batt_type == 'flow':
            with engine.connect() as conn: ## conflict for flow
                init = pd.read_sql("select max(e_c_cmltv) from " + self.stats_table + " where cell_id='"+ID+"'", conn).iloc[0,0] #for continuity btwn calc_stats calls
                init = 0 if init == None else init
                df_c['e_c_cmltv'] = init 
                init = pd.read_sql("select max(e_d_cmltv) from " + self.stats_table + " where cell_id='"+ID+"'", conn).iloc[0,0]
                init = 0 if init == None else init
            df_c['e_d_cmltv'] = init ## conflict
            df_c['e_eff_cmltv'] = 0 ##conflict 
        if self.batt_type == 'flow':
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
                        'e_c_cmltv': float, ##conflict
                        'e_d_cmltv': float, ##conflict
                        'v_c_mean': float,
                        'v_d_mean': float,
                        'test_time': float,
                        'ah_eff': float,
                        'e_eff': float,
                        'e_eff_cmltv': float ##conflict
                    }
        df_f['w'] = 0
        if self.batt_type == 'flow':
            df_t.loc[df_t.cycle_index == x, 'w'] = df_f['i'] * df_f['v'] 
            df_c.iloc[c_ind, df_c.columns.get_loc('e_c_cmltv')] = df_f['e_c'].max() + df_c.iloc[c_ind-1,df_c.columns.get_loc('e_c_cmltv')] ##conflict
            df_c.iloc[c_ind, df_c.columns.get_loc('e_d_cmltv')] = df_f['e_d'].max() + df_c.iloc[c_ind-1,df_c.columns.get_loc('e_d_cmltv')] ##conflict

            if df_c.iloc[c_ind, df_c.columns.get_loc('e_c_cmltv')] == 0: ##conflict
                df_c.iloc[c_ind, df_c.columns.get_loc('e_eff_cmltv')] = 0
            else:
                df_c.iloc[c_ind, df_c.columns.get_loc('e_eff_cmltv')] = df_c.iloc[c_ind, df_c.columns.get_loc('e_d_cmltv')] / \
                                                            df_c.iloc[c_ind, df_c.columns.get_loc('e_c_cmltv')]
            
    def populate_cycle_metadata(df_c_md):
        # Build cell metadata
        df_cell_md = pd.DataFrame()
        df_cell_md['cell_id'] = [df_c_md['cell_id']]
        df_cell_md['flow_pattern'] = [df_c_md['flow pattern']]
        df_cell_md['ne_material'] = [df_c_md['NE material']]
        df_cell_md['pe_material'] = [df_c_md['PE material']]
        df_cell_md['membrane'] = [df_c_md['membrane']]
        df_cell_md['membrane_size'] = [df_c_md['membrane size (cm2)']]
        df_cell_md['ne_active'] = [df_c_md['NE active']]
        df_cell_md['initial_ne_active'] = [df_c_md['initial [NE active], M']]
        df_cell_md['pe_active'] = [df_c_md['PE active']]
        df_cell_md['initial_pe_active'] = [df_c_md['initial [PE active], M']]
        df_cell_md['ne_volume'] = [df_c_md['NE volume (L)']]
        df_cell_md['pe_volume'] = [df_c_md['PE volume (L)']]  
        df_cell_md['flow_rate'] = [df_c_md['flow rate (L/min)']]
        df_cell_md['test_type'] = [df_c_md['test type']]
        #df_cell_md['source'] = [df_c_md['source']]
        df_cell_md['test'] = [df_c_md['test']]
        df_cell_md['tester'] = [df_c_md['tester']]
        # Build cycle metadata - TODO
        df_cycle_md = pd.DataFrame()
        return df_cell_md, df_cycle_md

class liModule(abstractModule):
    def __init__(self):
        super().__init__()

        
def main(argv):

    # command line variables that can be used to run from an IDE without passing arguments
    mode = 'env'
    path = r'\\'

    # initializing the logger
    logging.basicConfig(format='%(asctime)s %(message)s', filename='blc-python.log', level=logging.DEBUG)
    logging.info('starting')

    try:
        opts, args = getopt.getopt(argv, "ht:p:", ["dataType=","path="])
    except getopt.GetoptError:
        print('run as: data_import_agent.py -t <dataType> -p <path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('run as: data_import_agent.py -t <dataType> -p <path>')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-t", "--dataType"):
            data_type = arg

    # read database connection
    conn = ''
    try:
        env = yaml.safe_load(open('../env'))
        x = env.split(" ")
        for i in x:
            j = i.split("=")
            if j[0] == 'LOCAL_CONNECTION':
                conn =  j[1]
    except:
        print("Error opening env file:", sys.exc_info()[0])
    
        # read configuration values
    data = yaml.safe_load(open('battery-blc-library.yaml'))

    plot = data['environment']['PLOT']
    save = data['environment']['SAVE']
    style = data['environment']['STYLE']

    # use default if env file not there
    if conn == '':
        conn = data['environment']['DATABASE_CONNECTION']

    logging.info('command line: ' + str(opts))
    logging.info('configuration: ' + str(data))

    mod_flag=False
    if data_type == 'li-cell':
        df_md = pd.read_excel(os.path.join(path, '') + "cell_list.xlsx")
        imp = liCell(df_md)
    elif data_type == 'flow-cell':
        df_md = pd.read_excel(os.path.join(path, '') + "cell_list.xlsx")
        imp = flowCell(df_md)
    elif data_type == 'li-module':
        df_md = pd.read_excel(os.path.join(path,'') + "module_list.xlsx")
        imp = liModule()
        mod_flag=True
    imp.add_data(conn, path, map)


if __name__ == "__main__":
    main(sys.argv[1:])
