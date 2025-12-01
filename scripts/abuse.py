#!/usr/bin/env python
# coding: utf-8
#from imghdr import tests
import os
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
import zipfile
import time

# Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

# Function to convert a list to a string
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

#for matlab files
def convert_mat_to_df(batch):
    num_cells = batch['summary'].shape[0]
    bat_dict = {}
    for i in range(num_cells):
        cycle_dataframes = []
        cl = f[batch['cycle_life'][i,0]][()]
        summary_CY = np.hstack(f[batch['summary'][i,0]]['cycle'][0,:].tolist())
        cycles = f[batch['cycles'][i,0]]
        cycle_dict = {}
        no_cycles = cycles['I'].shape[0]
        for j in range(no_cycles):
            I = np.hstack((f[cycles['I'][j,0]][()]))
            Qc = np.hstack((f[cycles['Qc'][j,0]][()]))
            Qd = np.hstack((f[cycles['Qd'][j,0]][()]))
            T = np.hstack((f[cycles['T'][j,0]][()]))
            V = np.hstack((f[cycles['V'][j,0]][()]))
            #dQdV = np.hstack((f[cycles['discharge_dQdV'][j,0]][()]))
            t = np.hstack((f[cycles['t'][j,0]][()]))
            cd = {'I': I, 'Qc': Qc, 'Qd': Qd, 'T': T, 'V':V, 't':t}
            cycle_dict[str(j)] = cd
            df_cycle = pd.DataFrame(cd)
            df_cycle['cycle_number'] = summary_CY[j]
            cycle_dataframes.append(df_cycle)
    
        df_battery = pd.concat(cycle_dataframes)

        cell_dict = {'cycle_life': cl, 'summary': summary_CY, 'cycles': cycle_dict}
        key = 'b3c' + str(i)
        bat_dict[key] = cell_dict
        
    print(df_battery)
    return df_battery

# unpack the dataframe and calculate quantities used in statistics
def calc_cycle_quantities(df):

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


# calculate statistics and cycle time
def calc_stats(df_t, ID):

    logging.info('calculate cycle time and cycle statistics')
    df_t['cycle_time'] = 0

    no_cycles = int(df_t['cycle_index'].max())
    
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
                'cycle_index': float,
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
                'e_eff': float
            }
 
    df_c = df_c.astype(convert_dict)

    for c_ind in df_c.index:
        #x = c_ind + 1
        x = no_cycles + c_ind - 29
        
        df_f = df_t[df_t['cycle_index'] == x] ##optimize call
        
        df_f['ah_c'] = 0
        df_f['e_c'] = 0
        df_f['ah_d'] = 0
        df_f['e_d'] = 0
        
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

                df_f = calc_cycle_quantities(df_f)
                df_t['cycle_time'] = df_t['cycle_time'].astype('float64') #to address dtype warning

                df_t.loc[df_t.cycle_index == x, 'cycle_time'] = df_f['cycle_time']
                df_t.loc[df_t.cycle_index == x, 'ah_c'] = df_f['ah_c']
                df_t.loc[df_t.cycle_index == x, 'e_c'] = df_f['e_c']
                df_t.loc[df_t.cycle_index == x, 'ah_d'] = df_f['ah_d']
                
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
    df_tt = df_t[df_t['cycle_index'] > 0]

    return df_cc, df_tt

# sort data imported to insure cycle index and test times are correctly calculated
def sort_timeseries(df_tmerge):
    # Arrange the data by date time first, then by test time
    # Rebuild Cycle Index and test time to increment from file to file
    # This method does not depend on data from a specific testers

    logging.info('sorting timeseries dataframe')

    if not df_tmerge.empty:

        df_t = df_tmerge.sort_values(by=['date_time'])
        df_t = df_t.reset_index(drop=True)

        cycles = df_t[["cycle_index_file", "cycle_index", "filename", "test_time"]].to_numpy()

        max_cycle = 1
        past_index = 1
        max_time = 0
        last_file = ""
        delta_t = 0
        start = 0

        for x in cycles:

            if start == 0:
                last_file = x[2]
                start += 1

            if x[2] != last_file:
                delta_t = max_time
                x[3] += delta_t
                last_file = x[2]
            else:
                x[3] += delta_t
                max_time = x[3]
                last_file = x[2]

            if x[0] < max_cycle:

                if past_index == x[0]:
                    past_index = x[0]
                    x[1] = max_cycle
                else:
                    past_index = x[0]
                    x[1] = max_cycle + 1
                    max_cycle = x[1]

            else:
                past_index = x[0]
                max_cycle = x[0]
                x[1] = x[0]

        df_tmp = pd.DataFrame(data=cycles[:, [1]], columns=["cycle_index"])
        df_t['cycle_index'] = df_tmp['cycle_index']

        df_tmp = pd.DataFrame(data=cycles[:, [3]], columns=["test_time"])
        df_t['test_time'] = pd.to_numeric(df_tmp['test_time'])

        df_ts = df_t.sort_values(by=['test_time'])

        # Remove quantities only needed to tag files
        df_ts.drop('filename', axis=1, inplace=True)
        df_ts.drop('cycle_index_file', axis=1, inplace=True)

        return df_ts


# Build cell metadata
def populate_abuse_metadata(df_c_md):

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
    df_cell_md['weight'] = [df_c_md['weight']]
    df_cell_md['dimensions'] = [df_c_md['dimensions']]
    
    # Build cycle metadata
    df_abuse_md = pd.DataFrame()
    df_abuse_md['cell_id'] = [df_c_md['cell_id']]
    df_abuse_md['v_init'] = [df_c_md['v_init']]
    df_abuse_md['indentor'] = [df_c_md['indentor']]
    df_abuse_md['nail_speed'] = [df_c_md['nail_speed']]
    df_abuse_md['soc'] = [df_c_md['soc']]

    return df_cell_md, df_abuse_md


# direct_query
def execute_query(sql_str, conn):

    # this method will delete data for a cell_id. Use with caution as there is no undo
    db_conn = psycopg2.connect(conn)
    curs = db_conn.cursor()
    curs.execute(sql_str)
    db_conn.commit()
    curs.close()
    db_conn.close()

    return


# delete records (call with caution)
def delete_records(cell_id, conn):
    # this method will delete data for a cell_id. Use with caution as there is no undo
    db_conn = psycopg2.connect(conn)
    curs = db_conn.cursor()

    curs.execute("delete from timeseries_data where cell_id='" + cell_id + "'")
    curs.execute("delete from cycle_data where cell_id='" + cell_id + "'")
    curs.execute("delete from cell_metadata where cell_id='" + cell_id + "'")
    curs.execute("delete from cycle_metadata where cell_id='" + cell_id + "'")

    db_conn.commit()
    curs.close()
    db_conn.close()

    return


# delete records (call with caution)
def clear_buffer(cell_id, conn):
    # this method will delete data for a cell_id. Use with caution as there is no undo
    db_conn = psycopg2.connect(conn)
    curs = db_conn.cursor()

    curs.execute("delete from cycle_timeseries_buffer where cell_id='" + cell_id + "'")

    db_conn.commit()
    curs.close()
    db_conn.close()

    return


def set_cell_status(cell_id, status, conn):

    sql_str = "update cell_metadata set status = '" + status + "' where cell_id = '" + cell_id + "'"

    db_conn = psycopg2.connect(conn)
    curs = db_conn.cursor()
    curs.execute(sql_str)
    db_conn.commit()
    curs.close()
    db_conn.close()

    return


def get_cycle_index_max(cell_id,conn):


    sql_str = "select max(cycle_index)::int as max_cycles from cycle_timeseries_buffer where cell_id = '" + cell_id + "'"

    db_conn = psycopg2.connect(conn)
    curs = db_conn.cursor()
    curs.execute(sql_str)
    db_conn.commit()

    record = [r[0] for r in curs.fetchall()]

    if record[0]: 
        # bad valerio -- very bad! you are a very bad man!!
        cycle_index_max = record[0]
    else:
        cycle_index_max = 0

    curs.close()
    db_conn.close()

    return cycle_index_max


def get_cycle_stats_index_max(cell_id,conn):


    sql_str = "select max(cycle_index)::int as max_cycles from cycle_stats where cell_id = '" + cell_id + "'"

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


def check_cell_status(cell_id,conn):

    status = 'new'

    sql_str = "select * from cell_metadata where cell_id = '" + cell_id + "'"

    db_conn = psycopg2.connect(conn)
    curs = db_conn.cursor()
    curs.execute(sql_str)
    db_conn.commit()

    record = curs.fetchall()

    if record: 
        status = record[0][8]
    else:
        status = 'new'

    curs.close()
    db_conn.close()

    print('cell status is: ' + status)

    return status


def buffered_sheetnames(cell_id, conn):

    sql_str = "select distinct sheetname from cycle_timeseries_buffer where cell_id = '" + cell_id + "'"

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
        print("empty list")

    return sheetnames


# calculate statistics for abuse test
def calc_abuse_stats(df_t, df_test_md):

    for _ in df_t.index:
        df_t['norm_d'] = df_t.iloc[0:, df_t.columns.get_loc('axial_d')] - df_t['axial_d'][0]
        df_t['strain'] = df_t.iloc[0:, df_t.columns.get_loc('norm_d')] / df_test_md['indentor']

    return df_t


# calculate statistics for abuse test
def read_ornlabuse(file_path, cell_id):

    excels = glob.glob(file_path + '*.xls*')

    df_tmerge = pd.DataFrame()
    for excel in excels:
        if '~$' in excel:
            continue
        df_ts_file = pd.read_excel(
            excel, sheet_name='Sheet1')  # dictionary of sheets

        df_ts_a = pd.DataFrame()
        df_ts_a['test_time'] = df_ts_file['Time (second)']
        df_ts_a['axial_d'] = df_ts_file['Displacement (mm)']
        df_ts_a['v'] = df_ts_file['Voltage (V)']
        df_ts_a['axial_f'] = df_ts_file['Penetrator Force (N)']
        df_ts_a['load'] = df_ts_file['Load (lb)']

        df_ts_a['top_indent_temperature'] = 0
        df_ts_a['top_back_temperature'] = 0
        df_ts_a['left_bottom_temperature'] = 0
        df_ts_a['right_bottom_temperature'] = 0
        df_ts_a['above_punch_temperature'] = 0
        df_ts_a['below_punch_temperature'] = 0

        df_ts_b = pd.DataFrame()
        df_ts_b['test_time'] = df_ts_file['Time (sec) ']
        df_ts_b['axial_d'] = 0
        df_ts_b['v'] = 0
        df_ts_b['axial_f'] = 0

        if 'TC1 top indent [C]' in df_ts_file:
            print("6 cols" + cell_id) 
            df_ts_b['top_indent_temperature'] = df_ts_file['TC1 top indent [C]']
            df_ts_b['top_back_temperature'] = df_ts_file['TC2 top back [C]']
            df_ts_b['left_bottom_temperature'] = df_ts_file['TC3 bottom back [C]']
            df_ts_b['right_bottom_temperature'] = df_ts_file['TC4 bottom indent [C]']
            df_ts_b['above_punch_temperature'] = df_ts_file['TC5 above punch [C]']
            df_ts_b['below_punch_temperature'] = df_ts_file['TC6 below punch [C]']
        elif 'TC1 (°C)' in df_ts_file:
            print("1 col:" + cell_id)
            df_ts_b['below_punch_temperature'] = df_ts_file['TC1 (°C)']

        if df_tmerge.empty:
            df_tmerge = df_ts_a
            df_tmerge = pd.concat([df_tmerge, df_ts_b], ignore_index=True)
        else:
            df_tmerge = pd.concat([df_tmerge, df_ts_a], ignore_index=True)
            df_tmerge = pd.concat([df_tmerge, df_ts_b], ignore_index=True)

    df_tmerge['cell_id'] = cell_id

    return df_tmerge


# read the abuse excel files from SNL
def read_snlabuse(file_path, cell_id):

    excels = glob.glob(file_path + '*.xls*')

    df_tmerge = pd.DataFrame()

    for excel in excels:
        if '~$' in excel:
            continue
        df_ts_file = pd.read_excel(
            excel, sheet_name='Sheet1')  # dictionary of sheets

        df_ts = pd.DataFrame()
        df_ts['test_time'] = df_ts_file['Test Time [s]']
        df_ts['axial_d'] = df_ts_file['Displacement [mm]']
        df_ts['axial_f'] = df_ts_file['Penetrator Force [mm]']
        df_ts['v'] = df_ts_file['vCell [V]']
        df_ts['ambient_temperature'] = df_ts_file['tAmbient [C]']
        df_ts['top_indent_temperature'] = df_ts_file['TC1 near positive terminal [C]']
        df_ts['top_back_temperature'] = df_ts_file['TC2 near negative terminal [C]']
        df_ts['left_bottom_temperature'] = df_ts_file['TC3 bottom - bottom [C]']
        df_ts['right_bottom_temperature'] = df_ts_file['TC4 bottom - top [C]']
        df_ts['above_punch_temperature'] = df_ts_file['TC5 above punch [C]']
        df_ts['below_punch_temperature'] = df_ts_file['TC6 below punch [C]']

        if df_tmerge.empty:
            df_tmerge = df_ts
        else:
            ##df_tmerge = df_tmerge.append(df_ts, ignore_index=True)
            df_tmerge = pd.concat([df_tmerge, df_ts], ignore_index=True)

    df_tmerge['cell_id'] = cell_id

    return df_tmerge


# add cells to the database
def add_ts_md_abuse(cell_list, conn, save, plot, path, slash):
    # The importer expects an Excel file with cell and test information
    # The file contains one row per cell

    logging.info('add cells')
    df_excel = pd.read_excel(cell_list)

    # Process one cell at the time
    for ind in df_excel.index:

        cell_id = df_excel['cell_id'][ind]
        file_id = df_excel['file_id'][ind]
        tester = df_excel['tester'][ind]

        logging.info("add file: " + file_id + " cell: " + cell_id)

        df_tmp = df_excel.iloc[ind]

        print(df_tmp)

        df_cell_md, df_abuse_md = populate_abuse_metadata(df_tmp)

        engine = create_engine(conn)

        logging.info('save cell metadata')
        df_cell_md.to_sql('cell_metadata', con=engine, if_exists='append', chunksize=1000, index=False)
        logging.info('save cycle metadata')
        df_abuse_md.to_sql('abuse_metadata', con=engine, if_exists='append', chunksize=1000, index=False)

        file_path = path + file_id + slash

        df_abuse_ts = pd.DataFrame()   

        print("tester=" + tester)

        if tester=='ORNL-Servo-Motor':
            df_abuse_ts = read_ornlabuse(file_path, cell_id)
        if tester=='SNL-Hydraulic':
            df_abuse_ts = read_snlabuse(file_path, cell_id)
       
        if not df_abuse_ts.empty:
            df_abuse_ts = calc_abuse_stats(df_abuse_ts, df_abuse_md)
            df_abuse_ts.to_sql('abuse_timeseries', con=engine, if_exists='append', chunksize=1000, index=False)
            status = 'completed'
            set_cell_status(cell_id, status, conn)
            

def main(argv):

    # command line variables that can be used to run from an IDE without passing arguments
    mode = 'env'
    path = r'\\'

    # initializing the logger
    logging.basicConfig(format='%(asctime)s %(message)s', filename='blc-python.log', level=logging.DEBUG)
    logging.info('starting')

    try:
        opts, args = getopt.getopt(argv, "hm:p:t:", ["mode=", "path=", "test="])
    except getopt.GetoptError:
        print('run as: data_import.py -m <mode> -t <test> -p <path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('data_import.py -m <mode> -t <test> -p <path>')
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-t", "--test"):
            test = arg
        elif opt in ("-p", "--path"):
            path = arg

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

    # Mode of operation
    if mode == 'add':
        if test == 'abuse':
            add_ts_md_abuse(path + "cell_list.xlsx", conn, save, plot, path, slash)
        logging.info('Done adding files')
    elif mode == 'env':
        logging.info('printing environment variables only')
        print("style: " + style)
        print("  -slash: " + slash)
        print("  -path: " + path)
        print("conn: " + conn)
        print("plot: " + str(plot))
        print("save: " + str(save))
    else:
        print('data_import.py -m <mode> -p <path>')


if __name__ == "__main__":
    #import cProfile
    main(sys.argv[1:])
    #cProfile.run('main()')





