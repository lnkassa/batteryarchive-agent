# Data Import Agent Breakdown
This code takes files from a selected folder, and using instructions from an associated metadata file, imports the data into the postgres database. It keeps track of the import using the status column. A new file is marked 'new' then the data is entered into the buffer table. Once that is complete, the code calculates each cycle's statistics in chunks of 30 cycles. These statistics and the 30 cycles of timeseries data are imported into their respective tables. Once all the data is imported, the file is marked 'completed'.\
Please see the importing data file for more information on how to run the code and import data.\
Please see the schema description for more information about the tables.

## Requirements
Python Modules:\
-os\
-glob\
-pandas\
-numpy\
-h5py\
-sqlalchemy\
-yaml\
-psycopg2\
-logging\
-time\
-sys\
-getopt\
-logging\
-time

## Function List
| Function | Description |
| -------- | ----------- |
|convert_mat_to_df(f):| Converts matlab files to a pandas dataframe
|calc_cycle_quantities(df):| Calculates certain quantities to be used in calc_stats()
|calc_stats(df_t, ID):| Calculates statistics for each cycle, in chunks of 30 cycles per call
|read_save_timeseries_arbin(cell_id, file_path):| Loads arbin-type data files into the buffer table
|read_save_timeseries_json(cell_id, file_path, engine, conn):| Loads json-type files into the buffer table
|read_save_timeseries_csv(cell_id, file_path, source, engine, conn):| Loads csv files in to the buffer table
|read_save_timeseries_voltaiq(cell_id, file_path, engine, conn):| Loads voltaiq-csv-type files into the buffer table
|read_save_timeseries_matlab(cell_id, file_path, engine, conn):| Loads matlab files into the buffer table by calling convert_mat_to_df()
|populate_cycle_metadata(df_c_md):| Loads metadata into the cell and cycle metadata tables
|clear_buffer(cell_id, conn):| Clears the buffer table once all data is processed.
|set_cell_status(cell_id, status, conn):| Updates the status of the cell (i.e. new, buffering, processing, completed)
|get_cycle_index_max(cell_id,conn):| Gets the current/largest cycle index from the buffer table.
|get_cycle_stats_index_max(cell_id,conn):| Gets the current/largest cycle index from the stats table.
|check_cell_status(cell_id,conn):| Gets the status of the cell (i.e. new, buffering, processing, completed) |
|buffered_sheetnames(cell_id, conn): | Gets the sheetnames in the buffered file. Used in arbin function |
|add_ts_md_cycle(cell_list, conn, save, plot, path, slash):| Import new data file(s) by checking the status and calling the appropriate function for the data type. Saves the data from the buffer to the timeseries table.
|main(argv):| Sets up command line run capability




```

```


```

```
