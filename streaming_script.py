import pandas as pd
import numpy as np
import os
import sys
import subprocess
from matplotlib import pyplot as plt
from shutil import copy
import time

from functions.parse import parse_to_dataframe
from functions.connect_sql import sqlalchemy_connect, pymysql_connect
from functions.insert_query_generator import generate_insert_query

# File source
file_source = '/usr/me/out.log'
file_destination = os.getcwd()

# Connect to MySQL instance
try:
    sqlalchemy_conn = sqlalchemy_connect()
except Exception as e:
    print(e)
    sys.exit()

try:
    pymysql_conn = pymysql_connect()
    cur = pymysql_conn.cursor()
except Exception as e:
    print(e)
    sys.exit()
# Name of the table
logs_table = 'logs'
cursor_positon_table = 'cursor_position'


# Copy file to current folder
copy(file_source, file_destination)

# Resume after last processed line
get_cursor_position = """
SELECT position 
FROM   {}; 
""".format(cursor_positon_table)
try:
    cur.execute(get_cursor_position)
    original_line_number = int(cur.fetchone()[0])
except Exception as e:
    print(e)
    sys.exit('Could not get cursor position.')


# Column names
columns_log = ['LogType', 'Date', 'Time',
               'DateTime', 'PID', 'ResponseTime', 'UID', 'URL']

# Dataframe with all logs
df_logs = pd.DataFrame(columns=columns_log)

f = open(file_destination + '/out.log', 'r')

"""
Fetch the current line from the database.
Wait for length of the file to keep changing. After every change, process the new lines.
"""

while(True):
    insert_rows_chunk_size = 20
    current_line_number = int(subprocess.check_output(
        "wc -l {}".format(file_destination + '/out.log'), shell=True).decode('ascii').split(' ')[0])
    print('Original line number')
    print(original_line_number + 1)
    print('Current line number')
    print(current_line_number + 1)
    if(original_line_number < current_line_number):
        lines = subprocess.check_output("awk 'NR > {} && NR <= {}' out.log".format(
            original_line_number + 1, current_line_number + 1), shell=True).decode('ascii').split('\n')
        print('New log entries detected.')
        rows = []
        for line in lines:
            # print(line)
            # print('\n\n')
            row = parse_to_dataframe(line)
            # print(row)
            if(row):
                df_logs.loc[len(df_logs)] = row
                rows.append(row)
        # What if the number of new rows is smaller than insert_rows_chunk_size ?
        if(current_line_number - original_line_number <= insert_rows_chunk_size):
            insert_rows_chunk_size = current_line_number - original_line_number
        # Insert into the table, chunk-by-chunk
        for i in range(0, len(rows), insert_rows_chunk_size):
            """ 
            The following commented code is an alternative to using pandas by generating a query.
            Please look in functions -> insert_query_generator 
            """
            # Generate SQL query for every chunk.
            # query = generate_insert_query(
            #     'logs', columns_log, rows[i:i+insert_rows_chunk_size])
            # print(query)
            # Insert chunk into SQL table
            # try:
            #     cur.execute(query)
            #     pymysql_conn.commit()
            # except Exception as e:
            #     print(e)
            print(i)
            print(rows[i:i+insert_rows_chunk_size])
            pd_chunk = pd.DataFrame(
                columns=columns_log, data=rows[i:i+insert_rows_chunk_size])
            pd_chunk.to_sql(
                con=sqlalchemy_conn, name=logs_table, if_exists='append', index=False)
            try:
                cur.execute(""" 
                            UPDATE {}
                            SET position = {} 
                                """.format(cursor_positon_table, i))
                pymysql_conn.commit()
            except Exception as e:
                print(e)
            print('Written to SQL table.')
            print(pd_chunk)
            print('\n\n\n')
            time.sleep(1)
    original_line_number = current_line_number
    print(df_logs.tail(3))
    print('Sleeping for ten seconds.')
    time.sleep(10)
