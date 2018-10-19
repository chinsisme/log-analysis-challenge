import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from shutil import copy

file_source = '/tmp/me/out.log'
file_destination = os.getcwd()

# Function generate new column


def datetime(row):
    return row.Date + ' ' + row.Time


# Copy file to current folder
copy(file_source, file_destination)

# Set columns for the dataframe
columns_log = ['LogType', 'Date', 'Time', 'PID', 'ResponseTime', 'UID', 'URL']

# Create dataframe
df_logs = pd.DataFrame(columns=columns_log)

# Load and transform log data into dataframe
with open(file_destination + '/out.log', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # Eliminate incorrect entries
        if('Something messed up' in line):
            pass
        else:
            for log_identifier in ['[ERROR]', '[DEBUG]', '[INFO]']:
                if(log_identifier in line):
                    log_array = line.split(log_identifier)[0].split(' ')
                    # Constructing columns
                    log_type = log_identifier.replace('[', '').replace(']', '')
                    date = str(log_array[0])
                    time = str(log_array[1])
                    pid = str(log_array[3]).replace('[', '').replace(']', '')
                    response_time = str(log_array[4]).replace(
                        '[', '').replace(']', '').replace('ms', '')
                    uid = str(log_array[6]).replace(']', '')
                    url = line.split(log_identifier)[1].split(' ')[1]
                    df_logs.loc[len(df_logs)] = [log_type, date,
                                                 time, pid, response_time, uid, url]

# Remove file from current folder
os.remove('out.log')


"""
Generating visualization for number of errors per hour
"""
# Create dataframe containing only errors
df_only_error = df_logs[df_logs.LogType == 'ERROR']

df_error_group_by_date_time = df_only_error['ResponseTime'].groupby(
    [df_only_error['Date'], df_only_error['Time'].str.slice(start=0, stop=2)])
series_error_count = df_error_group_by_date_time.count()
series_error_count = series_error_count.reset_index(name='ErrorCount')
df_error_count = pd.DataFrame(series_error_count)

df_error_count['Datetime'] = df_error_count.apply(
    lambda row: datetime(row), axis=1)

# Plot graph for error count per hour
# plt.plot(df_error_count['Datetime'], df_error_count['ErrorCount'])
# plt.show()


"""
Generating percentile stats for response times of successful responses
"""
# Create dataframe containing only successful responses
df_non_error = df_logs[df_logs.LogType != 'ERROR']
df_non_error['ResponseTime'] = df_non_error['ResponseTime'].apply(
    pd.to_numeric)

# df_non_error_average_response = pd.to_numeric(df_non_error['ResponseTime']).groupby(
#     [df_non_error['Date'], df_non_error['Time'].str.slice(start=0, stop=2)]).mean().reset_index()

# df_non_error_average_response['Datetime'] = df_non_error_average_response.apply(
#     lambda row: datetime(row), axis=1)

# Plot graph for response time for successful requests
# plt.plot(df_non_error_average_response['Datetime'],
#          df_non_error_average_response['ResponseTime'])
# plt.show()

print(df_non_error[['LogType', 'ResponseTime']].quantile(0.8))

df_percentile = pd.DataFrame(columns=['Percentile', 'ResponseTime'])
percentile_list = [0.5, 0.9, 0.95]
for percentile in percentile_list:
    df_percentile.loc[len(df_percentile)] = [str(percentile * 100) + '%',
                                             df_non_error[['LogType', 'ResponseTime']].quantile(percentile).tolist()[0]]

print(df_percentile)
