#!/usr/bin/env python
# coding: utf-8

import os
import argparse 
import glob
import pandas as pd
import numpy as np #for mat files
import h5py #for mat files
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
import psycopg2
from sqlalchemy import create_engine
import yaml
import sys, getopt
import logging
import logging.config
import time
from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine, select, insert, update, delete, func
from io import BytesIO ##new

# Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.
metadata_obj = MetaData()

class abstractFileType():
    def __init__(self):
        return
    
class abstractModule():
    def __init__(self):
        self.module_metadata_table = 'module_metadata'
        self.cycle_metadata_table = 'cycle_metadata'
        self.timeseries_table = 'cycle_timeseries'
        self.buffer_table = 'cycle_timeseries_buffer'
        self.stats_table = 'cycle_stats'
    def add_data(self, df_md, conn, path, slash, mod_flag, **kwargs): 
        logging.info('add modules')

        # Process one module at a time
        for ind in df_md.index:

            row = df_md[ind]
            module_id = df_md['module_id'][ind]
            file_id = df_md['file_id'][ind]
            self.configuration_file=os.path.join(path, f"{file_id}.xlsx")
            #tester = df_md['tester'][ind]
            #file_type = df_md['file_type'][ind]
            #source = df_md['source'][ind]

            logging.info("add file: " + file_id + " module: " + module_id)

            df_md = df_md.iloc[ind]
            print(df_md)

            engine = create_engine(conn)

            # check if the module is already there and report status

            status = self.get_status(module_id, conn) ##rconflict

            if status=="completed":
                print("skip module: " + module_id + '\n') ##rconflict module

            if status=='new': 

                logging.info('save module metadata') ##conflict module
                df_module_md, df_c_md = self.populate_metadata(self, df_md, file_id) ##conflict module?
                df_module_md.to_sql(self.module_metadata_table, con=engine, if_exists='append', chunksize=1000, index=False)##rconflict
                #logging.info('save cycle metadata')
                #df_cycle_md.to_sql(self._metadata_table, con=engine, if_exists='append', chunksize=1000, index=False)##rconflict

                status = 'buffering'

                self.set_status(module_id, status, conn)##rconflict

            if status=='buffering':
                print("buffering module: " + module_id)

                file_path = path + file_id + slash

                #replacing selector with one function that will differ in each class
                cycle_index_max = self.buffer(file_path, conn, mod_flag=mod_flag, df_cell_md=df_c_md, md_row=row, sl=slash)

                print('start import')

                status = "processing"

                self.set_status(module_id, status, conn)

            if status == 'processing':

                #read the data back in chunks.
                block_size = 30

                cycle_index_max = self.get_cycle_index_max(module_id, conn, self.buffer_table) ##rconflict
                cycle_stats_index_max = self.get_cycle_index_max(module_id, conn, self.stats_table) ##rconflict

                print("max cycle: " + str(cycle_index_max))

                start_cycle = 1
                start_time = time.time()

                for i in range(cycle_index_max+1):
                
                    if (i-1) % block_size == 0 and i > 0 and i>cycle_stats_index_max:

                        start_cycle = i
                        end_cycle = start_cycle + block_size - 1

                        sql_module =  " cell_id='" + module_id + "'" 
                        sql_cycle = " and cycle_index>=" + str(start_cycle) + " and cycle_index<=" + str(end_cycle)
                        sql_str = "select * from " + self.buffer_table + " where " + sql_module + sql_cycle + " order by test_time"##rconflict

                        print(sql_str)
                        df_ts = pd.read_sql(sql_str, conn)

                        df_ts.drop('sheetname', axis=1, inplace=True)

                        if not df_ts.empty:
                            start_time = time.time()
                            df_cycle_stats, df_cycle_timeseries = self.calc_stats(df_ts, module_id, engine)
                            print("calc_stats time: " + str(time.time() - start_time))
                            logging.info("calc_stats time: " + str(time.time() - start_time))

                            start_time = time.time()
                            df_cycle_stats.to_sql(self.stats_table, con=engine, if_exists='append', chunksize=1000, index=False)##rconflict
                            print("save stats time: " + str(time.time() - start_time))
                            logging.info("save stats time: " + str(time.time() - start_time))

                            start_time = time.time()
                            df_cycle_timeseries.to_sql(self.timeseries_table, con=engine, if_exists='append', chunksize=1000, index=False) ##rconflict
                            print("save timeseries time: " + str(time.time() - start_time))
                            logging.info("save timeseries time: " + str(time.time() - start_time))


                status='completed'

                self.set_status(module_id, status, conn)

                self.clear_buffer(module_id, conn)

    def setup_buffer(self, file_path, conn, mod_flag, **kwargs):
        df_cell_md = kwargs[df_cell_md]
        df_cell_ts = kwargs[df_cell_ts]
        slash = kwargs[sl]
        md_row = kwargs[md_row]
        if df_cell_md.empty:
            print('There is no cell data to add.')
        else:
            for index, row in self.configuration_file.iterrows():
                tester = md_row['tester']
                if row['Type'] == 'Module':
                    self.buffer(module_id=md_row['module_id'])
                elif row['Type'] == 'Cell': 
                    df_cell_ts = self.create_cell_df(file_path, row)
                    if tester=='arbin':
                        cell = liCellArbin() ##conflict pass parent id
                        cell.add_data(df_cell_md, conn, file_path, slash, df_cell_ts, mod_flag) ##confict pass df as single row
                    #elif tester=='generic':
                        #cell = liCellCsv() ##conflict pass parent id
                        #cell.add_data(df_cell_md, conn, file_path, slash) ##conflict pass df as single row?
                
    def buffer(self, **kwargs):
        config = pd.ExcelFile(self.configuration_file)
        df_module_data = kwargs[df_module_data]
        module_id = kwargs[module_id]
        df_m_data = pd.DataFrame
        for index, row in config:
            if row["Voltage column"]:
                df_m_data["v"] = df_module_data[row["Voltage column"]]
            if row["Current column"]:
                df_m_data["i"] = df_module_data[row["Current column"]]
            if row["Internal temperature column"]:
                df_m_data["cell_temperature"] = df_module_data[row["Internal temperature column"]]
            if row["Ambient temperature column"]:
                df_m_data["env_temperature"] = df_module_data[row["Ambient temperature column"]]
            df_m_data["date_time"] = df_module_data[row["Timestamp column"]]
            df_m_data["test_time"] = df_module_data[row["Test time column"]]
            df_m_data["cycle_index"] = df_module_data[row["Cycle index column"]]
            df_m_data["cell_id"] = module_id ##should we change this in the schema?
            df_m_data["component_level"] = 'module'

    def create_cell_df(self, path, row):
        #creates timeseries dataframe for a single cell from the module data timeseries excel file
        data_files = glob.glob(os.path.join(path, f"*.xlsx"))
        data_files = [file for file in data_files if not self.configuration_file and "~$" not in os.path.basename(file)]
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
    
    def populate_metadata(self, df_m_md, file_id):
        # Build module metadata
        df_module_md = pd.DataFrame()
        df_module_md['module_id'] = [df_m_md['module_id']]
        df_module_md['configuration'] = [df_m_md['configuration']]
        df_module_md['num_parallel'] = [df_m_md['cathode']]
        df_module_md['num_series'] = [df_m_md['source']]
        # create virtual 'cell_list.xlsx' as a dataframe
        config = pd.ExcelFile(self.configuration_file)
        insert_md = pd.DataFrame({'cathode':None,'anode':None,'temperature':None,'soc_max':None,'soc_min':None,'source':None,'crate_c':None,'crate_d':None,'ah':None,'form_factor':None,'tester':None,'test':None,'file_type':None})
        insert_md = df_module_md[insert_md.columns]
        df_cell_md = pd.DataFrame()
        for index, row in config: 
            df_cell_md.loc[index] = insert_md
            if row['Type'] == 'Cell':
                df_cell_md.loc[index] = insert_md
                df_cell_md.at[index,'cell_id'] = df_module_md['module_id'] + '_' + row['Name'] #create cell_id by concat
                df_cell_md.at[index,'file_id'] = file_id
        print(df_cell_md) #temp for testing
        return df_module_md, df_cell_md
    
    def get_status(self, module_id, conn):
        table = Table(self.module_metadata_table, metadata_obj, autoload_with=engine)
        stmt = select(table.c.status).where(table.c.module_id==module_id)
        with engine.connect() as conn:
            result = conn.execute(stmt).first()
        if result is not None:
            return result[0]
        else:
            return None
    
    def set_status(self, module_id, status, conn):
        sql_str = "update " + self.module_metadata_table + " set status = '" + status + "' where cell_id = '" + module_id + "'" ##rconflict
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute(sql_str)
        db_conn.commit()
        curs.close()
        db_conn.close()
        return
    
    def clear_buffer(self, module_id, conn):
        # this method will delete data for a module_id. Use with caution as there is no undo
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute("delete from " + self.buffer_table + " where cell_id='" + module_id + "'") ##conflict
        db_conn.commit()
        curs.close()
        db_conn.close()
        return
        
class abstractCell():
    def __init__(self, md, slash):
        self.cell_metadata_table = 'cell_metadata'
        self.cycle_metadata_table = 'cycle_metadata'
        self.timeseries_table = 'cycle_timeseries'
        self.buffer_table = 'cycle_timeseries_buffer'
        self.stats_table = 'cycle_stats'
        self.cell_md = md #to get fixed md
        self.slash = slash

    #add cells to the database
    def add_data(self, conn, path, slash, mapper): ##conflict how to pass all tables
        #optional args: df_cell_ts
        #df_cell_ts = kwargs[df_cell_ts]
        logging.info('add cells')

        # Process one cell at a time
        for ind in self.cell_md.index:

            cell_id = self.cell_md['cell_id'][ind]
            file_id = self.cell_md['file_id'][ind]
            file_type = self.cell_md['file_type'][ind]
            source = self.cell_md['source'][ind]
            tester = self.cell_md['tester'][ind]
            mapper = self.create_mapper(tester)

            logging.info("add file: " + file_id + " cell: " + cell_id)

            df_tmp = self.cell_md.iloc[ind]
            print(df_tmp)

            df_cell_md, df_cycle_md = self.populate_metadata(df_tmp) ##conflict module?

            engine = create_engine(conn)

            # check if the cell is already there and report status

            status = self.get_status(cell_id, conn) ##conflict module

            if status=="completed":
                print("skip cell_id: " + cell_id + '\n') ##conflict module

            if status=='new': 
                logging.info('save cell metadata') ##conflict module
                df_cell_md.to_sql(self.cell_metadata_table, con=engine, if_exists='append', chunksize=1000, index=False)##rconflict
                logging.info('save cycle metadata')
                df_cycle_md.to_sql(self.cycle_metadata_table, con=engine, if_exists='append', chunksize=1000, index=False)##rconflict
                status = 'buffering'
                self.set_status(cell_id, status, conn)##conflict
            if status=='buffering':
                print("buffering cell_id: " + cell_id)
                #replacing selector with one function that will differ in each class
                cycle_index_max = self.buffer(engine, conn, path, cell_id, file_id, mapper)
                print('start import')
                status = "processing"
                self.set_status(cell_id, status, conn)
            if status == 'processing':
                # read the data back in chunks.
                block_size = 30
                cycle_index_max = self.get_cycle_index_max(cell_id, conn, self.buffer_table) ##rconflict
                cycle_stats_index_max = self.get_cycle_index_max(cell_id, conn, self.stats_table) ##rconflict
                print("max cycle: " + str(cycle_index_max))
                start_cycle = 1
                start_time = time.time()
                for i in range(cycle_index_max+1):
                
                    if (i-1) % block_size == 0 and i > 0 and i>cycle_stats_index_max:

                        start_cycle = i
                        end_cycle = start_cycle + block_size - 1

                        sql_cell =  " cell_id='" + cell_id + "'" 
                        sql_cycle = " and cycle_index>=" + str(start_cycle) + " and cycle_index<=" + str(end_cycle)
                        sql_str = "select * from " + self.buffer_table + " where " + sql_cell + sql_cycle + " order by test_time"##rconflict

                        print(sql_str)
                        df_ts = pd.read_sql(sql_str, conn)

                        df_ts.drop('sheetname', axis=1, inplace=True)

                        if not df_ts.empty:
                            start_time = time.time()
                            df_cycle_stats, df_cycle_timeseries = self.calc_stats(df_ts, cell_id, engine)
                            print("calc_stats time: " + str(time.time() - start_time))
                            logging.info("calc_stats time: " + str(time.time() - start_time))

                            start_time = time.time()
                            df_cycle_stats.to_sql(self.stats_table, con=engine, if_exists='append', chunksize=1000, index=False)##rconflict
                            print("save stats time: " + str(time.time() - start_time))
                            logging.info("save stats time: " + str(time.time() - start_time))

                            start_time = time.time()
                            df_cycle_timeseries.to_sql(self.timeseries_table, con=engine, if_exists='append', chunksize=1000, index=False) ##rconflict
                            print("save timeseries time: " + str(time.time() - start_time))
                            logging.info("save timeseries time: " + str(time.time() - start_time))


                status='completed'

                self.set_status(cell_id, status, conn)

                self.clear_buffer(cell_id, conn)

    def calc_stats(self, df_t, ID, engine):
        logging.info('calculate cycle time and cycle statistics')
        df_t['cycle_time'] = 0
        no_cycles = int(df_t['cycle_index'].max())
        # Initialize the cycle_data time frame
        a = [x for x in range(no_cycles-30, no_cycles)]  # using loops
        df_c = pd.DataFrame(data=a, columns=["cycle_index"]) 
        
        #'cmltv' = 'cumulative'
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
        if self.batt_type == 'flow':
            with engine.connect() as conn: ## conflict for flow
                init = pd.read_sql("select max(e_c_cmltv) from " + self.stats_table + " where cell_id='"+ID+"'", conn).iloc[0,0] #for continuity btwn calc_stats calls
                init = 0 if init == None else init
                df_c['e_c_cmltv'] = init 
                init = pd.read_sql("select max(e_d_cmltv) from " + self.stats_table + " where cell_id='"+ID+"'", conn).iloc[0,0]
                init = 0 if init == None else init
            df_c['e_d_cmltv'] = init ## conflict
            df_c['e_eff_cmltv'] = 0 ##conflict 
        df_c['v_c_mean'] = 0
        df_c['v_d_mean'] = 0
        df_c['test_time'] = 0
        df_c['ah_eff'] = 0
        df_c['e_eff'] = 0
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
        elif self.batt_type == 'li-ion':
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
            df_f['w'] = 0
            
            if not df_f.empty:
                try:
                    df_c.iloc[c_ind, df_c.columns.get_loc('cycle_index')] = x
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_max')] = df_f.loc[df_f['v'].idxmax()].v
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_min')] = df_f.loc[df_f['v'].idxmin()].v
                    df_c.iloc[c_ind, df_c.columns.get_loc('i_max')] = df_f.loc[df_f['i'].idxmax()].i
                    df_c.iloc[c_ind, df_c.columns.get_loc('i_min')] = df_f.loc[df_f['i'].idxmin()].i
                    df_c.iloc[c_ind, df_c.columns.get_loc('test_time')] = df_f.loc[df_f['test_time'].idxmax()].test_time
                    
                    df_f['dt'] = df_f['test_time'].diff() / 3600.0
                    df_f_c = df_f[df_f['i'] > 0]
                    df_f_d = df_f[df_f['i'] < 0]
                    df_f = self.calc_cycle_quantities(df_f)
                    df_t['cycle_time'] = df_t['cycle_time'].astype('float64') #to address dtype warning
                    
                    df_t.loc[df_t.cycle_index == x, 'cycle_time'] = df_f['cycle_time']
                    df_t.loc[df_t.cycle_index == x, 'ah_c'] = df_f['ah_c']
                    df_t.loc[df_t.cycle_index == x, 'e_c'] = df_f['e_c']
                    df_t.loc[df_t.cycle_index == x, 'ah_d'] = df_f['ah_d']
                    df_t.loc[df_t.cycle_index == x, 'e_d'] = df_f['e_d']
                    df_c.iloc[c_ind, df_c.columns.get_loc('ah_c')] = df_f['ah_c'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('ah_d')] = df_f['ah_d'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('e_c')] = df_f['e_c'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('e_d')] = df_f['e_d'].max()
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_c_mean')] = df_f_c['v'].mean()
                    df_c.iloc[c_ind, df_c.columns.get_loc('v_d_mean')] = df_f_d['v'].mean()
                    if self.batt_type == 'flow':
                        df_t.loc[df_t.cycle_index == x, 'w'] = df_f['i'] * df_f['v'] 
                        df_c.iloc[c_ind, df_c.columns.get_loc('e_c_cmltv')] = df_f['e_c'].max() + df_c.iloc[c_ind-1,df_c.columns.get_loc('e_c_cmltv')] ##conflict
                        df_c.iloc[c_ind, df_c.columns.get_loc('e_d_cmltv')] = df_f['e_d'].max() + df_c.iloc[c_ind-1,df_c.columns.get_loc('e_d_cmltv')] ##conflict

                        if df_c.iloc[c_ind, df_c.columns.get_loc('e_c_cmltv')] == 0: ##conflict
                            df_c.iloc[c_ind, df_c.columns.get_loc('e_eff_cmltv')] = 0
                        else:
                            df_c.iloc[c_ind, df_c.columns.get_loc('e_eff_cmltv')] = df_c.iloc[c_ind, df_c.columns.get_loc('e_d_cmltv')] / \
                                                                        df_c.iloc[c_ind, df_c.columns.get_loc('e_c_cmltv')]
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
        df_tt = df_t[df_t['cycle_index'] > 0]
        return df_cc, df_tt
    
    def buffer(self, engine, conn, path, cell_id, file_id, mapper): ##conflict need to pass file_type
        #file_type = kwargs[file_type]
        #cell_id = kwargs[cell_id]
        #df_cell_ts = kwargs[df_cell_ts]
        #optional args: source, engine
        logging.info('adding files')
        md = self.cell_md
        file_type = md.iloc[0]['file_type']
        file_path = path + self.slash + file_id + self.slash
        listOfFiles = glob.glob(file_path + '*.'+ file_type +'*') ##rconflict
        #listOfFiles = glob.glob(file_path + '*.xls*')
        for i in range(len(listOfFiles)):
            listOfFiles[i] = listOfFiles[i].replace(file_path[:-1], '')
        logging.info('list of files to add: ' + str(listOfFiles))
        df_file = pd.DataFrame(listOfFiles, columns=['filename'])
        df_file.sort_values(by=['filename'], inplace=True)
        if df_file.empty:
            return
        df_file['cell_id'] = cell_id
        #df_tmerge = pd.DataFrame()
        start_time = time.time()
        cycle_index_max = 0
        sheetnames = self.buffered_sheetnames(cell_id, conn)
        for ind in df_file.index:
            filename = df_file['filename'][ind]
            cellpath = file_path + filename
            logging.info('buffering file: ' + filename)
        if os.path.exists(cellpath):
            try: 
                df_cell = pd.ExcelFile(cellpath)
            except ValueError as e:
                print('\nI got a ValueError - reason: ' + str(e))
                print('Make sure metadata and data files (and hidden files) are closed. \n')
            # Find the time series sheet in the excel file
            for k in df_cell.sheet_names:
                unread_sheet = True
                sheetname = filename + "|" + k
                try:
                    sheetnames.index(sheetname)
                    print("found:" + sheetname)
                    unread_sheet = False
                except ValueError:
                    print("not found:" + sheetname)
                if "hannel" in k and  k != "Channel_Chart" and unread_sheet:
                    logging.info("file: " + filename + " sheet:" + str(k))
                    timeseries = k
                    #df_time_series_file = pd.read_excel(df_cell, sheet_name=timeseries)
                    df_time_series = pd.DataFrame()
            # if mod_flag==True: #if this cell is part of a module, the timeseries df is passed down from the module class
            #      df_time_series_file = df_cell_ts
            # elif os.path.exists(cellpath):
            #     if file_type=='csv':
            #         df_time_series_file = pd.read_csv(cellpath)
            #     elif file_type=='excel':
                    try:
                        df_time_series_file = pd.read_excel(cellpath, sheet_name=timeseries)
                    except ValueError as e:
                        print('\nI got a ValueError - reason: ' + str(e))
                        print('Make sure metadata and data files (and hidden files) are closed. \n')
                    try:
                        for key,value in mapper.column_mapping.items():
                            df_time_series[key] = df_time_series_file[value]
                        df_time_series['cell_id'] = cell_id
                        df_time_series['sheetname'] = filename + "|" + timeseries
                        df_time_series['component_level'] = 'cell'
                        cycle_index_file_max = df_time_series.cycle_index.max()
                        if cycle_index_file_max > cycle_index_max:
                            cycle_index_max = cycle_index_file_max

                        print('saving sheet: ' + timeseries + ' with max cycle: ' +str(cycle_index_file_max))

                        df_time_series.to_sql('cycle_timeseries_buffer', con=engine, if_exists='append', chunksize=1000, index=False)

                        print("saved=" + timeseries + " time: " + str(time.time() - start_time))

                        start_time = time.time()

                    except KeyError as e:
                        print("I got a KeyError - reason " + str(e))
                        print("processing:" + timeseries + " time: " + str(time.time() - start_time))
                        start_time = time.time()

        return cycle_index_max

    
    def calc_cycle_quantities(self,df):
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
    
    def create_mapper(self,tester):
        if tester=='arbin':
            return arbin()

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
    
    def get_cycle_index_max(self, cell_id, conn, table):
        sql_str = "select max(cycle_index)::int as max_cycles from " + table + " where cell_id = '" + cell_id + "'" ##rconflict
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute(sql_str)
        db_conn.commit()
        record = [r[0] for r in curs.fetchall()]
        if record[0]: 
            cycle_index_max = record[0] 
        else:
            cycle_index_max = 0
        curs.close()
        db_conn.close()
        return cycle_index_max

    def get_cycle_stats_index_max():
        ##rconfict this could be combined with get_cycle_index_max
        return
    
    def get_status(self, cell_id, conn):
        sql_str = "select status from cell_metadata where cell_id = '" + cell_id + "'"
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute(sql_str)
        db_conn.commit()
        record = curs.fetchall()
        if record:
            return record[0]
        else:
            return 'new'
        
    def set_status(self, cell_id, status, conn):
        sql_str = "update " + self.cell_metadata_table + " set status = '" + status + "' where cell_id = '" + cell_id + "'" ##rconflict
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute(sql_str)
        db_conn.commit()
        curs.close()
        db_conn.close()
        return
    
    def clear_buffer(self, cell_id, conn):
        # this method will delete data for a cell_id. Use with caution as there is no undo
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute("delete from " + self.buffer_table + " where cell_id='" + cell_id + "'") ##rconflict
        db_conn.commit()
        curs.close()
        db_conn.close()
        return
    
    def buffered_sheetnames(self, cell_id, conn):
        sql_str = "select distinct sheetname from " + self.buffer_table + " where cell_id = '" + cell_id + "'" ##rconflict
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute(sql_str)
        db_conn.commit()
        record = [r[0] for r in curs.fetchall()]
        curs.close()
        db_conn.close()
        sheetnames=[]
        if record:
            print("record: " + str(record))
            sheetnames = record
        else:
            print("no sheets buffered")
        return sheetnames

class arbin(abstractFileType):
    def __init__(self):
        super().__init__()
        self.column_mapping = {'cycle_index':'Cycle_Index',
                               'test_time':'Test_Time(s)',
                               'i':'Current(A)',
                               'v':'Voltage(V)',
                               'date_time':'Date_Time'}

class liCell(abstractCell):
    def __init__(self,md,slash):
        super().__init__(md, slash)
        self.batt_type = 'li-ion'

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

    # needed to maintain compatibility with windows machines
    if style == 'unix':
        slash = "/"
    elif style == 'windows':
        slash = r'\\'

    mod_flag=False
    if data_type == 'li-cell':
        df_md = pd.read_excel(path + slash + "cell_list.xlsx")
        imp = liCell(df_md, slash)
        tester = df_md['tester'][0]
        if tester == 'arbin':
            map = arbin()
        # elif tester == 'generic':
        #     map = generic()
    elif data_type == 'li-module':
        df_md = pd.read_excel(path + "module_list.xlsx")
        imp = liModule()
        mod_flag=True
    imp.add_data(conn, path, slash, map)


if __name__ == "__main__":
    main(sys.argv[1:])

# class liCellCsv(abstractDataType):
#     def __init__(self):
#         super().__init__()
#         self.batt_type = 'li-ion'
#         self.cell_metadata_table = 'cell_metadata'
#         self.cycle_metadata_table = 'cycle_metadata'
#         self.timeseries_table = 'cycle_timeseries'
#         self.buffer_table = 'cycle_timeseries_buffer'
#         self.stats_table = 'cycle_stats'

#     def buffer(self, cell_id, source, df_time_series_file, filename, sheetnames, engine, start_time):
#         cycle_index_max = 0
#         if source=='ISU-ILCC':
#         #Calculate the Time (s) for the UConn data (only has date time)
#             df_time_series_file['pystamp']=pd.to_datetime(df_time_series_file['Timestamp']) #convert to python date-time format in ns
#             df_time_series_file['inttime']=df_time_series_file['pystamp'].astype(int)
#             df_time_series_file['inttime']=df_time_series_file['inttime'].div(10**9)
#             df_time_series_file['Time [s]']=df_time_series_file['inttime']-df_time_series_file['inttime'].iloc[0]

#         df_time_series = pd.DataFrame()

#         try:
#             if source=='ISU-ILCC':
#                 df_time_series['cycle_index'] = df_time_series_file['Cycle'] 
#                 df_time_series['test_time'] = df_time_series_file['Time [s]']
#                 df_time_series['i'] = df_time_series_file['Current (A)'] 
#                 df_time_series['v'] = df_time_series_file['Voltage (V)']
#                 df_time_series['date_time'] = df_time_series_file['Timestamp'] 
 
#             elif source=='TON-KIT':
#                 df_time_series['cycle_index'] = df_time_series_file['cycle number']
#                 df_time_series['test_time'] = df_time_series_file['time/s']
#                 df_time_series['i'] = df_time_series_file['<I>/mA']
#                 df_time_series['v'] = df_time_series_file['Ecell/V']

#             elif source=='XCEL':
#                 df_time_series['cycle_index'] = df_time_series_file['cycle_index']
#                 df_time_series['test_time'] = df_time_series_file['test_time']
#                 df_time_series['i'] = df_time_series_file['i']
#                 df_time_series['v'] = df_time_series_file['v']
#                 df_time_series['date_time'] = df_time_series_file['date_time']
#                 df_time_series['env_temperature'] = df_time_series_file['env_temperature']
                
#             df_time_series['cell_id'] = cell_id
#             df_time_series['sheetname'] = filename
#             df_time_series['component_level'] = 'cell'

#             cycle_index_file_max = df_time_series.cycle_index.max()

#             print('saving sheet: with max cycle: ' +str(cycle_index_file_max)) ##weird

#             df_time_series.to_sql(self.buffer_table, con=engine, if_exists='append', chunksize=1000, index=False)

#             print("saved=" + filename + " time: " + str(time.time() - start_time))

#             start_time = time.time()

#         except KeyError as e:
#             print("I got a KeyError - reason: " + str(e))
#             print("processing: time: " + str(time.time() - start_time))##weird
#             start_time = time.time()

#         return cycle_index_max