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
        self.cell_metadata_table = ''
        self.cycle_metadata_table = ''
        self.timeseries_table = ''
        self.buffer_table = ''
        self.stats_table = ''
        self.cell_md = md #to get fixed md
        self.slash = slash

    #add cells to the database
    def add_data(self, conn, path, mapper): ##conflict how to pass all tables
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
            mapper = self.create_mapper(tester, source)
            print(mapper)

            logging.info("add file: " + file_id + " cell: " + cell_id)
            df_tmp = self.cell_md.iloc[ind]
            df_cell_md, df_cycle_md = self.populate_metadata(df_tmp) ##conflict module?
            engine = create_engine(conn)

            # check if the cell is already there and report status
            status = self.get_status(cell_id, conn) ##conflict module
            if status=="completed":
                print("skipping cell_id: " + cell_id + " (import completed)") ##conflict module
                continue 
            print(df_tmp)
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
                            df_cycle_stats = self.calc_stats(df_ts, cell_id, engine)
                            df_cycle_timeseries = self.calc_timeseries(df_ts,cell_id, engine)
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

    def calc_timeseries(self, df_t, ID, engine):
        return
    
    def calc_stats(self, df_t, ID, engine):
        return
    
    def buffer(self, engine, conn, path, cell_id, file_id, mapper):
        return
    
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
    
    def create_mapper(self,tester, source):
        if tester == 'generic': #find a way to remove need for this
            tester = 'csv_' + source
        with open(f'mapper.yaml','r') as f:
            for mapping in list(yaml.safe_load_all(f)):
                if mapping['tester'] == tester:
                    return mapping
        print("Please verify that 'tester' in cell_list/module_list etc. matches with mapper.yaml")
        os._exit(0)

    def populate_metadata(self, df_c_md): ##conflict need to pass cell type from main
        #gets overwritten by subclasses
        return
    
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

    def get_status(self, cell_id, conn):
        sql_str = "select status from cell_metadata where cell_id = '" + cell_id + "'"
        db_conn = psycopg2.connect(conn)
        curs = db_conn.cursor()
        curs.execute(sql_str)
        db_conn.commit()
        record = curs.fetchall()
        if record:
            return record[0][0]
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
        return sheetnames

    def get_sheetname(self, cell_id, conn, cellpath, filename):
        #called for excel files
        sheetnames = self.buffered_sheetnames(cell_id, conn)
        if os.path.exists(cellpath):
            try: 
                df_cell = pd.read_excel(cellpath) #test to see if read_excel works vsa excelfile
            except ValueError as e:
                print('\nI got a ValueError - reason: ' + str(e))
                print('Make sure metadata and data files (and hidden files) are closed. \n')
            # Find the time series sheet in the excel file
            for k in df_cell.sheet_names:
                unread_sheet = True
                sheetname = filename + "|" + k
                try:
                    sheetnames.index(sheetname)
                    print("sheetname: " + sheetname + " already in database.")
                    unread_sheet = False
                except ValueError:
                    print("new sheetname: " + sheetname)
                if 'channel' in k.lower() and  k != "Channel_Chart" and unread_sheet:
                    logging.info("file: " + filename + " sheet:" + str(k))
                    return k
            return None

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