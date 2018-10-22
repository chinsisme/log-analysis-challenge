import pandas as pd
import numpy as np
import os
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

try:
    pymysql_conn = pymysql_connect()
    cur = pymysql_conn.cursor()
except Exception as e:
    print(e)

# Copy file to current folder
copy(file_source, file_destination)

# Get number of lines in the file first (runs one time only)
original_number_of_lines = int(subprocess.check_output(
    "wc -l {}".format(file_destination + '/out.log'), shell=True).decode('ascii').split(' ')[0])

# Column names
columns_log = ['LogType', 'Date', 'Time',
               'DateTime', 'PID', 'ResponseTime', 'UID', 'URL']

# Dataframe with all logs
df_logs = pd.DataFrame(columns=columns_log)

f = open(file_destination + '/out.log', 'r')

"""
First, process all lines upto the length of the file calculated at the start of the lines.
Then, wait for length of the file to keep changing. After every change, process the new lines.
"""

for line in f.readlines():
    row = parse_to_dataframe(line)
    if(row):
        df_logs.loc[len(df_logs)] = row
        print(row)
    else:
        pass
df_logs.to_sql(con=sqlalchemy_conn, name='logs',
               if_exists='append', index=False)

print('Loaded entire log file into a dataframe.')
print(df_logs.head(10))

while(True):
    current_number_of_lines = int(subprocess.check_output(
        "wc -l {}".format(file_destination + '/out.log'), shell=True).decode('ascii').split(' ')[0])
    print('Original number of lines')
    print(original_number_of_lines + 1)
    print('Current number of lines')
    print(current_number_of_lines + 1)
    if(original_number_of_lines < current_number_of_lines):
        lines = subprocess.check_output("awk 'NR > {} && NR <= {}' out.log".format(
            original_number_of_lines + 1, current_number_of_lines + 1), shell=True).decode('ascii').split('\n')
        print('New log entries detected.')
        rows = []
        for line in lines:
            print(line)
            print('\n\n')
            row = parse_to_dataframe(line)
            print(row)
            if(row):
                df_logs.loc[len(df_logs)] = row
                rows.append(row)
        # Add new rows to MySQL table
        query = generate_insert_query('logs', columns_log, rows)
        print(query)
        try:
            cur.execute(query)
            pymysql_conn.commit()
        except Exception as e:
            print(e)

        print('Written to SQL table.')
    original_number_of_lines = current_number_of_lines
    print(df_logs.tail(3))
    print('Sleeping for ten seconds.')
    time.sleep(10)
